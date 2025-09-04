from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Segment:
    """Base class for path segments."""
    length: float

    def pose_at(self, s: float) -> Tuple[float, float, float]:
        """Return (x, y, theta) at arc-length position ``s`` within the segment."""
        raise NotImplementedError


@dataclass
class Straight(Segment):
    angle: float = 0.0

    def pose_at(self, s: float) -> Tuple[float, float, float]:
        x = s * math.cos(self.angle)
        y = s * math.sin(self.angle)
        return x, y, self.angle


@dataclass
class Arc(Segment):
    radius: float
    angle: float

    def pose_at(self, s: float) -> Tuple[float, float, float]:
        theta = s / self.radius
        x = self.radius * math.sin(theta)
        y = self.radius * (1 - math.cos(theta))
        return x, y, theta


class Path2D:
    """Composite path made of straight and arc segments."""

    def __init__(self, segments: List[Segment]):
        self.segments = segments
        self.lengths = [seg.length for seg in segments]
        self.total_length = sum(self.lengths)

    def pose_at(self, s: float) -> Tuple[float, float, float]:
        if s < 0 or s > self.total_length:
            raise ValueError("s out of bounds")
        for seg in self.segments:
            if s <= seg.length:
                return seg.pose_at(s)
            s -= seg.length
        # fallback
        last = self.segments[-1]
        return last.pose_at(last.length)
