def explain_prediction(file, changed_files, static_graph, coupling_graph):
    changed_set = set(changed_files)
    if file in changed_set:
        return "Same file as change"

    for cf in changed_set:
        if cf in static_graph and file in static_graph:
            if static_graph.has_edge(cf, file):
                return f"{file} is imported by {cf}"
            if static_graph.has_edge(file, cf):
                return f"{file} imports {cf}"
        if cf in coupling_graph and file in coupling_graph:
            if coupling_graph.has_edge(cf, file):
                co = coupling_graph.edges[cf, file].get("co_count", 0)
                return f"{file} co-changed {co} times with {cf}"

    for cf in changed_set:
        if cf in coupling_graph and file in coupling_graph:
            for intermediate in coupling_graph.neighbors(cf):
                if intermediate in coupling_graph and file in coupling_graph:
                    if coupling_graph.has_edge(intermediate, file):
                        return f"{file} co-changed with {intermediate} (linked to {cf})"

    for cf in changed_set:
        if cf in static_graph and file in static_graph:
            for intermediate in static_graph.successors(cf):
                if static_graph.has_edge(intermediate, file):
                    return f"{file} is imported by {intermediate} (which {cf} imports)"
                if static_graph.has_edge(file, intermediate):
                    return f"{file} imports {intermediate} (which imports {cf})"

    return "No direct relationship found"
