# REI: Repository Evolution Intelligence

**Predicting downstream file impact from source code changes using static analysis and historical change coupling.**

[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)]()

REI is a research framework that answers a practical software engineering question: *when a developer changes file X, which other files in the repository are likely to need changes too?* The system combines two complementary signals — a static dependency graph parsed from Python AST and a change-coupling graph mined from git commit history — to rank potentially impacted files.

On the Django codebase (1972 test commits), REI achieves **24.85% Top-5 accuracy** in a temporally-fair evaluation and **46.50% Top-5 accuracy** when using the full available co-change history.

![REI overview](https://via.placeholder.com/800x400?text=REI+Architecture+Diagram)

## Table of Contents

- [Motivation](#motivation)
- [Method](#method)
- [Results](#results)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Citing](#citing)
- [License](#license)

---

## Motivation

Modern software repositories are large and densely interconnected. A single-line change in a utility module can cascade into breakages across dozens of downstream files. Developers currently rely on mental models, build systems, and ad-hoc testing to navigate this dependency graph — approaches that are manual, incomplete, or slow.

REI formalises this problem as a **learning-to-rank** task over a heterogeneous graph built from two sources:

1. **Static dependencies** — import and call relationships extracted via Python AST analysis.
2. **Historical change coupling** — files that frequently co-appear in the same commit, mined from git history.

The goal is to predict, for a given changed file, the set of other files that will be modified in the same commit. This enables tooling that surfaces likely breakages before a build or test cycle.

## Method

### Graph Construction

**Static Graph.** Each Python file is parsed with the `ast` module to extract imports, function definitions, class definitions, and function call targets. A directed graph is built where file nodes connect to their defined functions/classes via `defines` edges, and files connect to imported modules via `imports` edges. Test files (paths containing `/test` or `/tests`) are excluded from the static graph to avoid candidate-set pollution.

**Coupling Graph.** Git commit history is mined to build a co-change matrix: for every pair of files that appear in the same commit, the count of co-occurrences is recorded. Edges with fewer than `min_support=2` co-occurrences or edge weight below `min_weight=0.05` are filtered. The resulting undirected weighted graph captures historical change dependencies.

### Prediction

Given a set of changed files (the *query*), REI:

1. **Collects candidates** via breadth-first traversal in both graphs — direct and 2-hop neighbours of each query file.
2. **Scores candidates** using a query-aware function:

| Relationship | Score Contribution |
|---|---|
| Direct co-change edge | `weight × 10.0` |
| 2-hop co-change chain | `w₁ × w₂ × 3.0` |
| Static import (candidate → query) | `+2.0` |

3. **Ranks** candidates by descending score and returns the top-N.

The key insight behind the scoring function is that it is **query-dependent**: unlike prior approaches that rank by global file popularity (e.g., total number of importers), REI measures the *specific connection strength* between each candidate and the query.

### Evaluation

Evaluation follows a **temporal train/test split** at `2023-01-01`. For each commit in the test period, each changed file becomes a query and the remaining co-changed files are the ground-truth targets. The coupling graph is rebuilt from *training commits only* to prevent data leakage. Metrics:

- **Top-5 Accuracy**: fraction of test cases where at least one ground-truth file appears among the top-5 predictions.
- **Precision@5**, **Recall@5**: standard information retrieval metrics over the top-5 ranked list.

## Results

### Django (2919 Python files, 5000 commits, 1972 test cases)

| Eval Type | Top-5 Acc | P@5 | R@5 | Description |
|---|---|---|---|---|
| Baseline (Phase 0–4) | 13.29% | 0.031 | 0.065 | Original global-popularity scorer |
| **Fair (Phase 5.5)** | **24.85%** | **0.060** | **0.138** | Query-aware scorer, training-only coupling graph |
| Upper Bound | 46.50% | 0.125 | 0.277 | Query-aware scorer, full historical coupling graph |

The jump from 13.29% → 24.85% is driven entirely by the shift from query-independent (global popularity) to query-aware scoring. The upper bound of 46.50% demonstrates that coverage — not ranking quality — is the primary remaining bottleneck: 34% of test queries are non-Python files (documentation, configuration, JavaScript) that cannot appear in any graph, and an additional fraction have insufficient co-change history in the training window.

### Ablation Studies

| Change | Top-5 Acc | Verdict |
|---|---|---|
| Baseline | 13.29% | – |
| + Query-aware scoring | **24.85%** | Core improvement |
| + `min_support=3 → 2` | **25.96%** | Helpful with query-aware scoring |
| + Log-scale normalisation | 10.70% | Hurts (score compression) |
| + Bidirectional BFS | 4.56% | Hurts (successor-derived candidates are noise) |
| + Test files in static graph | 7.91% | Hurts (candidate set pollution) |

---

## Installation

```bash
# Clone the repository
git clone https://github.com/RavaniRoshan/REI.git
cd REI

# It is recommended to use a virtual environment
py -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install --editable .
```

**Requirements:**
- Python ≥ 3.10
- Git (for history extraction)
- NetworkX ≥ 3.0
- Click, Rich (CLI)

---

## Usage

REI exposes a CLI through `py -m rei` with five commands:

```bash
# 1. Ingest a repository
py -m rei ingest https://github.com/django/django.git

# 2. Build the static dependency graph
py -m rei build-graph /path/to/django

# 3. Build the change-coupling graph
py -m rei build-coupling /path/to/django

# 4. Evaluate prediction accuracy
py -m rei eval /path/to/django

# 5. Predict impact for a specific change
py -m rei predict /path/to/django --changed django/core/wsgi.py --top 5
```

### Reproducing the Evaluation

```bash
# Ingest Django (up to 5000 commits)
py -m rei ingest https://github.com/django/django.git --max-commits 5000

# Build graphs
py -m rei build-graph rei/data/tmp/django
py -m rei build-coupling rei/data/tmp/django

# Run fair evaluation
py -m rei eval rei/data/tmp/django

# Run with full coupling graph (upper bound)
py -m rei eval rei/data/tmp/django --coupling rei/data/coupling_graph.json
```

---

## Project Structure

```
REI/
├── rei/
│   ├── cli.py                     # CLI entry point (Click commands)
│   ├── src/
│   │   ├── engine/
│   │   │   ├── predictor.py       # Candidate collection & query-aware scoring
│   │   │   ├── scorer.py          # Legacy scoring functions
│   │   │   └── explainer.py       # Prediction explanation
│   │   ├── eval/
│   │   │   ├── runner.py          # Evaluation orchestrator
│   │   │   ├── ground_truth.py    # Temporal train/test split
│   │   │   └── metrics.py         # Top-5 Acc, P@5, R@5
│   │   ├── graph/
│   │   │   ├── graph_builder.py   # Static graph construction (AST)
│   │   │   ├── static_analyzer.py # Per-file AST analysis
│   │   │   ├── coupling_analyzer.py # Co-change matrix computation
│   │   │   ├── coupling_graph.py  # Coupling graph builder
│   │   │   └── noise_filter.py    # Edge filtering (min_support, min_weight)
│   │   ├── ingestion/
│   │   │   ├── repo_parser.py     # Repository cloning & file discovery
│   │   │   └── git_extractor.py   # Git commit history extraction
│   │   └── storage/
│   │       ├── commit_store.py    # SQLite commit persistence
│   │       └── graph_store.py     # JSON graph serialization
│   └── data/                      # Generated data (gitignored)
│       ├── commits.db
│       ├── static_graph.json
│       ├── coupling_graph.json
│       └── eval_results/
├── RESULTS.md                     # Full evaluation report
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## Future Work

- **Per-repo database isolation**: Currently all repos share a single `commits.db`, preventing clean multi-repo evaluation.
- **Non-Python coverage**: 34% of test queries are documentation, config, or JS files. A filename-based dependency heuristic could cover these.
- **ML-based scoring**: Replace hand-tuned weights with a learned ranking model (e.g., LambdaRank) over graph features.
- **Embedding-based candidate expansion**: Use code embeddings to find semantically similar files beyond co-change edges.
- **Continuous coupling**: Update the coupling graph incrementally as new commits arrive, rather than full rebuilds.

## Citing

If you use REI in your research, please cite:

```bibtex
@misc{rei2025,
  author = {Roshan Ravani},
  title = {{REI}: Repository Evolution Intelligence},
  year = {2026},
  howpublished = {\url{https://github.com/RavaniRoshan/REI}}
}
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
