"""Chunk size experiment: how do text cleaning, chunk size and overlap change retrieval quality?

For every configuration the script
  1. re-ingests all documents in data/ with that chunk size and overlap,
  2. evaluates retrieval (vector-only and hybrid) on eval/questions.jsonl,
  3. asks a few questions end-to-end and stores the answers.
At the end it re-ingests with the configured default (CHUNK_SIZE / CHUNK_OVERLAP in .env).

Usage (from the project root):  python -m experiments.chunk_size
Results: experiments/results/chunk_size.md and chunk_size.json
"""
import json
import statistics
import time
from pathlib import Path

from app.config import CHUNK_OVERLAP, CHUNK_SIZE, DATA_DIR, TOP_K
from app.db import get_conn
from app.ingest import SUPPORTED, chunk_document, ingest_file
from app.llm import generate_answer
from app.retrieve import search
from eval.run_eval import evaluate, load_items

CONFIGS = [  # (chunk_size, overlap, clean_text); overlap = 15 % of size
    (800, 120, False),  # baseline: the Day 1 setup, raw PDF text
    (400, 60, True),
    (800, 0, True),
    (800, 120, True),
    (1200, 180, True),
]
ANSWER_QUESTIONS = [0, 2, 4, 8, 14]  # indices into the question file, answered end-to-end per config
SAMPLE_DOC, SAMPLE_PAGE = "OTH_Informatik_SPO_2024.pdf", 3  # page whose chunks are shown in the report
OUT = Path("experiments/results")


def documents() -> list[Path]:
    return sorted(p for p in Path(DATA_DIR).iterdir() if p.suffix.lower() in SUPPORTED)


def refresh_indexes(conn) -> None:
    """Deleted rows stay in the HNSW graph until it is rebuilt, which makes approximate search miss
    live rows after repeated re-ingestion. Rebuild the indexes so every configuration starts clean."""
    conn.execute("REINDEX TABLE chunks")
    conn.execute("VACUUM ANALYZE chunks")


def reingest(size: int, overlap: int, clean: bool = True) -> dict:
    start = time.perf_counter()
    lengths = []
    with get_conn() as conn:
        conn.execute("DELETE FROM chunks")
        for doc in documents():
            ingest_file(conn, doc, size, overlap, clean)
            lengths += [len(c["content"]) for c in chunk_document(doc, size, overlap, clean)]
        refresh_indexes(conn)
    return {
        "chunks": len(lengths),
        "avg_chars": round(statistics.mean(lengths)),
        "ingest_seconds": round(time.perf_counter() - start, 1),
    }


def sample_chunks(size: int, overlap: int, clean: bool) -> list[str]:
    doc = Path(DATA_DIR) / SAMPLE_DOC
    return [c["content"] for c in chunk_document(doc, size, overlap, clean) if c["page"] == SAMPLE_PAGE]


def answer(question: str) -> dict:
    start = time.perf_counter()
    with get_conn() as conn:
        hits = search(conn, question, TOP_K, "hybrid")
    text = generate_answer(question, hits)
    return {
        "answer": text.strip(),
        "sources": [f"{h['doc_name'].split('_SPO')[0]} p.{h['page']}" for h in hits],
        "seconds": round(time.perf_counter() - start, 1),
    }


def run() -> dict:
    items = load_items("eval/questions.jsonl")
    results = []
    for size, overlap, clean in CONFIGS:
        print(f"\n=== chunk_size={size} overlap={overlap} clean={clean}")
        row = {"chunk_size": size, "overlap": overlap, "clean": clean, **reingest(size, overlap, clean)}
        print(f"    {row['chunks']} chunks, avg {row['avg_chars']} chars, ingest {row['ingest_seconds']} s")
        for mode in ("vector", "hybrid"):
            r = evaluate(items, mode, TOP_K)
            row[mode] = r
            print(f"    {mode:<6} hit@{TOP_K}={r['hit_rate']:.3f}  MRR={r['mrr']:.3f}")
        row["answers"] = [{"question": items[i]["question"], "expected": items[i]["answer"], **answer(items[i]["question"])}
                          for i in ANSWER_QUESTIONS]
        row["sample_chunks"] = sample_chunks(size, overlap, clean)
        results.append(row)
    print(f"\n=== restoring default chunk_size={CHUNK_SIZE} overlap={CHUNK_OVERLAP}")
    reingest(CHUNK_SIZE, CHUNK_OVERLAP)
    repeat = {mode: evaluate(items, mode, TOP_K) for mode in ("vector", "hybrid")}
    print("    repeat check: " + "  ".join(f"{m} hit@{TOP_K}={r['hit_rate']:.3f} MRR={r['mrr']:.3f}" for m, r in repeat.items()))
    return {"questions": items, "k": TOP_K, "results": results, "repeat_check": {m: {k: r[k] for k in ("hit_rate", "mrr")} for m, r in repeat.items()}}


def to_markdown(data: dict) -> str:
    k, items, res = data["k"], data["questions"], data["results"]
    name = lambda r: f"{r['chunk_size']} / {r['overlap']}" + ("" if r["clean"] else " raw")
    lines = [
        "# Chunk size experiment",
        "",
        "Configurations are chunk size / overlap in characters. \"raw\" = PDF text without cleanup; "
        "all other rows use clean_text() (page headers, sentence numbers and line-break hyphens removed).",
        "",
        f"{len(items)} questions in English and German, top-{k} retrieval. "
        f"A hit = a correct page among the top {k} results.",
        "",
        f"| size / overlap | chunks | avg chars | vector hit@{k} | vector MRR | hybrid hit@{k} | hybrid MRR | ingest s |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in res:
        v, h = r["vector"], r["hybrid"]
        lines.append(f"| {name(r)} | {r['chunks']} | {r['avg_chars']} | {v['hit_rate']:.2f} | {v['mrr']:.2f} | "
                     f"{h['hit_rate']:.2f} | {h['mrr']:.2f} | {r['ingest_seconds']} |")
    lines += ["", "## Rank of the first correct page per question (hybrid; - = not in top results)", "",
              "| # | question | " + " | ".join(name(r) for r in res) + " |",
              "|---|---|" + "---|" * len(res)]
    for i, q in enumerate(items):
        ranks = [r["hybrid"]["ranks"][i] or "-" for r in res]
        lines.append(f"| {i + 1} | {q['question']} | " + " | ".join(str(x) for x in ranks) + " |")
    lines += ["", "## End-to-end answers (hybrid search + LLM)", ""]
    for j, idx in enumerate(ANSWER_QUESTIONS):
        q = items[idx]
        lines += [f"### {q['question']}", f"Expected: {q['answer']}", ""]
        for r in res:
            a = r["answers"][j]
            lines.append(f"- **{name(r)}** ({a['seconds']} s): {a['answer'].replace(chr(10), ' ')}  \n  sources: {', '.join(a['sources'])}")
        lines.append("")
    lines += [f"## How the chunks of {SAMPLE_DOC} page {SAMPLE_PAGE} look", ""]
    for r in res:
        lines.append(f"### {name(r)}: {len(r['sample_chunks'])} chunks on this page")
        for c in r["sample_chunks"][:3]:
            lines.append(f"> {c[:300]}{'…' if len(c) > 300 else ''}")
            lines.append(">")
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    data = run()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "chunk_size.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "chunk_size.md").write_text(to_markdown(data), encoding="utf-8")
    print(f"\nWrote {OUT / 'chunk_size.md'}")
