"""Generate a deterministic, synthetic mobile-game event stream."""

from __future__ import annotations

import csv
import random
from datetime import UTC, datetime, timedelta
from pathlib import Path


FIELDNAMES = [
    "event_id",
    "user_id",
    "event_name",
    "event_ts_utc",
    "install_date_utc",
    "build",
    "platform",
    "level",
    "revenue_usd",
]


def generate_dataset(output_path: Path, seed: int = 42) -> list[dict[str, str]]:
    """Write deterministic synthetic events and return them as dictionaries."""

    rng = random.Random(seed)
    base = datetime(2026, 1, 5, 9, tzinfo=UTC)
    rows: list[dict[str, str]] = []
    event_number = 0

    def add_event(
        *,
        user_id: str,
        event_name: str,
        event_time: datetime,
        install_date: str,
        build: str,
        platform: str,
        level: int | None = None,
        revenue: float = 0.0,
    ) -> None:
        nonlocal event_number
        event_number += 1
        rows.append(
            {
                "event_id": f"EVT-{event_number:04d}",
                "user_id": user_id,
                "event_name": event_name,
                "event_ts_utc": event_time.isoformat().replace("+00:00", "Z"),
                "install_date_utc": install_date,
                "build": build,
                "platform": platform,
                "level": "" if level is None else str(level),
                "revenue_usd": f"{revenue:.2f}",
            }
        )

    for cohort_index in range(4):
        install_time = base + timedelta(days=cohort_index)
        install_date = install_time.date().isoformat()
        build = "101" if cohort_index < 2 else "102"

        for user_index in range(10):
            user_id = f"SYN-U{cohort_index}{user_index:02d}"
            platform = "ios" if user_index % 2 == 0 else "android"
            start = install_time + timedelta(minutes=user_index * 3)
            add_event(
                user_id=user_id,
                event_name="install",
                event_time=start,
                install_date=install_date,
                build=build,
                platform=platform,
            )
            add_event(
                user_id=user_id,
                event_name="level_start",
                event_time=start + timedelta(minutes=2),
                install_date=install_date,
                build=build,
                platform=platform,
                level=1,
            )

            tutorial_completed = user_index != 9
            if tutorial_completed:
                add_event(
                    user_id=user_id,
                    event_name="tutorial_complete",
                    event_time=start + timedelta(minutes=6),
                    install_date=install_date,
                    build=build,
                    platform=platform,
                    level=2,
                )

            level_20_threshold = 5 if build == "101" else 7
            reached_level_20 = tutorial_completed and user_index < level_20_threshold
            if reached_level_20:
                add_event(
                    user_id=user_id,
                    event_name="level_20_complete",
                    event_time=start + timedelta(hours=2, minutes=user_index),
                    install_date=install_date,
                    build=build,
                    platform=platform,
                    level=20,
                )

            d1_threshold = 4 if build == "101" else 6
            if user_index < d1_threshold:
                add_event(
                    user_id=user_id,
                    event_name="session_start",
                    event_time=start + timedelta(days=1, minutes=rng.randint(0, 90)),
                    install_date=install_date,
                    build=build,
                    platform=platform,
                )

            if reached_level_20 and user_index < 2:
                add_event(
                    user_id=user_id,
                    event_name="purchase",
                    event_time=start + timedelta(hours=4),
                    install_date=install_date,
                    build=build,
                    platform=platform,
                    revenue=1.99 if user_index == 0 else 4.99,
                )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)
    return rows
