from __future__ import annotations

import json
from pathlib import Path

from darukaa_assignment.knowledge.sources import SOURCE_CATALOG

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "knowledge_base"


def ensure_knowledge_base_dirs() -> None:
    (DATA_DIR / "pdfs").mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "json").mkdir(parents=True, exist_ok=True)


def save_source_manifest() -> None:
    ensure_knowledge_base_dirs()
    manifest_path = DATA_DIR / "json" / "source_manifest.json"
    payload = [
        {
            "title": source.title,
            "source_org": source.source_org,
            "url": source.url,
            "year": source.year,
            "domain": source.domain,
            "doc_type": source.doc_type,
        }
        for source in SOURCE_CATALOG
    ]
    manifest_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
