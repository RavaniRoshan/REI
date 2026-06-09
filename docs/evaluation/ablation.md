# Ablation Studies

Each change tested individually against the baseline:

| Change | Top-5 | Effect |
|--------|------:|--------|
| Baseline (static + global popularity) | 13.29% | baseline |
| + Query-aware scoring (no min_support change) | 10.70% | hurt |
| + min_support=2 (with old scorer) | 7.61% | hurt |
| + Bidirectional BFS | 4.56% | hurt |
| + Log-scale normalization | 10.70% | hurt |
| + Test files in static graph | 7.91% | hurt |
| + Query-aware scoring + min_support=2 | **24.85%** | **+87% relative gain** |

!!! success "Key insight"
Query-aware scoring is the breakthrough. All other changes were reverted.
