# Prediction Engine

The engine takes a target file (the "query"), queries the static and coupling graphs, and returns a ranked list of affected files.

## Candidate Generation

1. Look up the coupling graph: files that co-changed with the query.
2. Walk one hop of the static graph: direct importers of the query.
3. Union the two sets and remove the query itself.

## Scoring: Query-Aware (Not Global Popularity)

This is the single biggest improvement in REI. The current scorer computes weight only along the edge from candidate back to the query:

- Direct co-change (coupling edge): `weight x 10`
- Two-hop co-change via another file: `w1 x w2 x 3`
- Direct import (static edge): `+2`

```python
score = (
    coupling_weight(query, candidate) * 10
    + max_2hop * 3
    + (1 if imports_directly(candidate, query) else 0) + 1
)
```

!!! success "Key insight"
The ranking reflects relevance to this query, not just global changefrequency.

## Explainer

Every prediction carries a reason:

- "Changed together 22 times"
- "Direct importer of models/fields.py"
- "Two-hop: changes fields.py and core.py together"
