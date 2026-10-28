"""Search comparison: vector vs. keyword vs. hybrid retrieval, and what each change contributes.

Variants
  vector                    embedding similarity only
  keyword (all words)       full-text search ORing every word of the question (the original version)
  keyword (content words)   stop words removed, prefix matching for longer words
  hybrid (all words)        RRF of vector + keyword (all words)
  hybrid (content words)    RRF of vector + keyword (content words)
  hybrid + dedupe           as above, duplicate passages (same rule in both documents) removed
  hybrid kw x0.5 / x0.25    keyword results weighted 0.5 / 0.25 in the fusion (plus dedupe)

For every question it records the rank of the first correct page within the top DEPTH results,
so failures can be split into "ranked too low" and "not retrieved at all".

Usage (from the project root, documents already ingested):  python -m experiments.search_comparison
Results: experiments/results/search_comparison.md and .json
"""
import json
import re
from pathlib import Path

from app.config import TOP_K
from app.db import get_conn
from app.retrieve import drop_duplicates, hybrid_search, keyword_search, keyword_terms, rrf_merge, vector_search
from eval.run_eval import answerable, first_correct_rank, load_items

DEPTH = 20
FINAL = "hybrid kw x0.5"  # the variant used by the app; its misses are listed in detail
OUT = Path("experiments/results")


def keyword_all_words(conn, query: str, k: int) -> list[dict]:
    """The original keyword search: every word of the question, ORed."""
    words = re.findall(r"\w+", query.lower())
    tsquery = " | ".join(words)
    rows = conn.execute(
        """SELECT id, doc_name, page, content, ts_rank(tsv, to_tsquery('simple', %s))
           FROM chunks WHERE tsv @@ to_tsquery('simple', %s) ORDER BY 5 DESC LIMIT %s""",
        (tsquery, tsquery, k),
    ).fetchall()
    return [{"id": r[0], "doc_name": r[1], "page": r[2], "content": r[3], "keyword_score": float(r[4])} for r in rows]


def matching_chunks(conn, tsquery: str) -> int:
    return conn.execute("SELECT count(*) FROM chunks WHERE tsv @@ to_tsquery('simple', %s)", (tsquery,)).fetchone()[0]


VARIANTS = {
    "vector": lambda c, q: vector_search(c, q, DEPTH),
    "keyword (all words)": lambda c, q: keyword_all_words(c, q, DEPTH),
    "keyword (content words)": lambda c, q: keyword_search(c, q, DEPTH),
    "hybrid (all words)": lambda c, q: rrf_merge([vector_search(c, q, DEPTH * 4), keyword_all_words(c, q, DEPTH * 4)])[:DEPTH],
    "hybrid (content words)": lambda c, q: rrf_merge([vector_search(c, q, DEPTH * 4), keyword_search(c, q, DEPTH * 4)])[:DEPTH],
    "hybrid + dedupe": lambda c, q: drop_duplicates(hybrid_search(c, q, DEPTH * 3, keyword_weight=1.0))[:DEPTH],
    "hybrid kw x0.5": lambda c, q: drop_duplicates(hybrid_search(c, q, DEPTH * 3, keyword_weight=0.5))[:DEPTH],
    "hybrid kw x0.25": lambda c, q: drop_duplicates(hybrid_search(c, q, DEPTH * 3, keyword_weight=0.25))[:DEPTH],
}


def run() -> dict:
    items = answerable(load_items("eval/questions.jsonl"))
    rows = []
    with get_conn() as conn:
        total = conn.execute("SELECT count(*) FROM chunks").fetchone()[0]
        for item in items:
            q = item["question"]
            row = {"question": q, "expected": item["answer"], "ranks": {}, "top5": {}}
            for name, fn in VARIANTS.items():
                hits = fn(conn, q)
                row["ranks"][name] = first_correct_rank(hits, item)
                row["top5"][name] = [f"{h['doc_name'].split('_SPO')[0].replace('OTH_', '')} p.{h['page']}: {h['content'][:90]}" for h in hits[:5]]
            terms = keyword_terms(q)
            row["terms"] = terms
            row["chunks_matched"] = {
                "all words": matching_chunks(conn, " | ".join(re.findall(r"\w+", q.lower()))),
                "content words": matching_chunks(conn, " | ".join(f"{t}:*" if len(t) >= 4 else t for t in terms)) if terms else 0,
            }
            rows.append(row)
    summary = {}
    for name in VARIANTS:
        ranks = [r["ranks"][name] for r in rows]
        top = [x for x in ranks if x and x <= TOP_K]
        summary[name] = {
            f"hit@{TOP_K}": round(len(top) / len(ranks), 3),
            f"mrr@{TOP_K}": round(sum(1 / x for x in top) / len(ranks), 3),
            f"found@{DEPTH}": round(sum(1 for x in ranks if x) / len(ranks), 3),
        }
    return {"k": TOP_K, "depth": DEPTH, "total_chunks": total, "summary": summary, "questions": rows}


