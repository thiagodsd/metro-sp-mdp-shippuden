use pyo3::prelude::*;
use std::collections::{HashMap, HashSet};

#[derive(Clone)]
struct Node {
    state: String,
    cost: f64,
    parent: Option<Box<Node>>,
    depth: usize,
}

impl Node {
    fn new(state: String, cost: f64, parent: Option<Box<Node>>) -> Self {
        let depth = parent.as_ref().map(|p| p.depth + 1).unwrap_or(0);
        Node {
            state,
            cost,
            parent,
            depth,
        }
    }
}

fn cost_function(pos1: (f64, f64), pos2: (f64, f64)) -> f64 {
    let (y1, x1) = pos1;
    let (y2, x2) = pos2;
    ((x1 - x2).powi(2) + (y1 - y2).powi(2)).sqrt()
}

#[pyfunction]
fn depth_first_search(
    graph: HashMap<String, Vec<String>>,
    positions: HashMap<String, (f64, f64)>,
    start: String,
    goal: String,
) -> PyResult<Option<Vec<String>>> {
    // precalculate costs
    let mut costs: HashMap<(String, String), f64> = HashMap::new();
    for (station, neighbors) in &graph {
        let pos_from = positions.get(station).unwrap();
        for neighbor in neighbors {
            let pos_to = positions.get(neighbor).unwrap();
            costs.insert(
                (station.clone(), neighbor.clone()),
                cost_function(*pos_from, *pos_to),
            );
        }
    }

    let root = Node::new(start.clone(), 0.0, None);
    let mut frontier = vec![root];
    let mut explored: HashSet<String> = HashSet::new();

    while let Some(node) = frontier.pop() {
        explored.insert(node.state.clone());

        if node.state == goal {
            // reconstruct path
            let mut path = Vec::new();
            let mut current = Some(Box::new(node));
            while let Some(n) = current {
                path.push(n.state.clone());
                current = n.parent;
            }
            path.reverse();
            return Ok(Some(path));
        }

        if let Some(neighbors) = graph.get(&node.state) {
            for neighbor in neighbors {
                if !explored.contains(neighbor) {
                    let edge_cost = costs
                        .get(&(node.state.clone(), neighbor.clone()))
                        .unwrap_or(&0.0);
                    let new_cost = node.cost + edge_cost;
                    let new_node = Node::new(neighbor.clone(), new_cost, Some(Box::new(node.clone())));
                    frontier.push(new_node);
                }
            }
        }
    }

    Ok(None)
}

#[pymodule]
fn _rust(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(depth_first_search, m)?)?;
    Ok(())
}
