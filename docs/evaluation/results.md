# Results

| Metric | Top-5 | Top-10 |
|--------|------:|-------:|
| Baseline (static + global popularity) | 13.29% | 17.05% |
| Fair evaluation (query-aware scoring) | **24.85%** | **32.14%** |
| Full coupling graph upper bound | **46.50%** | **56.21%** |

## Observations

- **99% of correct predictions come from the coupling graph.** The static graph contributes almost nothing in fair evaluation.
- The gap between 24.85% and 46.50% shows that more history unlocks the approach; increasing `max_commits` is the natural next experiment.
- Run `py -m rei eval` and results are saved under `data/eval_results/<repo>.json`.
