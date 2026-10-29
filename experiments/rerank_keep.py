"""Re-ranking experiment (retrieval only, no LLM): how many of the original top hybrid results to keep.

keep = 0 is pure cross-encoder ranking; keep = n always keeps the first n hybrid results in the top k,
because the cross-encoder ranks flattened table rows (module credits, exam types) too low.

Usage (from the project root):  python -m experiments.rerank_keep
Results: experiments/results/rerank_keep.md
"""
from pathlib import Path

from app.config import RERANK_CANDIDATES, TOP_K
from app.db import get_conn
from app.rerank import rerank
from app.retrieve import search
from eval.run_eval import answerable, first_correct_rank, load_items

KEEPS = [0, 1, 2, 3]
OUT = Path("experiments/results")


def metrics(ranks: list[int | None]) -> tuple[float, float]:
    top = [r for r in ranks if r and r <= TOP_K]
    return len(top) / len(ranks), sum(1 / r for r in top) / len(ranks)


if __name__ == "__main__":
    items = answerable(load_items("eval/questions.jsonl"))
    with get_conn() as conn:
        candidates = [search(conn, i["question"], RERANK_CANDIDATES, "hybrid", rerank=False) for i in items]
    rows = {"hybrid (no re-ranking)": [first_correct_rank(c[:TOP_K], i) for c, i in zip(candidates, items)]}
    for keep in KEEPS:
        rows[f"re-rank, keep top {keep}"] = [first_correct_rank(rerank(i["question"], c, TOP_K, keep), i) for c, i in zip(candidates, items)]
    lines = ["# Re-ranking: keeping the top hybrid results", "",
             f"{len(items)} answerable questions, {RERANK_CANDIDATES} hybrid candidates re-ranked by the cross-encoder, top {TOP_K} kept.", "",
             f"| setup | hit@{TOP_K} | MRR |", "|---|---|---|"]
    for name, ranks in rows.items():
        hit, mrr = metrics(ranks)
        lines.append(f"| {name} | {hit:.2f} | {mrr:.2f} |")
        print(f"{name:<26} hit@{TOP_K}={hit:.3f} MRR={mrr:.3f}")
    names = list(rows)
    lines += ["", "| # | question | " + " | ".join(names) + " |", "|---|---|" + "---|" * len(names)]
    for n, item in enumerate(items):
        lines.append(f"| {n + 1} | {item['question']} | " + " | ".join(str(rows[c][n] or "-") for c in names) + " |")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "rerank_keep.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT / 'rerank_keep.md'}")
