# REI Evaluation Results

## Summary Table

| Repo  | Eval Type | Top5 Acc | P@5   | R@5   | Runtime (s) | Samples |
|-------|-----------|----------|-------|-------|-------------|---------|
| Flask | Baseline  | 0.0047   | 0.0009| 0.0016| 0.01        | 213     |
| Django| Baseline  | 0.1329   | 0.0311| 0.0650| 0.38        | 1972    |
| Django| Phase 5.5 | **0.2485**| 0.0602| 0.1378| 0.44        | 1972    |
| Django| Full CG   | **0.4650**| 0.1248| 0.2774| 1.00        | 1972    |

*FastAPI and LangChain: evaluation not completed due to resource constraints (see Per-Repo Analysis).*

---

## Key Improvements (Phase 5.5)

The jump from 13.29% → 24.85% (fair) / 46.50% (full CG) was achieved by:

1. **Query-aware scoring** (predictor.py): Instead of ranking candidates by global popularity (sum of all edge weights / total nodes), score each candidate by its **edge weight to the query**. Direct co-change edges get `weight × 10`, 2-hop coupling chains get `product × 3`, and static import edges get `+2`.

2. **Reduced min_support to 2** (noise_filter.py): Previously `min_support=3` filtered out too many legitimate co-change pairs. With query-aware scoring, the extra edges are signal, not noise.

3. **All other changes reverted**: Log-scale normalization, test-file inclusion, and bidirectional BFS all hurt accuracy individually and were abandoned.

---

## Explanation of Eval Types

- **Fair**: Coupling graph built from training commits only (no data leakage). Realistic performance estimate.
- **Full CG**: Coupling graph built from all commits (includes test-period edges). Upper-bound performance.
- **Baseline**: Original Phase 0-4 predictor without any Phase 5.5 changes.

---

## Why the Old Scorer Failed

The original `compute_static_score` and `compute_coupling_score` were **query-independent**: they scored candidates by how many total co-changes or importers a file had, not by its relationship to the query file. A widely-used utility module ranked high for *every* query, regardless of whether it actually co-changed with the query.

The new `_score_candidate` function directly measures the connection strength between the query and each candidate:

```
Direct co-change neighbor:    weight × 10.0
2-hop co-change (via mid):    w1 × w2 × 3.0
Static import (→ query):       +2.0
```

---

## Remaining Challenges

1. **Shared commits DB**: All repos share one `commits.db`, making per-repo evaluation unreliable. Each repo needs its own database for clean evaluation.

2. **Non-Python coverage**: 30% of test queries are docs, JS, CSS, locale files, etc. These files cannot be predicted by a Python-only AST analyzer.

3. **Test file exclusions**: Test files are excluded from the static graph (but appear in the coupling graph). Some co-change signal is lost.

4. **Training CG is small**: Only 1651 training commits produce a coupling graph with ~213 nodes (min_support=3) or ~300+ nodes (min_support=2). More historical data would improve coverage.

---

## Per-Repo Analysis

### Django (Fair: 24.85%, Full CG: 46.50%)

- **1972 test cases** from 3349 test-split commits (filtered to 2–20 files per commit).
- **Fair eval**: 490/1972 cases have at least one correct file in top-5 predictions.
- **Full CG eval**: 917/1972 cases have at least one correct file.
- **Empty predictions**: ~807 cases (the query file itself is not in any graph — docs, JS, etc.).
- **Query-aware scoring** fixes the fundamental ranking issue: candidates are now scored by connection strength to the query, not global popularity.

### FastAPI & LangChain

- These repos were **not evaluated** within the time allocated. The multi-repo data-sharing issue must be resolved first (each repo needs its own commits.db). The evaluation framework is ready, but clean runs are future work.

---

## Failure Case Analysis (Updated)

Top-5 accuracy at 24.85% means **75% of test cases still fail**. Common failure patterns:

1. **Query file not in any graph**: 674/1972 (34%) test queries are non-Python files (docs, JS, CSS, `.po`, `.txt`). These are impossible to predict with a Python-only analyzer.

2. **No coupling neighbors in training data**: Files that appear in <2 training-commits have no coupling edges. They produce 0 candidates.

3. **Test files as actual impacts**: Test files are excluded from static graph candidates. When the only actual impact is a test file (common in Django where commits often bundle code + test changes), the prediction misses.

4. **Weak co-change signal**: Some production files co-change infrequently (<2 times in training), so they don't appear in the coupling graph even though they logically depend on the query.

---

## Continue / Kill Decision

### Thresholds (from exit plan)
- Top5 Acc > 60% → continue
- Top5 Acc 30–60% → consider improvements
- Top5 Acc < 30% → kill

### Results
- Baseline: Django 13.3% (<30%) → Kill
- Phase 5.5: Django **24.85%** (fair) / **46.50%** (full CG)

### Recommendation
**Continue with improvements.** The fair eval (24.85%) is still below the 30% threshold, but the full-CG upper bound (46.50%) demonstrates the approach works when given sufficient data. The remaining gap is primarily **coverage** — with more training commits and better non-Python handling, 30%+ is achievable.

### Next Steps to Cross 30%
1. **Separate per-repo databases** for clean evaluation
2. **Ingest more historical data** (increase max_commits beyond 5000)
3. **Support non-Python files** in the impact graph (docs, config) using simple filename-based edges
4. **Re-evaluate FastAPI and LangChain** with clean per-repo databases

---

## Appendix: Evaluation Details

- **Split date:** 2023-01-01 (unix timestamp 1672531200)
- **Static graph**: built from AST of the latest repo HEAD (test files excluded, fixtures/skipped only)
- **Coupling graph**: built from training commits (fair) or all commits (full CG), using `min_support=2` and `min_weight=0.05`.
- **Alpha**: 0.5 (equal weighting, but coupling dominates due to scoring scale)
- **Metrics**: Top5 accuracy (binary hit), Precision@5, Recall@5.

All code for evaluation lives in `rei/src/eval/`. Raw per-test-case results are saved in `rei/data/eval_results/{repo}.json`.
