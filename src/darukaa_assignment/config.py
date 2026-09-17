from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_PATH = os.getenv("DATABASE_PATH", str(BASE_DIR / "data" / "darukaa.db"))
VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", str(BASE_DIR / "data" / "vector_store"))
MODEL_NAME = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
LLM_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

REQUIRED_METRIC_FIELDS = {
    "soc",
    "ph",
    "rainfall",
    "land_use",
    "region",
}
