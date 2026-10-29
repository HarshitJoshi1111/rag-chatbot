"""Answer quality experiment: what does each change contribute?

  1. baseline       llama3.2 (3B), prompt v1, hybrid search            (the Day 1 pipeline)
  2. prompt v2      llama3.2 (3B), prompt v2, hybrid search
  3. bigger model   qwen2.5:7b,    prompt v2, hybrid search
  4. + re-ranking   qwen2.5:7b,    prompt v2, hybrid search + cross-encoder re-ranking

One change at a time, all on eval/questions.jsonl, scored with the checks in eval/report.py.
Needs the models pulled in Ollama:  ollama pull llama3.2 && ollama pull qwen2.5:7b

Usage (from the project root):  python -m experiments.answer_quality
Results: experiments/results/answer_quality.md and .json
"""
import json
import statistics
import subprocess
from pathlib import Path

from app.config import TOP_K
from eval.report import answers
from eval.run_eval import answerable, evaluate, load_items

OUT = Path("experiments/results")
VARIANTS = [
    ("1. baseline", {"model": "llama3.2", "prompt": "v1", "rerank": False}),
    ("2. prompt v2", {"model": "llama3.2", "prompt": "v2", "rerank": False}),
    ("3. bigger model", {"model": "qwen2.5:7b", "prompt": "v2", "rerank": False}),
    ("4. + re-ranking", {"model": "qwen2.5:7b", "prompt": "v2", "rerank": True}),
]


def summarize(rows: list[dict], ranks: list[int | None]) -> dict:
    ans = [r for r in rows if r["answerable"]]
    unans = [r for r in rows if not r["answerable"]]
    detected = [r for r in ans if r["answer_lang"]]
    retrieved = [bool(x and x <= TOP_K) for x in ranks]
    return {
        "fact_correct": sum(1 for r in ans if r["fact_correct"]),
        "answerable": len(ans),
        "cited": sum(1 for r in ans if r["cited"]),
        "language_ok": sum(1 for r in detected if r["answer_lang"] == r["lang"]),
        "language_detected": len(detected),
        "wrongly_refused": sum(1 for r in ans if r["refused"]),
        "declined": sum(1 for r in unans if r["refused"]),
        "unanswerable": len(unans),
        "retrieval_misses": sum(1 for r, ok in zip(ans, retrieved) if not r["fact_correct"] and not ok),
        "generation_misses": sum(1 for r, ok in zip(ans, retrieved) if not r["fact_correct"] and ok),
        "median_seconds": statistics.median(r["seconds"] for r in rows),
    }


def to_markdown(results: list[dict], items: list[dict]) -> str:
    pct = lambda a, b: f"{a}/{b} ({a / b:.0%})" if b else "-"
    names = [r["name"] for r in results]
    lines = [
        "# Answer quality experiment",
        "",
        f"{len(items)} questions ({len(answerable(items))} answerable). One change per row; scoring as in eval/report.py.",
        "",
        "| variant | model | prompt | re-rank | correct fact | cited | right language | wrongly declines | declines unanswerable | search misses | answer misses | median s |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in results:
        s, c = r["summary"], r["config"]
        lines.append(
            f"| {r['name']} | {c['model']} | {c['prompt']} | {'yes' if c['rerank'] else 'no'} | {pct(s['fact_correct'], s['answerable'])} | "
            f"{pct(s['cited'], s['answerable'])} | {pct(s['language_ok'], s['language_detected'])} | {s['wrongly_refused']} | "
            f"{s['declined']}/{s['unanswerable']} | {s['retrieval_misses']} | {s['generation_misses']} | {s['median_seconds']:.1f} |"
        )
    lines += ["", "## Correct fact per question", "", "| # | question | " + " | ".join(names) + " |",
              "|---|---|" + "---|" * len(names)]
    for i, item in enumerate(items):
        cells = []
        for r in results:
            row = r["answers"][i]
            if row["answerable"]:
                cells.append("yes" if row["fact_correct"] else "no")
            else:
                cells.append("declined" if row["refused"] else "answered")
        lines.append(f"| {i + 1} | {item['question']} | " + " | ".join(cells) + " |")
    lines += ["", "## Answers of the last variant", ""]
    for i, row in enumerate(results[-1]["answers"], 1):
        lines.append(f"{i}. **{row['question']}**  \n   expected: {row['expected']}  \n   answer: {row['answer'].replace(chr(10), ' ')}")
    return "\n".join(lines)


if __name__ == "__main__":
    items = load_items("eval/questions.jsonl")
    results = []
    previous_model = None
    for name, cfg in VARIANTS:
        print(f"=== {name}: {cfg}", flush=True)
        if previous_model and previous_model != cfg["model"]:
            # Free the memory of the previous model first (two LLMs at once do not fit in 8 GB RAM)
            subprocess.run(["ollama", "stop", previous_model], check=False)
        previous_model = cfg["model"]
        ranks = evaluate(items, "hybrid", TOP_K, cfg["rerank"])["ranks"]
        rows = answers(items, **cfg)
        summary = summarize(rows, ranks)
        print("    " + ", ".join(f"{k}={v}" for k, v in summary.items()), flush=True)
        results.append({"name": name, "config": cfg, "summary": summary, "ranks": ranks, "answers": rows})
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / "answer_quality.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "answer_quality.md").write_text(to_markdown(results, items), encoding="utf-8")
    print(f"Wrote {OUT / 'answer_quality.md'}")
