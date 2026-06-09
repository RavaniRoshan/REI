import time
from pathlib import Path

from rei.src.eval.ground_truth import build_ground_truth
from rei.src.eval.metrics import compute_all_metrics
from rei.src.engine.predictor import predict_impact
from rei.src.storage.graph_store import load_graph
from rei.src.graph.coupling_analyzer import build_cochange_matrix
from rei.src.graph.coupling_graph import build_coupling_graph
from rei.src.graph.noise_filter import filter_graph


def run_eval(repo_path, db_path, static_graph_path, coupling_graph_path=None):
    from rei.src.storage.commit_store import load_commits
    commits = load_commits(db_path)
    ground = build_ground_truth(commits)
    test_cases = ground["test"]

    static_graph = load_graph(static_graph_path)
    if coupling_graph_path:
        coupling_graph = load_graph(coupling_graph_path)
    else:
        train_commits = ground["train"]
        matrix, file_change_counts = build_cochange_matrix(train_commits)
        raw = build_coupling_graph(matrix, file_change_counts)
        coupling_graph = filter_graph(raw)

    start = time.time()
    results = []
    total = len(test_cases)
    for idx, case in enumerate(test_cases):
        if idx > 0 and idx % 100 == 0:
            elapsed = time.time() - start
            rate = idx / elapsed if elapsed > 0 else 0
            print(f"  [{idx}/{total}] {elapsed:.1f}s elapsed, {rate:.1f} cases/s")
        query = case["query"]
        actual = case["actual"]
        preds_raw = predict_impact([query], static_graph, coupling_graph, top_n=5)
        predictions = [p["file"] for p in preds_raw]
        results.append({"predictions": predictions, "actual": actual})
    runtime = time.time() - start

    metrics = compute_all_metrics(results)
    metrics["runtime_s"] = runtime
    metrics["sample_count"] = len(test_cases)

    output_dir = Path(__file__).resolve().parent.parent.parent / "data" / "eval_results"
    output_dir.mkdir(parents=True, exist_ok=True)
    repo_name = Path(repo_path).name
    output_path = output_dir / f"{repo_name}.json"
    import json
    output_data = {
        "repo": repo_name,
        "metrics": metrics,
        "cases": [{"query": test_cases[i]["query"], "actual": test_cases[i]["actual"], "predictions": results[i]["predictions"]} for i in range(len(results))],
    }
    with open(output_path, "w") as f:
        json.dump(output_data, f, indent=2)

    return metrics
