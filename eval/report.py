"""Full evaluation report: retrieval quality and answer quality on eval/questions.jsonl.

Retrieval (answerable questions only), for vector, keyword and hybrid search:
  hit@k and MRR with 95 % bootstrap confidence intervals, split by question language.
Answers (all questions, the app's default pipeline = hybrid search + LLM):
  fact correct  every expected fact appears in the answer ("facts": groups of alternatives)
  cited         the answer contains a [n] citation
  language      the answer is in the language of the question
  refused       the answer says the documents don't contain it (wanted only for unanswerable questions)

Usage (from the project root):  python -m eval.report
        python -m eval.report --rescore   re-check the saved answers without calling the LLM again
Results: experiments/results/evaluation.md and evaluation.json
"""
import json
import random
import re
import statistics
import sys
import time
from pathlib import Path

from app.config import LLM_MODEL, PROMPT_VERSION, RERANK, TOP_K
from app.db import get_conn
from app.llm import generate_answer
from app.retrieve import search
from eval.run_eval import answerable, evaluate, load_items

OUT = Path("experiments/results")
BOOTSTRAP_SAMPLES = 2000

REFUSAL = re.compile(
    r"keine (explizite |genaue |konkrete )?(angabe|information|antwort|zahl)"
    r"|nicht (direkt |explizit |genau )?(im|in den|angegeben|enthalten|zu finden|erwähnt|beantwort|bestätigen|bestimmen)"
    r"|no information|not (explicitly |directly )?(mentioned|contain|found|specified|provided|stated)"
    r"|do(es)? not (say|contain|mention|specify)"
    r"|cannot (find|answer)|don't know|do not know|weiß (ich )?nicht",
    re.IGNORECASE,
)
CITATION = re.compile(r"\[\d+\]")
DE_WORDS = set("der die das und ist nicht ein eine einer im in den dem für mit von zu sind wird werden es beträgt dauert "
               "muss kann darf nach bei oder auch wenn wer man stunden wochen jahre semester gibt".split())
EN_WORDS = set("the is are and of to in a an for not with it be must can may after if who weeks hours years semesters "
               "there this that".split())


def has_fact(answer: str, alternatives: list[str]) -> bool:
    text = answer.lower()
    for alt in alternatives:
        if alt.isdigit():  # a number must stand alone: "5" should not match "15" or "2025"
            if re.search(rf"(?<![\d.,]){alt}(?![\d])", text):
                return True
        elif alt.lower() in text:
            return True
    return False


def detect_language(text: str) -> str | None:
    words = re.findall(r"[a-zäöüß]+", text.lower())
    de, en = sum(w in DE_WORDS for w in words), sum(w in EN_WORDS for w in words)
    return None if de == en else ("de" if de > en else "en")


def bootstrap_ci(values: list[float], seed: int = 0) -> tuple[float, float]:
    rng = random.Random(seed)
    means = sorted(statistics.mean(rng.choices(values, k=len(values))) for _ in range(BOOTSTRAP_SAMPLES))
    return means[int(0.025 * BOOTSTRAP_SAMPLES)], means[int(0.975 * BOOTSTRAP_SAMPLES) - 1]


def retrieval(items: list[dict]) -> dict:
    qs = answerable(items)
    out = {}
    for mode, rerank in (("vector", False), ("keyword", False), ("hybrid", False), ("hybrid", True)):
        r = evaluate(qs, mode, TOP_K, rerank)
        mode = r["mode"]
        hits = [1.0 if x and x <= TOP_K else 0.0 for x in r["ranks"]]
        rr = [1 / x if x else 0.0 for x in r["ranks"]]
        by_lang = {lang: round(statistics.mean(h for h, q in zip(hits, qs) if q["lang"] == lang), 3) for lang in ("en", "de")}
        out[mode] = {"hit": round(statistics.mean(hits), 3), "hit_ci": [round(x, 2) for x in bootstrap_ci(hits)],
                     "mrr": round(statistics.mean(rr), 3), "mrr_ci": [round(x, 2) for x in bootstrap_ci(rr)],
                     "hit_by_lang": by_lang, "ranks": r["ranks"]}
    return out


def score(item: dict, text: str, seconds: float) -> dict:
    return {
        "question": item["question"], "lang": item["lang"], "expected": item["answer"],
        "answerable": item.get("answerable", True), "answer": text, "seconds": seconds,
        "fact_correct": all(has_fact(text, g) for g in item["facts"]) if item["facts"] else None,
        "cited": bool(CITATION.search(text)),
        "answer_lang": detect_language(text),
        "refused": bool(REFUSAL.search(text)),
    }


def answers(items: list[dict], model: str | None = None, prompt: str | None = None, rerank: bool | None = None) -> list[dict]:
    """Run the pipeline on every question. None = the app's configured default."""
    rows = []
    for item in items:
        start = time.perf_counter()
        with get_conn() as conn:
            hits = search(conn, item["question"], TOP_K, rerank=rerank)
        text = generate_answer(item["question"], hits, model=model, prompt=prompt).strip()
        rows.append(score(item, text, round(time.perf_counter() - start, 1)))
    return rows


def rescore(items: list[dict]) -> list[dict]:
    saved = {r["question"]: r for r in json.loads((OUT / "evaluation.json").read_text(encoding="utf-8"))["answers"]}
    return [score(i, saved[i["question"]]["answer"], saved[i["question"]]["seconds"]) for i in items]


