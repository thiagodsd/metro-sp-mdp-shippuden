# metro-mdp-rust

rust-powered mdp route planning for são paulo metro system

## what

same api as metro-mdp, but with rust under the hood for performance.

uses pyo3 to expose rust implementations of:
- depth-first search algorithm
- graph operations
- cost calculations

## install

```bash
pip install metro-mdp-rust
```

or from git:
```bash
pip install git+https://github.com/thiagodsd/metro-sp-mdp-shippuden.git@main#subdirectory=packages/metro-mdp-rust
```

## usage

same as metro-mdp:

```python
import pandas as pd
from metro_mdp import solve_route, fuzz_string

df = pd.read_csv("stations.csv")
route = solve_route(df, "luz", "paulista")
print(route)
```

## performance

ainda preciso benchmarkar direito, mas teoricamente rust deve ser mais rápido
que python puro pra essa parte de busca no grafo.

na prática pra grafos pequenos (~80 estações) a diferença é mínima - overhead de
conversão python→rust cancela os ganhos. pra grafos maiores deveria compensar.

## dev

requires rust toolchain.

```bash
maturin develop
```
