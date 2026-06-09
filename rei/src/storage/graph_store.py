import json
from pathlib import Path

import networkx as nx


def save_graph(graph: nx.Graph, path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    data = nx.node_link_data(graph)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_graph(path: str) -> nx.Graph:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return nx.node_link_graph(data)


def save_coupling_graph(graph: nx.Graph, path: str) -> None:
    save_graph(graph, path)
