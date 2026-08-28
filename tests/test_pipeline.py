from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from game_analytics import build_database, generate_dataset, run_query  # noqa: E402


class AnalyticsPipelineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.csv_path = Path(self.temp_dir.name) / "events.csv"
        self.rows = generate_dataset(self.csv_path)
        self.connection = build_database(self.csv_path)

    def tearDown(self) -> None:
        self.connection.close()
        self.temp_dir.cleanup()

    def test_dataset_is_deterministic(self) -> None:
        second_path = Path(self.temp_dir.name) / "events-2.csv"
        self.assertEqual(self.rows, generate_dataset(second_path))

    def test_event_ids_are_unique(self) -> None:
        quality = run_query(self.connection, ROOT / "sql" / "01_data_quality.sql")[0]
        self.assertEqual(quality["total_events"], quality["unique_event_ids"])

    def test_funnel_is_monotonic(self) -> None:
        funnel = run_query(self.connection, ROOT / "sql" / "02_funnel.sql")
        counts = [int(row["users"]) for row in funnel]
        self.assertEqual(counts, sorted(counts, reverse=True))

    def test_build_comparison_has_two_builds(self) -> None:
        rows = run_query(self.connection, ROOT / "sql" / "04_build_comparison.sql")
        self.assertEqual([row["build"] for row in rows], ["101", "102"])

    def test_no_real_user_ids_are_generated(self) -> None:
        self.assertTrue(all(row["user_id"].startswith("SYN-") for row in self.rows))


if __name__ == "__main__":
    unittest.main()
