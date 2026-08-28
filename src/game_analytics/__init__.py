"""Synthetic game-product analytics helpers."""

from .generate_data import generate_dataset
from .pipeline import build_database, run_query

__all__ = ["build_database", "generate_dataset", "run_query"]
