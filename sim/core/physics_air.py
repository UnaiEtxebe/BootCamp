"""Simple air-deck speed profile integrator."""
from __future__ import annotations

import numpy as np


def air_speed_profile(distance: float, v0: float, thrust: float, drag_coeff: float) -> float:
    """Very small placeholder model returning a derated speed.

    The result is v0 reduced by drag over the given distance. Parameters are
    simplified and do not reflect real physics.
    """
    decel = drag_coeff * distance
    return max(v0 - decel + thrust, 0.0)
