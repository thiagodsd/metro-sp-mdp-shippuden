# Metro SP MDP

Route planning library for São Paulo Metro system using Markov Decision Process (MDP) and Depth-First Search.

## Installation

From the repository root:

```bash
cd packages/metro-mdp-lib
uv pip install -e .
```

## Usage

### Basic Route Finding

```python
import pandas as pd
from metro_mdp import solve_route

# Load station data
df = pd.read_csv("stations.csv")

# Find route
route = solve_route(df, origin="luz", destination="paulista")
print(route)  # ['luz', 'republica', 'anhangabau', 'se', 'paulista']
```

### With Fuzzy Matching

```python
from metro_mdp import solve_route, fuzz_string
import pandas as pd

df = pd.read_csv("stations.csv")

# Handle typos or variations in station names
origin = fuzz_string("estacao da luz", df["station"])
destination = fuzz_string("estação paulista", df["station"])

route = solve_route(df, origin, destination)
```

### Advanced Usage

```python
from metro_mdp import Problem, depth_first_search

# Create MDP problem
problem = Problem(df, start="luz", goal="paulista")

# Solve using DFS
solution_node = depth_first_search(problem)

# Extract path
path = []
node = solution_node
while node:
    path.append(node.state)
    node = node.parent
path = path[::-1]
```

## Data Format

The station data CSV should have the following columns:

- `station`: Station name (string)
- `neigh`: List of neighboring stations as string (e.g., "['republica','se']")
- `lat`: Latitude (float)
- `lon`: Longitude (float)
- `line`: Metro line(s) (optional, for display purposes)

## Development

Install dev dependencies:

```bash
uv sync --all-extras
```

Run tests:

```bash
uv run pytest
```

Run linting:

```bash
uv run ruff check .
uv run ruff format --check .
```
