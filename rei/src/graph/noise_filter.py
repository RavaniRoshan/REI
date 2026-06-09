import networkx as nx


def filter_graph(graph, min_support=2, min_weight=0.05):
    filtered = graph.copy()
    to_remove = []
    for u, v, data in filtered.edges(data=True):
        if u == v:
            to_remove.append((u, v))
            continue
        if data.get("co_count", 0) < min_support:
            to_remove.append((u, v))
        elif data.get("weight", 0) < min_weight:
            to_remove.append((u, v))
    filtered.remove_edges_from(to_remove)
    isolated = list(nx.isolates(filtered))
    filtered.remove_nodes_from(isolated)
    return filtered
