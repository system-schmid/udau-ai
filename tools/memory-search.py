#!/usr/bin/env python3
"""
UDAU Memory Search — tools/memory-search.py

Query the UDAU Chroma vector index for content semantically related to a topic.
Returns top-N ranked chunks with source paths and relevance scores.

Usage:
    python3 tools/memory-search.py "your query here" [--n 5] [--json]
    udau-search "your query here"   (if symlinked or aliased)

Options:
    --n N       Number of results to return (default: 5)
    --json      Output raw JSON instead of formatted text
    --filter    Filter by path prefix, e.g. --filter proposals/

Requirements:
    Chroma index must exist: run tools/memory-index.py first.
    pip install chromadb
    Ollama running locally with nomic-embed-text pulled.

Author: Kess — 2026-07-04
Proposal: 039 (Thread 041)
"""

import argparse
import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
INDEX_DIR = REPO_ROOT / "state" / "chroma-index"
OLLAMA_BASE = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
EMBED_MODEL = os.environ.get("UDAU_EMBED_MODEL", "nomic-embed-text")
COLLECTION_NAME = "udau-workspace"


def get_embedding(text: str) -> list[float]:
    import urllib.request
    payload = json.dumps({"model": EMBED_MODEL, "prompt": text}).encode()
    req = urllib.request.Request(
        f"{OLLAMA_BASE}/api/embeddings",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read())
    return result["embedding"]


def search(query: str, n: int = 5, path_filter: str = None) -> list[dict]:
    """
    Run a semantic search and return results as list of dicts:
    [{ source, chunk_idx, score, text }]
    """
    if not INDEX_DIR.exists():
        print(
            "Error: No index found. Run tools/memory-index.py first.",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        import chromadb
    except ImportError:
        print("Error: chromadb not installed. Run: pip install chromadb", file=sys.stderr)
        sys.exit(1)

    client = chromadb.PersistentClient(path=str(INDEX_DIR))
    collection = client.get_collection(name=COLLECTION_NAME)

    if collection.count() == 0:
        print("Error: Index is empty. Run tools/memory-index.py first.", file=sys.stderr)
        sys.exit(1)

    query_emb = get_embedding(query)

    where = None
    if path_filter:
        # Chroma doesn't support prefix matching natively, so we fetch more and filter
        n_fetch = min(n * 10, collection.count())
    else:
        n_fetch = min(n, collection.count())

    results = collection.query(
        query_embeddings=[query_emb],
        n_results=n_fetch,
        include=["documents", "metadatas", "distances"],
    )

    hits = []
    docs = results["documents"][0]
    metas = results["metadatas"][0]
    distances = results["distances"][0]

    for doc, meta, dist in zip(docs, metas, distances):
        source = meta.get("source", "unknown")
        if path_filter and not source.startswith(path_filter):
            continue
        # Chroma cosine distance → similarity score (0=identical, 2=opposite)
        # Convert to 0–1 score: 1 - dist/2
        score = round(1.0 - dist / 2.0, 4)
        hits.append({
            "source": source,
            "chunk": meta.get("chunk", 0),
            "score": score,
            "text": doc,
        })
        if len(hits) >= n:
            break

    return hits


def format_results(hits: list[dict], query: str) -> str:
    lines = [f'Search: "{query}"', f"Results: {len(hits)}", ""]
    for i, hit in enumerate(hits, 1):
        lines.append(f"--- [{i}] {hit['source']} (chunk {hit['chunk']}) | score: {hit['score']:.4f}")
        # Indent the text block
        text_preview = hit["text"]
        if len(text_preview) > 500:
            text_preview = text_preview[:497] + "..."
        for line in text_preview.split("\n"):
            lines.append("  " + line)
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UDAU semantic memory search")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--n", type=int, default=5, help="Number of results (default: 5)")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Output JSON")
    parser.add_argument("--filter", dest="path_filter", default=None,
                        help="Filter results by path prefix (e.g. proposals/)")
    args = parser.parse_args()

    hits = search(args.query, n=args.n, path_filter=args.path_filter)

    if args.json_output:
        print(json.dumps(hits, indent=2))
    else:
        print(format_results(hits, args.query))
