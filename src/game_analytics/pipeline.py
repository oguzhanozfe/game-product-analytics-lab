"""Load synthetic events into SQLite and execute reviewable SQL."""

from __future__ import annotations

import csv
import sqlite3
from pathlib import Path
from typing import Iterable


SCHEMA = """
CREATE TABLE events (
    event_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    event_name TEXT NOT NULL,
    event_ts_utc TEXT NOT NULL,
    install_date_utc TEXT NOT NULL,
    build TEXT NOT NULL,
    platform TEXT NOT NULL,
    level INTEGER,
    revenue_usd REAL NOT NULL
)
"""


def build_database(csv_path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    connection.execute(SCHEMA)
    with csv_path.open(encoding="utf-8", newline="") as handle:
        rows: Iterable[dict[str, str]] = csv.DictReader(handle)
        connection.executemany(
            """
            INSERT INTO events (
                event_id, user_id, event_name, event_ts_utc,
                install_date_utc, build, platform, level, revenue_usd
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                (
                    row["event_id"],
                    row["user_id"],
                    row["event_name"],
                    row["event_ts_utc"],
                    row["install_date_utc"],
                    row["build"],
                    row["platform"],
                    int(row["level"]) if row["level"] else None,
                    float(row["revenue_usd"]),
                )
                for row in rows
            ),
        )
    return connection


def run_query(connection: sqlite3.Connection, sql_path: Path) -> list[dict[str, object]]:
    cursor = connection.execute(sql_path.read_text(encoding="utf-8"))
    return [dict(row) for row in cursor.fetchall()]
