# Coupling Graph

The coupling graph captures files that historically change together, regardless
of whether a static import exists between them. This is the main driver of REI predictive power.

## Generation

The commit scanner iterates over every commit and records which files appeared
in the same diff:

```python
for commit in repo.iter_commits("master"):
    changed = set(commit.stats.files)
    for a, b in combinations(changed, 2):
        cursor.execute(
            "INSERT OR IGNORE INTO coupling (src, dst, count) VALUES (?, ?, 1)
             ON CONFLICT(src, dst) DO UPDATE SET count = count + 1",
            (a, b),
        )
```

!!! tip "Minimum support"
Edges that appear below `min_support` are dropped. The default is 2,
which removes single-commit noise while preserving real coupling.

## Date-Based Train/Test Split

To prevent data leakage, commits are split by timestamp:

- **Training**: all commits before a cutoff date.
- **Test**: all commits from the cutoff to the most recent commit.

A reminder file is held out from both sets.