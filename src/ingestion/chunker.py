from __future__ import annotations
import re
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config.settings import settings


def _parse_frontmatter(text: str) -> tuple[dict, str]:
    """Extract YAML frontmatter and return (metadata_dict, body_text)."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("---", 3)
    if end == -1:
        return {}, text
    fm_block = text[3:end].strip()
    body = text[end + 3:].strip()
    meta = {}
    for line in fm_block.splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            v = v.strip().strip('"')
            # Parse list values like ["finance", "clevel"]
            if v.startswith("["):
                items = re.findall(r'"([^"]+)"', v)
                meta[k.strip()] = items
            else:
                meta[k.strip()] = v
    return meta, body


def load_and_chunk(file_path: Path) -> list[tuple[str, dict]]:
    """
    Load a markdown file, parse frontmatter, split into chunks.
    Returns list of (chunk_text, raw_metadata_dict).
    access_roles is converted from list → comma-string here.
    """
    text = file_path.read_text(encoding="utf-8")
    fm, body = _parse_frontmatter(text)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        separators=["\n## ", "\n### ", "\n\n", "\n", " "],
    )
    chunks = splitter.split_text(body)

    ALL_DEPTS = ["finance", "marketing", "hr", "engineering", "clevel", "general", "employee"]

    access_roles = fm.get("access_roles", [])
    if isinstance(access_roles, str):
        access_roles = [r.strip() for r in access_roles.split(",") if r.strip()]

    dept_flags = {f"dept_{d}": (d in access_roles) for d in ALL_DEPTS}

    results = []
    for i, chunk in enumerate(chunks):
        raw_meta = {
            "doc_id":          fm.get("doc_id", file_path.stem),
            "chunk_id":        f"{fm.get('doc_id', file_path.stem)}_chunk_{i:03d}",
            "title":           fm.get("title", file_path.stem),
            "department":      fm.get("department", "general"),
            "classification":  fm.get("classification", "internal"),
            "doc_type":        fm.get("doc_type", "document"),
            "source_file":     file_path.name,
            "chunk_index":     i,
            "total_chunks":    len(chunks),
            "created_date":    fm.get("created_date", ""),
            **dept_flags,
        }
        results.append((chunk, raw_meta))
    return results
