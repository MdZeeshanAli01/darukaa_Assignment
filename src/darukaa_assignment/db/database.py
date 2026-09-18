from __future__ import annotations

import sqlite3
from pathlib import Path

from darukaa_assignment.config import DATABASE_PATH


def get_connection() -> sqlite3.Connection:
    Path(DATABASE_PATH).parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with get_connection() as connection:
        connection.execute(
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
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE,
                context TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.execute(
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
        connection.commit()


def save_land_metrics(metrics: dict[str, object]) -> int:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO land_metrics (
                region, soc, ph, rainfall, temperature, land_use,
                species_richness, moisture, pollution, deforestation_rate
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                metrics.get("region"),
                metrics.get("soc"),
                metrics.get("ph"),
                metrics.get("rainfall"),
                metrics.get("temperature"),
                metrics.get("land_use"),
                metrics.get("species_richness"),
                metrics.get("moisture"),
                metrics.get("pollution"),
                metrics.get("deforestation_rate"),
            ),
        )
        connection.commit()
        return cursor.lastrowid or 0


def save_session(session_id: str, context: str) -> None:
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO sessions (session_id, context)
            VALUES (?, ?)
            ON CONFLICT(session_id) DO UPDATE SET context = excluded.context
            """,
            (session_id, context),
        )
        connection.commit()


def save_recommendation(
    session_id: str,
    recommendation_text: str,
    source_title: str | None = None,
    source_url: str | None = None,
) -> int:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO recommendations (session_id, recommendation, source_title, source_url)
            VALUES (?, ?, ?, ?)
            """,
            (session_id, recommendation_text, source_title, source_url),
        )
        connection.commit()
        return cursor.lastrowid or 0


init_db()
