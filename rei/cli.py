from datetime import datetime, timezone
from pathlib import Path

import click


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """REI — Repository Evolution Intelligence.

    Predict downstream file/function impact when a developer changes a file.
    """


@cli.command()
@click.argument("repo_url_or_path")
@click.option("--max-commits", default=None, type=int, help="Max commits to extract (default: all)")
def ingest(repo_url_or_path, max_commits):
    """Ingest a repository's git history into the local database."""
    from rei.src.ingestion.repo_parser import parse_repo
    from rei.src.ingestion.git_extractor import extract_history
    from rei.src.storage.commit_store import save_commits

    click.echo(f"Cloning/parsing {repo_url_or_path} ...")
    repo_info = parse_repo(repo_url_or_path)
    click.echo(f"Found {repo_info['total_files']} Python files")

    click.echo("Extracting commit history ...")
    commits = extract_history(repo_info["root"], max_commits=max_commits)
    if not commits:
        click.echo("Warning: No commits found (empty repo).")
        return

    save_commits(commits)

    start_date = datetime.fromtimestamp(commits[0]["timestamp"], tz=timezone.utc).strftime("%Y-%m-%d")
    end_date = datetime.fromtimestamp(commits[-1]["timestamp"], tz=timezone.utc).strftime("%Y-%m-%d")
    click.echo(f"Ingested {len(commits)} commits | {repo_info['total_files']} files | {start_date} -> {end_date}")


@cli.command()
@click.argument("repo_path")
def build_graph(repo_path):
    """Build a static dependency graph from Python AST analysis."""
    from rei.src.ingestion.repo_parser import parse_repo
    from rei.src.graph.graph_builder import build_static_graph
    from rei.src.storage.graph_store import save_graph

    click.echo(f"Parsing {repo_path} ...")
    repo_info = parse_repo(repo_path)

    click.echo(f"Analyzing {repo_info['total_files']} Python files ...")
    graph = build_static_graph(repo_info["root"], repo_info["python_files"])

    n_nodes = graph.number_of_nodes()
    n_edges = graph.number_of_edges()
    n_files = sum(1 for _, d in graph.nodes(data=True) if d.get("kind") == "file")
    skipped = repo_info["total_files"] - n_files

    graph_path = str(Path(__file__).resolve().parent / "data" / "static_graph.json")
    save_graph(graph, graph_path)
    click.echo(f"Graph built: {n_nodes} nodes | {n_edges} edges | {skipped} files skipped")


@cli.command()
@click.argument("repo_path")
def build_coupling(repo_path):
    """Build a change coupling graph from git commit history."""
    from rei.src.storage.commit_store import load_commits
    from rei.src.graph.coupling_analyzer import build_cochange_matrix
    from rei.src.graph.coupling_graph import build_coupling_graph
    from rei.src.graph.noise_filter import filter_graph
    from rei.src.storage.graph_store import save_coupling_graph

    click.echo("Loading commits from SQLite ...")
    commits = load_commits()
    if not commits:
        click.echo("Warning: No commits found. Run 'ingest' first.")
        return

    click.echo("Building co-change matrix ...")
    matrix, file_change_counts = build_cochange_matrix(commits)

    click.echo("Building coupling graph ...")
    raw_graph = build_coupling_graph(matrix, file_change_counts)

    click.echo("Filtering noise ...")
    filtered = filter_graph(raw_graph)

    n_nodes = filtered.number_of_nodes()
    n_edges = filtered.number_of_edges()
    graph_path = str(Path(__file__).resolve().parent / "data" / "coupling_graph.json")
    save_coupling_graph(filtered, graph_path)

    click.echo(f"Coupling graph: {n_nodes} nodes | {n_edges} edges | top 10 pairs:")
    top_edges = sorted(filtered.edges(data=True), key=lambda x: x[2].get("weight", 0), reverse=True)[:10]
    for rank, (u, v, d) in enumerate(top_edges, 1):
        click.echo(f"  {rank:2d}. {u} <-> {v}  (weight={d['weight']:.3f}, co={d['co_count']})")


@cli.command()
@click.argument("repo_path")
@click.option("--db", default=None, help="Path to commits.db (default: ./rei/data/commits.db)")
@click.option("--static", default=None, help="Path to static_graph.json (default: ./rei/data/static_graph.json)")
@click.option("--coupling", default=None, help="Path to coupling_graph.json (default: ./rei/data/coupling_graph.json)")
def eval(repo_path, db, static, coupling):
    """Evaluate prediction accuracy on historical commits."""
    from rei.src.eval.runner import run_eval
    from pathlib import Path

    db_path = db or str(Path(__file__).resolve().parent / "data" / "commits.db")
    static_path = static or str(Path(__file__).resolve().parent / "data" / "static_graph.json")
    coupling_path = coupling  # If None, runner will build coupling from training commits

    click.echo(f"Running evaluation for {repo_path}...")
    metrics = run_eval(repo_path, db_path, static_path, coupling_path)

    click.echo("\nResults:")
    click.echo(f"{'Repo':<15} {'Top5 Acc':<10} {'P@5':<10} {'R@5':<10} {'Runtime':<10} {'Samples':<10}")
    click.echo("-" * 70)
    click.echo(f"{Path(repo_path).name:<15} {metrics['top5_acc']:<10.4f} {metrics['precision5']:<10.4f} {metrics['recall5']:<10.4f} {metrics['runtime_s']:<10.2f} {metrics['sample_count']:<10}")

    results_dir = Path(__file__).resolve().parent / "data" / "eval_results"
    click.echo(f"\nDetailed results saved to {results_dir / Path(repo_path).name}.json")


@cli.command()
@click.argument("repo_path")
@click.option("--changed", required=True, help="Comma-separated list of changed files")
@click.option("--top", default=10, type=int, help="Number of top predictions to show")
@click.option("--alpha", default=0.5, type=float, help="Weight for static score (default: 0.5)")
def predict(repo_path, changed, top, alpha):
    """Predict downstream file impact for a given change."""
    from rei.src.engine.predictor import predict_impact
    from rei.src.engine.explainer import explain_prediction
    from rei.src.storage.graph_store import load_graph

    static_path = str(Path(__file__).resolve().parent / "data" / "static_graph.json")
    coupling_path = str(Path(__file__).resolve().parent / "data" / "coupling_graph.json")

    static_graph = load_graph(static_path)
    coupling_graph = load_graph(coupling_path)

    changed_files = [f.strip() for f in changed.split(",")]
    results = predict_impact(changed_files, static_graph, coupling_graph, top_n=top)

    click.echo(f"{'Rank':<5} {'File':<50} {'Score':<8} {'Confidence':<12} {'Reason'}")
    click.echo("-" * 100)
    for rank, r in enumerate(results, 1):
        reason = explain_prediction(r["file"], changed_files, static_graph, coupling_graph)
        click.echo(f"{rank:<5} {r['file']:<50} {r['score']:<8.4f} {r['confidence']:<12} {reason}")
