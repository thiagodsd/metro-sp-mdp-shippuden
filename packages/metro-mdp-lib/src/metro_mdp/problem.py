"""MDP Problem definition for metro route planning."""

import pandas as pd
from .graph import StationGraph, CostMap, build_graph, calculate_costs


class Problem:
    """Markov Decision Process problem for metro routing.

    Attributes:
        states: Graph of stations with neighbors and positions
        costs: Cost map for all transitions
        start: Starting station name
        goal: Goal station name
    """

    def __init__(self, data: pd.DataFrame, start: str, goal: str):
        """Initialize MDP problem.

        Args:
            data: DataFrame with station data (station, neigh, lat, lon columns)
            start: Starting station name
            goal: Goal station name
        """
        self.states: StationGraph = build_graph(data)
        self.costs: CostMap = calculate_costs(self.states)
        self.start = start
        self.goal = goal

    def is_state(self, state: str) -> bool:
        """Check if state exists in the problem."""
        return state in self.states

    def actions(self, state: str) -> list[str]:
        """Get available actions (neighboring stations) from a state."""
        if state in self.states:
            return self.states[state]["neigh"]
        return []

    def next_state(self, state: str, action: str) -> str | None:
        """Get next state after taking an action."""
        if action in self.actions(state):
            return action
        return None

    def is_goal_state(self, state: str) -> bool:
        """Check if state is the goal."""
        return state == self.goal

    def cost(self, state: str, action: str) -> float:
        """Get cost of taking an action from a state."""
        return self.costs[(state, action)]
