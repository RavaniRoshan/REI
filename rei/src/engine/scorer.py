import networkx as nx


def compute_static_score(file: str, static_graph: nx.DiGraph) -> float:
    if file not in static_graph:
        return 0.0
    n_nodes = static_graph.number_of_nodes()
    if n_nodes == 0:
        return 0.0
    raw = sum(1.0 for _, _, d in static_graph.in_edges(file, data=True) if d.get("label") in ("imports", "calls"))
    return raw / n_nodes


def compute_coupling_score(file: str, coupling_graph: nx.Graph) -> float:
    if file not in coupling_graph:
        return 0.0
    neighbors = list(coupling_graph.neighbors(file))
    if not neighbors:
        return 0.0
    raw = sum(coupling_graph[file][nbr].get("weight", 0.0) for nbr in neighbors)
    max_neighbors = max(len(coupling_graph) - 1, 1)
    return raw / max_neighbors


def compute_combined_score(static: float, coupling: float, alpha: float = 0.5) -> float:
    return alpha * static + (1.0 - alpha) * coupling
