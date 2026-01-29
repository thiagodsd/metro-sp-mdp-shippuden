"""Graph construction and cost calculation for metro network."""

import pandas as pd
from .utils import cost_function


StationGraph = dict[str, dict[str, list[str] | tuple[float, float]]]
CostMap = dict[tuple[str, str], float]


def build_graph(data: pd.DataFrame) -> StationGraph:
    """Build graph structure from station data.

    Args:
        data: DataFrame with columns: station, neigh, lat, lon

    Returns:
        Dictionary mapping station names to their neighbors and positions
        Format: {station: {"neigh": [neighbors], "pos": (lat, lon)}}
    """
    graph = {}
    for _, row in data.iterrows():
        station = row["station"]
        neighbors_str = row["neigh"].strip("[]").replace("'", "").replace(" ", "")
        neighbors = neighbors_str.split(",") if neighbors_str else []
        position = (row["lat"], row["lon"])

        graph[station] = {"neigh": neighbors, "pos": position}

    return graph


def calculate_costs(graph: StationGraph) -> CostMap:
    """Calculate costs for all state transitions in the graph.

    Args:
        graph: Station graph from build_graph()

    Returns:
        Dictionary mapping (from_station, to_station) to cost
    """
    costs = {}
    for station in graph:
        for neighbor in graph[station]["neigh"]:
            pos_from = graph[station]["pos"]
            pos_to = graph[neighbor]["pos"]
            costs[(station, neighbor)] = cost_function(pos_from, pos_to)

    return costs
