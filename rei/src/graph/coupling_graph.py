import networkx as nx


def build_coupling_graph(cochange_matrix, file_change_counts):
    graph = nx.Graph()
    for (a, b), co_count in cochange_matrix.items():
        changes_a = file_change_counts.get(a, 1)
        changes_b = file_change_counts.get(b, 1)
        weight = co_count / max(changes_a, changes_b)
        graph.add_edge(a, b, weight=weight, co_count=co_count)
    return graph
