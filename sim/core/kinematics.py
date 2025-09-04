"""Kinematic utilities for gap statistics."""
from __future__ import annotations

from typing import Iterable


def gap_stats(times: Iterable[float]) -> dict:
    """Compute simple gap statistics from a series of timestamps."""
    times = list(times)
    if len(times) < 2:
        return {"count": 0, "mean": 0.0}
    gaps = [t2 - t1 for t1, t2 in zip(times, times[1:])]
    mean_gap = sum(gaps) / len(gaps)
    return {"count": len(gaps), "mean": mean_gap}