def share(rows: list[dict], key: str) -> str:
    n = sum(1 for r in rows if r[key])
    return f"{n}/{len(rows)} ({n / len(rows):.0%})" if rows else "-"


def to_markdown(ret: dict, rows: list[dict], n_items: int) -> str:
    ans = [r for r in rows if r["answerable"]]
    unans = [r for r in rows if not r["answerable"]]
    detected = [r for r in ans if r["answer_lang"]]
    lang_ok = sum(1 for r in detected if r["answer_lang"] == r["lang"])
    secs = [r["seconds"] for r in rows]
    hybrid_ranks = ret["hybrid + rerank" if RERANK else "hybrid"]["ranks"]
    retrieval_misses = sum(1 for r, rank in zip(ans, hybrid_ranks) if not r["fact_correct"] and not (rank and rank <= TOP_K))
    generation_misses = sum(1 for r, rank in zip(ans, hybrid_ranks) if not r["fact_correct"] and rank and rank <= TOP_K)
    lines = [
        "# Evaluation",
        "",
        f"{n_items} questions ({sum(1 for r in rows if r['lang'] == 'en')} English, {sum(1 for r in rows if r['lang'] == 'de')} German), "
        f"{len(ans)} answerable and {len(unans)} not answerable from the documents. LLM: `{LLM_MODEL}`, prompt {PROMPT_VERSION}, "
        f"top-{TOP_K} retrieval{' with re-ranking' if RERANK else ''}.",
        "",
        "## Retrieval (answerable questions)",
        "",
        f"| search | hit@{TOP_K} | 95 % CI | MRR | 95 % CI | hit@{TOP_K} English | hit@{TOP_K} German |",
        "|---|---|---|---|---|---|---|",
    ]
    for mode, m in ret.items():
        lines.append(f"| {mode} | {m['hit']:.2f} | {m['hit_ci'][0]:.2f}–{m['hit_ci'][1]:.2f} | {m['mrr']:.2f} | "
                     f"{m['mrr_ci'][0]:.2f}–{m['mrr_ci'][1]:.2f} | {m['hit_by_lang']['en']:.2f} | {m['hit_by_lang']['de']:.2f} |")
    lines += [
        "",
        "## Answers (the app's default pipeline)",
        "",
        "| metric | result |",
        "|---|---|",
        f"| correct fact in answer (answerable) | {share(ans, 'fact_correct')} |",
        f"| answer cites a source (answerable) | {share(ans, 'cited')} |",
        f"| answer in the question's language | {lang_ok}/{len(detected)} ({lang_ok / len(detected):.0%}) of answers with a detectable language |",
        f"| wrongly says \"not in the documents\" (answerable) | {share(ans, 'refused')} |",
        f"| correctly declines (unanswerable) | {share(unans, 'refused')} |",
        f"| latency per question | median {statistics.median(secs):.1f} s, max {max(secs):.1f} s |",
        "",
        "## Where the wrong answers come from",
        "",
        "| cause | questions |",
        "|---|---|",
        f"| search missed the right page (not in top {TOP_K}) | {retrieval_misses} |",
        f"| right page retrieved, but the answer is wrong | {generation_misses} |",
        f"| correct answer | {len(ans) - retrieval_misses - generation_misses} |",
        "",
        "## Every answer",
        "",
        "| # | lang | question | expected | answer | fact | cited | retrieval rank |",
        "|---|---|---|---|---|---|---|---|",
    ]
    ranks = iter(hybrid_ranks)
    for i, r in enumerate(rows, 1):
        rank = next(ranks) if r["answerable"] else None
        fact = "n/a" if r["fact_correct"] is None else ("yes" if r["fact_correct"] else "no")
        if not r["answerable"]:
            fact = "declined" if r["refused"] else "answered anyway"
        answer = r["answer"].replace("\n", " ").replace("|", "/")
        lines.append(f"| {i} | {r['lang']} | {r['question']} | {r['expected']} | {answer[:160]}{'…' if len(answer) > 160 else ''} | "
                     f"{fact} | {'yes' if r['cited'] else 'no'} | {rank if rank else ('-' if r['answerable'] else 'n/a')} |")
    return "\n".join(lines)


if __name__ == "__main__":
    items = load_items("eval/questions.jsonl")
    print("retrieval…")
    ret = retrieval(items)
    for mode, m in ret.items():
        print(f"  {mode:<16} hit@{TOP_K}={m['hit']:.3f} [{m['hit_ci'][0]:.2f}-{m['hit_ci'][1]:.2f}]  MRR={m['mrr']:.3f}  EN={m['hit_by_lang']['en']:.2f} DE={m['hit_by_lang']['de']:.2f}")
    if "--rescore" in sys.argv:
        print("re-scoring saved answers…")
        rows = rescore(items)
    else:
        print(f"answers ({len(items)} questions)…")
        rows = answers(items)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "evaluation.json").write_text(json.dumps({"retrieval": ret, "answers": rows}, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "evaluation.md").write_text(to_markdown(ret, rows, len(items)), encoding="utf-8")
    print("\n".join(to_markdown(ret, rows, len(items)).split("## Every answer")[0].splitlines()[-20:]))
    print(f"Wrote {OUT / 'evaluation.md'}")
