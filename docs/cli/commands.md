# CLI Commands

Run REI with `py -m rei`.

## init

```bash
py -m rei init <repo-path>
```

Ingests commits and Python files into SQLite.

## predict

```bash
py -m rei predict <file-path>
```

Returns a ranked list of affected files.

## eval

```bash
py -m rei eval
```

Runs the full evaluation framework and writes results to `data/eval_results/`.

All commands respect `rei.json` in the project root for configuration.
