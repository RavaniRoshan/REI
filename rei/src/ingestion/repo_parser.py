import os
import re
import tempfile
from pathlib import Path

from git import Repo as GitRepo


def _is_remote(path: str) -> bool:
    return path.startswith("http://") or path.startswith("https://") or path.startswith("git@")


def _repo_name_from_url(url: str) -> str:
    name = url.rstrip("/").split("/")[-1]
    name = re.sub(r"\.git$", "", name)
    return name


def parse_repo(path: str, data_dir: str = None) -> dict:
    if data_dir is None:
        data_dir = str(Path(__file__).resolve().parent.parent.parent / "data")

    if _is_remote(path):
        repo_name = _repo_name_from_url(path)
        clone_dir = os.path.join(data_dir, "tmp", repo_name)
        os.makedirs(clone_dir, exist_ok=True)
        if os.path.isdir(os.path.join(clone_dir, ".git")):
            repo = GitRepo(clone_dir)
            repo.remotes.origin.pull()
        else:
            GitRepo.clone_from(path, clone_dir)
        repo_root = clone_dir
    else:
        repo_root = os.path.abspath(path)

    python_files = []
    for root, dirs, files in os.walk(repo_root):
        dirs[:] = [d for d in dirs if d != ".git" and d != "__pycache__"]
        for f in files:
            if f.endswith(".py"):
                rel = os.path.relpath(os.path.join(root, f), repo_root).replace("\\", "/")
                python_files.append(rel)

    return {
        "root": repo_root,
        "python_files": sorted(python_files),
        "total_files": len(python_files),
    }
