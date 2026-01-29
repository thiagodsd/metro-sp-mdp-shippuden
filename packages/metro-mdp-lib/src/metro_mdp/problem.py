import pandas as pd
from .graph import build_graph, calculate_costs


class Problem:
    def __init__(self, data: pd.DataFrame, start: str, goal: str):
        self.states = build_graph(data)
        self.costs = calculate_costs(self.states)
        self.start = start
        self.goal = goal

    def is_state(self, state: str) -> bool:
        return state in self.states

    def actions(self, state: str) -> list[str]:
        if state in self.states:
            return self.states[state]["neigh"]
        return []

    def next_state(self, state: str, action: str) -> str | None:
        if action in self.actions(state):
            return action
        return None

    def is_goal_state(self, state: str) -> bool:
        return state == self.goal

    def cost(self, state: str, action: str) -> float:
        return self.costs[(state, action)]
