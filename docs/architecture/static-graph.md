# Static Graph

REI analyses the Python source tree and builds a directed dependency graph from
`import` and `from ... import` statements.

## How It Works

- Walk the target repository and index every `.py` file.
- Parse each file's AST and record incoming `import` edges.
- Store the result in SQLite as pairs `(source_file, target_file)`.

```python
import ast, pathlib

for path in pathlib.Path("repo").rglob("*.py"):
    tree = ast.parse(path.read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            yield str(path), node.module.replace(".", "/") + ".py"
```

!!! info "Scope"
The static graph is read-only and cross-repo. A file is reachable only if the
import chain exists inside the indexed source tree.

## Usage from the CLI

```bash
py -m rei init /path/to/repo
```

This builds both the static graph and the commit graph in one pass.

## Limitations

- Imports done dynamically (e.g. `importlib.import_module`) are invisible.
- The graph is scoped to `.py` files; other languages are routed through
  filename heuristics during evaluation.