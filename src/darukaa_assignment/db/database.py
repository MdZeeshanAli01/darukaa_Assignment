from __future__ import annotations

import sqlite3
from pathlib import Path

from darukaa_assignment.config import DATABASE_PATH


def get_connection() -> sqlite3.Connection:
    Path(DATABASE_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS land_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                region TEXT,
                soc REAL,
                ph REAL,
                rainfall REAL,
                temperature REAL,
                land_use TEXT,
                species_richness REAL,
                moisture REAL,
                pollution REAL,
                deforestation_rate REAL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE,
                context TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                recommendation TEXT,
                source_title TEXT,
                source_url TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def seed_sample_metrics() -> None:
    with get_connection() as conn:
        sample_rows = [
            (
                "Semi-arid Plains",
                0.8,
                6.3,
                480,
                28,
                "monoculture wheat",
                42,
                18,
                0.3,
                0.45,
            ),
            (
                "Mixed Cropping Zone",
                1.6,
                6.9,
                820,
                24,
                "mixed cropping",
                71,
                35,
                0.22,
                0.12,
            ),
            (
                "Forest Edge",
                2.4,
                6.8,
                1100,
                22,
                "agroforestry",
                88,
                41,
                0.18,
                0.08,
            ),
            (
                "River Basin",
                1.9,
                7.1,
                950,
                25,
                "agroforestry + cover crops",
                82,
            37,
                0.21,
                0.10,
            ),
        ]

        conn.execute("SELECT COUNT(*) FROM land_metrics")
        if conn.execute("SELECT COUNT(*) FROM land_metrics").fetchone()[0] == 0:
            conn.executemany(
                """
                INSERT INTO land_metrics (
                    region,
                    soc,
                    ph,
                    rainfall,
                    temperature,
                    land_use,
                    species_richness,
                    moisture,
                    pollution,
                    deforestation_rate
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                sample_rows,
            )
            conn.commit()


init_db()
seed_sample_metrics()

