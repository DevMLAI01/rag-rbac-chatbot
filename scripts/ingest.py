#!/usr/bin/env python3
"""Ingest data/raw/**/*.md into the Chroma vector store."""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ingestion.chunker import load_and_chunk
from src.ingestion.embedder import get_embedding_function
from config.settings import settings
import chromadb

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"


def ingest(reset: bool = False):
    client = chromadb.PersistentClient(path=settings.chroma_persist_dir)

    if reset:
        try:
            client.delete_collection(settings.chroma_collection_name)
            print(f"Deleted existing collection '{settings.chroma_collection_name}'")
        except Exception:
            pass

    collection = client.get_or_create_collection(
        name=settings.chroma_collection_name,
        metadata={"hnsw:space": "cosine"},
    )

    embed_fn = get_embedding_function()
    files = list(RAW_DIR.rglob("*.md"))
    print(f"Found {len(files)} documents in {RAW_DIR}\n")

    total_chunks = 0
    for file_path in sorted(files):
        chunks = load_and_chunk(file_path)
        if not chunks:
            continue

        texts = [c[0] for c in chunks]
        metadatas = [c[1] for c in chunks]
        ids = [m["chunk_id"] for m in metadatas]

        # Skip already-ingested chunks
        existing = set(collection.get(ids=ids)["ids"])
        new_idx = [i for i, cid in enumerate(ids) if cid not in existing]
        if not new_idx:
            print(f"  [skip] {file_path.name} — already ingested")
            continue

        new_texts = [texts[i] for i in new_idx]
        new_metas = [metadatas[i] for i in new_idx]
        new_ids   = [ids[i] for i in new_idx]

        embeddings = embed_fn.embed_documents(new_texts)
        collection.add(documents=new_texts, metadatas=new_metas, embeddings=embeddings, ids=new_ids)
        total_chunks += len(new_idx)
        print(f"  [ok] {file_path.name} — {len(new_idx)} chunks ingested")

    total_in_db = collection.count()
    print(f"\nDone — {total_chunks} new chunks added. Total in DB: {total_in_db}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest documents into Chroma")
    parser.add_argument("--reset", action="store_true", help="Wipe collection before ingesting")
    args = parser.parse_args()
    ingest(reset=args.reset)
