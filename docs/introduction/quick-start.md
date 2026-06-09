# Quick Start

Get REI running in under 5 minutes.

## Installation

REI is a Python tool (3.8+).

```bash
py -m pip install -e .
```

## Initialize

```bash
py -m rei init <path-to-your-repo>
```

## Predict

```bash
py -m rei predict <file-path>
```

```bash
py -m rei predict django/db/models/fields/__init__.py
```

## Evaluate Accuracy

```bash
py -m rei eval
```

Results are saved under `data/eval_results/`.

Next: [System Overview >](../architecture/overview.md)
