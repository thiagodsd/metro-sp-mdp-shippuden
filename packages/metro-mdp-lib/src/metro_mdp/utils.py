"""Utility functions for metro MDP system."""

import pandas as pd
from thefuzz import fuzz


def fuzz_string(station: str, series: pd.Series) -> str:
    """Find the closest matching station name using fuzzy string matching.

    Args:
        station: Target station name to match
        series: Series of valid station names

    Returns:
        Best matching station name from the series
    """
    matches = series.apply(lambda x: (x, fuzz.token_sort_ratio(x, station))).values
    best_match = sorted(matches, key=lambda t: t[1], reverse=True)[0]
    return best_match[0]


def cost_function(pos1: tuple[float, float], pos2: tuple[float, float]) -> float:
    """Calculate Euclidean distance between two positions.

    Args:
        pos1: First position as (lat, lon) tuple
        pos2: Second position as (lat, lon) tuple

    Returns:
        Euclidean distance between the two positions
    """
    y1, x1 = pos1
    y2, x2 = pos2
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