def fmt(rank) -> str:
    return "-" if rank is None else str(rank)


def to_markdown(d: dict) -> str:
    k, depth, rows = d["k"], d["depth"], d["questions"]
    out = [
        "# Search comparison",
        "",
        f"{len(rows)} questions, {d['total_chunks']} chunks. hit@{k} / MRR@{k} use the top {k}; "
        f"found@{depth} = a correct page anywhere in the top {depth}.",
        "",
        f"| variant | hit@{k} | MRR@{k} | found@{depth} |",
        "|---|---|---|---|",
    ]
    for name, s in d["summary"].items():
        out.append(f"| {name} | {s[f'hit@{k}']:.2f} | {s[f'mrr@{k}']:.2f} | {s[f'found@{depth}']:.2f} |")
    cols = list(d["summary"])
    out += ["", f"## Rank of the first correct page (- = not in top {depth})", "",
            "| # | question | " + " | ".join(cols) + " |", "|---|---|" + "---|" * len(cols)]
    for i, r in enumerate(rows, 1):
        out.append(f"| {i} | {r['question']} | " + " | ".join(fmt(r["ranks"][c]) for c in cols) + " |")

    out += ["", "## Keyword noise: chunks matched by the keyword query", "",
            f"| # | content words used | chunks matched (all words) | chunks matched (content words) |", "|---|---|---|---|"]
    for i, r in enumerate(rows, 1):
        out.append(f"| {i} | {', '.join(r['terms'])} | {r['chunks_matched']['all words']} of {d['total_chunks']} | "
                   f"{r['chunks_matched']['content words']} of {d['total_chunks']} |")

    def better(a: str, b: str):
        res = []
        for i, r in enumerate(rows, 1):
            ra, rb = r["ranks"][a] or 99, r["ranks"][b] or 99
            if ra < rb:
                res.append((i, r, ra, rb))
        return res

    out += ["", "## Where keyword search beats vector search", ""]
    for i, r, ra, rb in better("keyword (content words)", "vector"):
        out.append(f"- Q{i} *{r['question']}*: keyword rank {fmt(r['ranks']['keyword (content words)'])}, "
                   f"vector rank {fmt(r['ranks']['vector'])} (terms: {', '.join(r['terms'])})")
    out += ["", "## Where vector search beats keyword search", ""]
    for i, r, ra, rb in better("vector", "keyword (content words)"):
        out.append(f"- Q{i} *{r['question']}*: vector rank {fmt(r['ranks']['vector'])}, "
                   f"keyword rank {fmt(r['ranks']['keyword (content words)'])} (terms: {', '.join(r['terms'])})")

    final = FINAL
    out += ["", f"## Questions still outside the top {k} ({final})", ""]
    for i, r in enumerate(rows, 1):
        if not r["ranks"][final] or r["ranks"][final] > k:
            out += [f"### Q{i}: {r['question']}", f"Expected: {r['expected']}  ",
                    f"Correct page rank: vector {fmt(r['ranks']['vector'])}, keyword {fmt(r['ranks']['keyword (content words)'])}, "
                    f"{final} {fmt(r['ranks'][final])}", "", "Top 5 retrieved:"]
            out += [f"{j}. {t}" for j, t in enumerate(r["top5"][final], 1)]
            out.append("")
    return "\n".join(out)


if __name__ == "__main__":
    data = run()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "search_comparison.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "search_comparison.md").write_text(to_markdown(data), encoding="utf-8")
    for name, s in data["summary"].items():
        print(f"{name:<26} " + "  ".join(f"{m}={v:.3f}" for m, v in s.items()))
    print(f"Wrote {OUT / 'search_comparison.md'}")
