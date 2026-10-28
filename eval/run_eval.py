"""Retrieval evaluation: does a correct page show up in the top-k results?

Usage (from the project root, after ingesting your documents):
    python -m eval.run_eval eval/questions.jsonl

Each line of the questions file is one JSON object, either with a single correct page
    {"question": "...", "doc_name": "file.pdf", "page": 12}
or with several acceptable locations (e.g. the same rule appears in two documents)
    {"question": "...", "answer": "...", "relevant": [{"doc_name": "a.pdf", "page": 3}, {"doc_name": "b.pdf", "page": 3}]}
Questions marked "answerable": false (no answer in the documents) are skipped here; eval/report.py
uses them to test whether the system declines to answer.

Metrics:
    hit@k  share of questions where a correct page is anywhere in the top k
    MRR    mean of 1/rank of the first correct hit (1.0 = always ranked first)
"""
import json
import sys

from app.config import TOP_K
from app.db import get_conn
from app.retrieve import search


def load_items(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def answerable(items: list[dict]) -> list[dict]:
    return [i for i in items if i.get("answerable", True)]


def relevant_locations(item: dict) -> list[dict]:
    return item.get("relevant") or [{"doc_name": item["doc_name"], "page": item.get("page")}]


def is_match(hit: dict, item: dict) -> bool:
    for loc in relevant_locations(item):
        if hit["doc_name"] == loc["doc_name"] and (loc.get("page") is None or hit["page"] == loc["page"]):
            return True
    return False


def first_correct_rank(results: list[dict], item: dict) -> int | None:
    return next((i for i, h in enumerate(results, start=1) if is_match(h, item)), None)


def evaluate(items: list[dict], mode: str, k: int) -> dict:
    items = answerable(items)
    ranks = []
    with get_conn() as conn:
        for item in items:
            ranks.append(first_correct_rank(search(conn, item["question"], k, mode), item))
    n = len(items)
    found = [r for r in ranks if r]
    return {
        "mode": mode,
        "k": k,
        "questions": n,
        "hit_rate": round(len(found) / n, 3),
        "mrr": round(sum(1 / r for r in found) / n, 3),
        "ranks": ranks,
    }


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "eval/questions.jsonl"
    items = load_items(path)
    if not items:
        sys.exit(f"No questions in {path}. Add one JSON object per line.")
    print(f"{'mode':<8} {'k':>3} {'hit@k':>7} {'MRR':>7}")
    for mode in ("vector", "keyword", "hybrid"):
        r = evaluate(items, mode, TOP_K)
        print(f"{r['mode']:<8} {r['k']:>3} {r['hit_rate']:>7.3f} {r['mrr']:>7.3f}")
