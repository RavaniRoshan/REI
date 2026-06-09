# Why REI?

## The Problem

Every developer has experienced the "change one file, break ten others" syndrome.
When you modify a function in one module, the files that depend on it may silently break.

## What REI Does

REI predicts which files in a repository are likely to need changes when you
modify a given file.

1. **Static dependency analysis** - the import structure of the codebase.
2. **Evolutionary coupling analysis** - files that historically changed together.

!!! tip "Query-aware scoring"
The core engine ranks candidates by coupling strength directly to the query
file, delivering a **87% relative improvement** over baseline.

Next: [Quick Start >](quick-start.md)
