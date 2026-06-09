import networkx as nx


def _file_neighbors(file, static_graph, coupling_graph):
    one_hop = set()
    two_hop = set()

    if file in static_graph:
        for h1 in static_graph.predecessors(file):
            kind = static_graph.nodes[h1].get("kind", "")
            if kind == "file":
                one_hop.add(h1)
            elif kind == "function":
                mapped = _map_function_to_file(h1, static_graph)
                if mapped and mapped != file:
                    one_hop.add(mapped)
        for h1 in one_hop:
            for h2 in static_graph.predecessors(h1):
                kind2 = static_graph.nodes[h2].get("kind", "")
                if kind2 == "file":
                    two_hop.add(h2)
                elif kind2 == "function":
                    mapped2 = _map_function_to_file(h2, static_graph)
                    if mapped2:
                        two_hop.add(mapped2)

    if file in coupling_graph:
        for h1 in coupling_graph.neighbors(file):
            one_hop.add(h1)
            for h2 in coupling_graph.neighbors(h1):
                two_hop.add(h2)

    return one_hop | two_hop


def _map_function_to_file(fn_node, static_graph):
    for pred, _, data in static_graph.in_edges(fn_node, data=True):
        if data.get("label") == "defines" and static_graph.nodes[pred].get("kind") == "file":
            return pred
    return None


def predict_impact(changed_files, static_graph, coupling_graph, top_n=10):
    changed_set = set(changed_files)
    candidates = set()
    for f in changed_set:
        candidates.update(_file_neighbors(f, static_graph, coupling_graph))
    candidates -= changed_set

    seen = {}
    for candidate in candidates:
        if candidate not in static_graph and candidate not in coupling_graph:
            continue
        score = _score_candidate(changed_set, candidate, static_graph, coupling_graph)
        if score > 0:
            seen[candidate] = {"file": candidate, "score": score}

    if not seen:
        return []

    ranked = sorted(seen.values(), key=lambda r: (-r["score"], r["file"]))
    results = []
    for r in ranked[:top_n]:
        score = r["score"]
        confidence = "high" if score > 5.0 else ("medium" if score > 1.0 else "low")
        results.append({"file": r["file"], "score": round(score, 6), "confidence": confidence})
    return results


def _score_candidate(changed_set, candidate, static_graph, coupling_graph):
    best = 0.0
    for query in changed_set:
        score = 0.0

        if query in coupling_graph and candidate in coupling_graph:
            if coupling_graph.has_edge(query, candidate):
                w = coupling_graph[query][candidate].get("weight", 0)
                score = max(score, w * 10.0)
            else:
                for mid in coupling_graph.neighbors(query):
                    if coupling_graph.has_edge(mid, candidate):
                        w1 = coupling_graph[query][mid].get("weight", 0)
                        w2 = coupling_graph[mid][candidate].get("weight", 0)
                        score = max(score, w1 * w2 * 3.0)

        if candidate in static_graph:
            if static_graph.has_edge(candidate, query):
                score = max(score, 2.0)

        if score > best:
            best = score
    return best
