import ast
import pandas as pd
from .utils import cost_function


def build_graph(data: pd.DataFrame) -> dict:
    graph = {}
    for _, row in data.iterrows():
        station = row["station"]
        neighbors = ast.literal_eval(row["neigh"]) if row["neigh"] else []
        position = (row["lat"], row["lon"])
        graph[station] = {"neigh": neighbors, "pos": position}
    return graph


def calculate_costs(graph: dict) -> dict:
    costs = {}
    for station in graph:
        for neighbor in graph[station]["neigh"]:
            pos_from = graph[station]["pos"]
            pos_to = graph[neighbor]["pos"]
            costs[(station, neighbor)] = cost_function(pos_from, pos_to)
    return costs
