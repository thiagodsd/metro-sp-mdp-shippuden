from typing import Any


class Node:
    def __init__(
        self, state: str, cost: float, parent: "Node | None" = None, action: str | None = None
    ):
        self.state = state
        self.cost = cost
        self.parent = parent
        self.action = action
        self.depth = parent.depth + 1 if parent else 0

    def __repr__(self) -> str:
        return f"<Node {self.state}>"


def depth_first_search(problem: Any) -> Node | None:
    node = Node(problem.start, 0)
    frontier = [node]
    explored: set[str] = set()

    while frontier:
        node = frontier.pop()
        explored.add(node.state)

        if problem.is_goal_state(node.state):
            return node

        for action in problem.actions(node.state):
            next_state = problem.next_state(node.state, action)
            if next_state not in explored:
                cost = problem.cost(node.state, action) + node.cost
                frontier.append(Node(next_state, cost, node, action))

    return None
