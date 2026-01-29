"""Search algorithms and data structures for route finding."""

from typing import Any


class Node:
    """Node in the search tree.

    Attributes:
        state: Current state (station name)
        cost: Accumulated cost to reach this state
        parent: Parent node in the search tree
        action: Action taken to reach this state
        depth: Depth in the search tree
    """

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


class Stack:
    """Stack data structure for DFS."""

    def __init__(self):
        self.items: list[Any] = []

    def push(self, item: Any) -> None:
        """Add item to top of stack."""
        self.items.append(item)

    def pop(self) -> Any:
        """Remove and return top item from stack."""
        return self.items.pop()

    def peek(self) -> Any:
        """Return top item without removing it."""
        return self.items[-1]

    def __len__(self) -> int:
        return len(self.items)


def depth_first_search(problem: Any) -> Node | None:
    """Find path using Depth-First Search.

    Args:
        problem: Problem instance with start, goal, actions(), next_state(), etc.

    Returns:
        Goal node if found, None otherwise
    """
    node = Node(problem.start, 0)
    frontier = Stack()
    frontier.push(node)
    explored: set[str] = set()

    while len(frontier) > 0:
        node = frontier.pop()
        explored.add(node.state)

        if problem.is_goal_state(node.state):
            return node

        for action in problem.actions(node.state):
            next_state = problem.next_state(node.state, action)
            if next_state not in explored:
                cost = problem.cost(node.state, action) + node.cost
                frontier.push(Node(next_state, cost, node, action))

    return None
