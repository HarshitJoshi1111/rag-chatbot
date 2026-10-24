"""Retrieval evaluation: does the right page show up in the top-k results?

Usage (from the project root, after ingesting your documents):
    python -m eval.run_eval eval/questions.jsonl

Each line of the questions file:
    {"question": "...", "doc_name": "file.pdf", "page": 12}

Metrics:
    hit@k  share of questions where the expected page is anywhere in the top k
    MRR    mean of 1/rank of the first correct hit (1.0 = always ranked first)
"""
import json
import sys

from app.config import TOP_K
from app.db import get_conn
from app.retrieve import search


def is_match(hit: dict, item: dict) -> bool:
    if hit["doc_name"] != item["doc_name"]:
        return False
    return item.get("page") is None or hit["page"] == item["page"]


def evaluate(items: list[dict], mode: str, k: int) -> dict:
    hits, rr = 0, 0.0
    with get_conn() as conn:
        for item in items:
            results = search(conn, item["question"], k, mode)
            rank = next((i for i, h in enumerate(results, start=1) if is_match(h, item)), None)
            if rank:
                hits += 1
                rr += 1 / rank
    n = len(items)
    return {"mode": mode, "k": k, "questions": n, "hit_rate": round(hits / n, 3), "mrr": round(rr / n, 3)}


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "eval/questions.jsonl"
    with open(path, encoding="utf-8") as f:
        items = [json.loads(line) for line in f if line.strip()]
    if not items:
        sys.exit(f"No questions in {path}. Add one JSON object per line.")
    print(f"{'mode':<8} {'k':>3} {'hit@k':>7} {'MRR':>7}")
    for mode in ("vector", "hybrid"):
        r = evaluate(items, mode, TOP_K)
        print(f"{r['mode']:<8} {r['k']:>3} {r['hit_rate']:>7.3f} {r['mrr']:>7.3f}")
