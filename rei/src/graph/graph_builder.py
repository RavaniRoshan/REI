import os
from typing import List

import networkx as nx

from rei.src.graph.static_analyzer import analyze_file


def build_static_graph(repo_root: str, py_files: List[str]) -> nx.DiGraph:
    graph = nx.DiGraph()
    skipped = 0
    all_analyses = {}

    for rel_path in py_files:
        if "/test" in rel_path or "/tests" in rel_path:
            skipped += 1
            continue
        basename = os.path.basename(rel_path)
        if basename == "__init__.py":
            abs_path = os.path.join(repo_root, rel_path)
            try:
                with open(abs_path, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read().strip()
                if not content or content.startswith("from ") or content.startswith("import "):
                    skipped += 1
                    continue
            except Exception:
                skipped += 1
                continue

        analysis = analyze_file(rel_path, repo_root)
        if not analysis:
            skipped += 1
            continue
        all_analyses[rel_path] = analysis

        graph.add_node(rel_path, kind="file")
        for fn in analysis["functions"]:
            graph.add_node(fn, kind="function")
            graph.add_edge(rel_path, fn, label="defines")
        for cls in analysis["classes"]:
            graph.add_node(cls, kind="class")
            graph.add_edge(rel_path, cls, label="defines")

    for rel_path, analysis in all_analyses.items():
        for imp in analysis["imports"]:
            if imp in all_analyses:
                graph.add_edge(rel_path, imp, label="imports")

    function_index = {}
    for path, analysis in all_analyses.items():
        for fn in analysis["functions"]:
            name = fn.split("::")[-1]
            function_index.setdefault(name, []).append(fn)

    added_call_edges = set()
    for rel_path, analysis in all_analyses.items():
        for call_name in analysis["calls"]:
            for qualified_fn in function_index.get(call_name, []):
                if qualified_fn in all_analyses[rel_path]["functions"]:
                    continue
                edge_key = (rel_path, qualified_fn, "calls")
                if edge_key not in added_call_edges:
                    graph.add_edge(rel_path, qualified_fn, label="calls")
                    added_call_edges.add(edge_key)

    return graph
