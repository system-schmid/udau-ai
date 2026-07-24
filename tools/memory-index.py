#!/usr/bin/env python3
"""
UDAU Memory Indexer — tools/memory-index.py

Indexes UDAU workspace content (conversations/, proposals/, state/) into a
local Chroma vector store using Ollama's nomic-embed-text embeddings.

Usage:
    python3 tools/memory-index.py [--rebuild]

    --rebuild   Drop and rebuild the collection from scratch.
                By default, only new/modified files are re-indexed.

Requirements:
    pip install chromadb
    Ollama running locally with nomic-embed-text pulled:
        ollama pull nomic-embed-text

Index location:
    state/chroma-index/   (local, gitignored)

Author: Kess — 2026-07-04
Proposal: 039 (Thread 041)
"""

import argparse
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).parent.parent.resolve()
INDEX_DIR = REPO_ROOT / "state" / "chroma-index"
HASH_CACHE = REPO_ROOT / "state" / "chroma-file-hashes.json"
OLLAMA_BASE = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
EMBED_MODEL = os.environ.get("UDAU_EMBED_MODEL", "nomic-embed-text")
COLLECTION_NAME = "udau-workspace"

# Directories and file patterns to index
INDEX_TARGETS = [
    ("conversations", "*.md"),
    ("proposals", "*.md"),
    ("state", "*.md"),
    ("state", "*.json"),
]

# Files to always exclude (too noisy or binary)
EXCLUDE_PATTERNS = [
    "chroma-index",
    "chroma-file-hashes.json",
    "__pycache__",
    ".git",
]

# Chunking params
CHUNK_SIZE = 800      # characters per chunk (rough; split on paragraph boundaries)
CHUNK_OVERLAP = 100   # overlap between consecutive chunks


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def should_exclude(path: Path) -> bool:
    for pat in EXCLUDE_PATTERNS:
        if pat in str(path):
            return True
    return False


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def load_hash_cache() -> dict:
    if HASH_CACHE.exists():
        try:
            return json.loads(HASH_CACHE.read_text())
        except Exception:
            pass
    return {}


def save_hash_cache(cache: dict):
    HASH_CACHE.write_text(json.dumps(cache, indent=2))


def chunk_text(text: str, source: str) -> list[tuple[str, dict]]:
    """Split text into overlapping chunks; return (chunk_text, metadata) pairs."""
    # Prefer splitting on paragraph boundaries
    paragraphs = re.split(r"\n{2,}", text.strip())
    chunks = []
    current = ""
    chunk_idx = 0

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        if len(current) + len(para) + 2 <= CHUNK_SIZE:
            current = (current + "\n\n" + para).strip()
        else:
            if current:
                chunks.append((current, {"source": source, "chunk": chunk_idx}))
                chunk_idx += 1
                # Carry-over overlap: last ~CHUNK_OVERLAP chars of current
                overlap_start = max(0, len(current) - CHUNK_OVERLAP)
                current = current[overlap_start:].strip() + "\n\n" + para
                current = current.strip()
            else:
                # paragraph alone is too big — hard split
                for i in range(0, len(para), CHUNK_SIZE - CHUNK_OVERLAP):
                    chunk = para[i:i + CHUNK_SIZE]
                    chunks.append((chunk, {"source": source, "chunk": chunk_idx}))
                    chunk_idx += 1
                current = ""

    if current:
        chunks.append((current, {"source": source, "chunk": chunk_idx}))

    return chunks


def get_embedding(text: str) -> list[float]:
    """Call Ollama embeddings endpoint."""
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


def get_embeddings_batch(texts: list[str]) -> list[list[float]]:
    """Get embeddings for a list of texts (sequential; Ollama has no batch API)."""
    embeddings = []
    for i, text in enumerate(texts):
        if i > 0 and i % 10 == 0:
            print(f"  ... {i}/{len(texts)} embeddings done", flush=True)
        emb = get_embedding(text)
        embeddings.append(emb)
    return embeddings


def collect_files() -> list[Path]:
    """Collect all indexable files from the configured targets."""
    files = []
    for (subdir, pattern) in INDEX_TARGETS:
        target = REPO_ROOT / subdir
        if not target.exists():
            continue
        for path in target.glob(pattern):
            if path.is_file() and not should_exclude(path):
                files.append(path)
    return sorted(files)


def relative_path(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


# ---------------------------------------------------------------------------
# Main indexing logic
# ---------------------------------------------------------------------------

def build_index(rebuild: bool = False):
    import chromadb
    from chromadb.config import Settings

    INDEX_DIR.mkdir(parents=True, exist_ok=True)

    client = chromadb.PersistentClient(path=str(INDEX_DIR))

    if rebuild:
        print(f"[rebuild] Deleting existing collection '{COLLECTION_NAME}'...")
        try:
            client.delete_collection(COLLECTION_NAME)
        except Exception:
            pass
        hash_cache = {}
    else:
        hash_cache = load_hash_cache()

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    files = collect_files()
    print(f"[index] Found {len(files)} files to consider.")

    new_count = 0
    skip_count = 0
    error_count = 0

    for path in files:
        rel = relative_path(path)

        try:
            h = file_hash(path)
        except Exception as e:
            print(f"  [skip] {rel} — cannot hash: {e}")
            error_count += 1
            continue

        if not rebuild and hash_cache.get(rel) == h:
            skip_count += 1
            continue

        print(f"  [index] {rel}")

        try:
            text = path.read_text(errors="replace")
        except Exception as e:
            print(f"  [skip] {rel} — cannot read: {e}")
            error_count += 1
            continue

        chunks = chunk_text(text, rel)
        if not chunks:
            print(f"  [skip] {rel} — no content after chunking")
            skip_count += 1
            continue

        # Remove existing docs for this file before re-adding
        if not rebuild:
            try:
                existing = collection.get(where={"source": rel})
                if existing and existing["ids"]:
                    collection.delete(ids=existing["ids"])
            except Exception:
                pass

        chunk_texts = [c[0] for c in chunks]
        chunk_metas = [c[1] for c in chunks]

        try:
            embeddings = get_embeddings_batch(chunk_texts)
        except Exception as e:
            print(f"  [error] {rel} — embedding failed: {e}")
            error_count += 1
            continue

        ids = [f"{rel}::chunk{i}" for i in range(len(chunks))]
        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=chunk_texts,
            metadatas=chunk_metas,
        )

        hash_cache[rel] = h
        new_count += 1

    save_hash_cache(hash_cache)

    total_docs = collection.count()
    print(f"\n[index] Done.")
    print(f"  Files indexed (new/updated): {new_count}")
    print(f"  Files skipped (unchanged):   {skip_count}")
    print(f"  Errors:                       {error_count}")
    print(f"  Total chunks in collection:   {total_docs}")
    print(f"  Index location: {INDEX_DIR}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UDAU memory indexer")
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Drop and rebuild the index from scratch",
    )
    args = parser.parse_args()

    print(f"UDAU Memory Indexer — {EMBED_MODEL} embeddings via Ollama")
    print(f"Repo root: {REPO_ROOT}")
    print()

    build_index(rebuild=args.rebuild)
