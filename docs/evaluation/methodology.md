# Methodology

REI is measured against real commit history using a **date-based train/test split**
to prevent future-data leakage.

## Data

- Target repository is cloned and commits are extracted in reverse-chronological order.
- Only `.py` files are kept for the static graph.
- train/test cutoff is chosen so ~70-80% of commits are training.

## Query Selection

- Every unique file touched in the test commits becomes a query.
- Files without any coupling or static incoming edges are skipped automatically.

## Metric

`top_k_accuracy` ' did the ground-truth file appear in the `k` highest-ranked predictions?

- **Fair** evaluation: coupling graph only (`--coupling`).
- **Full-CG** evaluation: evidence from all commits in the graph (deployed via `--coupling --full`).

## Why date split matters

A train/test split that is random at the line or commit level leaks future
information into the model. Using timestamps ensures REI is evaluated on
"what it would have known at the time."

!!! info "Note on non-Python files"
~34% of test queries are non-Python (JS, docs, locale). Those cases are
included in the denominator but are unreachable by the Python-only analyzer.
This is the main reason fair accuracy stays below 30%.