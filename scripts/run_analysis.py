#!/usr/bin/env python3
"""Generate synthetic data and print every decision query as Markdown."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from game_analytics import build_database, generate_dataset, run_query  # noqa: E402


def markdown_table(rows: list[dict[str, object]]) -> str:
    if not rows:
        return "_No rows_"
    headers = list(rows[0])
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    lines.extend("| " + " | ".join(str(row[key]) for key in headers) + " |" for row in rows)
    return "\n".join(lines)


def main() -> int:
    csv_path = ROOT / "data" / "derived" / "events.csv"
    generate_dataset(csv_path)
    connection = build_database(csv_path)
    for sql_path in sorted((ROOT / "sql").glob("*.sql")):
        print(f"## {sql_path.stem.replace('_', ' ').title()}\n")
        print(markdown_table(run_query(connection, sql_path)))
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
