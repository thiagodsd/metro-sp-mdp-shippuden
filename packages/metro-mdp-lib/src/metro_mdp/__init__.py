import pandas as pd
from .problem import Problem
from .search import depth_first_search
from .utils import fuzz_string

__version__ = "0.1.0"

__all__ = [
    "solve_route",
    "Problem",
    "depth_first_search",
    "fuzz_string",
]


def solve_route(data: pd.DataFrame, origin: str, destination: str) -> list[str]:
    problem = Problem(data, origin, destination)
    solution_node = depth_first_search(problem)

    if solution_node is None:
        return []

    stations = []
    node = solution_node
    while node is not None:
        stations.append(node.state)
        node = node.parent

    return stations[::-1]
