import ast
import pandas as pd
from thefuzz import fuzz
from metro_mdp._rust import depth_first_search as _rust_dfs

__version__ = "0.1.0"

__all__ = [
    "solve_route",
    "fuzz_string",
]


def fuzz_string(station: str, series: pd.Series) -> str:
    """Fuzzy match station name against series."""
    matches = series.apply(lambda x: (x, fuzz.token_sort_ratio(x, station))).values
    best_match = sorted(matches, key=lambda t: t[1], reverse=True)[0]
    return best_match[0]


def solve_route(data: pd.DataFrame, origin: str, destination: str) -> list[str]:
    """Find route between two stations using rust-powered DFS."""
    # build graph and positions from dataframe
    graph = {}
    positions = {}

    for _, row in data.iterrows():
        station = row["station"]
        neighbors = ast.literal_eval(row["neigh"]) if row["neigh"] else []
        position = (float(row["lat"]), float(row["lon"]))
        graph[station] = neighbors
        positions[station] = position

    # call rust dfs
    result = _rust_dfs(graph, positions, origin, destination)

    return result if result is not None else []
