import ast
import os
from pathlib import Path


def _resolve_import(module_path: str, file_path: str, repo_root: str, level: int = 0) -> str:
    if level > 0:
        file_dir = os.path.dirname(file_path)
        for _ in range(level - 1):
            file_dir = os.path.dirname(file_dir)
        parts = module_path.split(".") if module_path else []
        resolved = os.path.join(file_dir, *parts) if parts else file_dir
        for suffix in (".py", "/__init__.py"):
            candidate = os.path.normpath(os.path.join(resolved + suffix))
            abs_candidate = os.path.normpath(os.path.join(repo_root, candidate))
            if os.path.isfile(abs_candidate):
                return candidate.replace("\\", "/")
    else:
        parts = module_path.split(".")
        resolved = os.path.join(*parts)
        for suffix in (".py", "/__init__.py"):
            candidate = os.path.normpath(os.path.join(resolved + suffix))
            abs_candidate = os.path.normpath(os.path.join(repo_root, candidate))
            if os.path.isfile(abs_candidate):
                return candidate.replace("\\", "/")
    return module_path


def analyze_file(file_path: str, repo_root: str) -> dict:
    abs_path = os.path.join(repo_root, file_path)
    try:
        with open(abs_path, "r", encoding="utf-8", errors="replace") as f:
            source = f.read()
        tree = ast.parse(source, filename=file_path)
    except (SyntaxError, UnicodeDecodeError, ValueError):
        return {}

    imports = []
    functions = []
    classes = []
    calls = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                resolved = _resolve_import(node.module, file_path, repo_root, level=node.level)
                imports.append(resolved)
        elif isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
            qualified = f"{file_path}::{node.name}"
            functions.append(qualified)
        elif isinstance(node, ast.ClassDef):
            qualified = f"{file_path}::{node.name}"
            classes.append(qualified)
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                calls.append(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                calls.append(node.func.attr)

    return {
        "file": file_path,
        "imports": imports,
        "functions": functions,
        "classes": classes,
        "calls": calls,
    }
