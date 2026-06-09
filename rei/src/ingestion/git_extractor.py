from typing import List

from git import Repo as GitRepo


def _get_default_branch(repo: GitRepo) -> str:
    for name in ("main", "master"):
        try:
            repo.rev_parse(f"refs/heads/{name}")
            return name
        except Exception:
            continue
    heads = [h.name for h in repo.heads]
    if heads:
        return heads[0]
    return "main"


def extract_history(repo_path: str, max_commits: int = None) -> List[dict]:
    repo = GitRepo(repo_path)
    branch = _get_default_branch(repo)
    try:
        repo.git.checkout(branch)
    except Exception:
        pass

    commits = []
    for commit in repo.iter_commits(branch):
        if max_commits is not None and len(commits) >= max_commits:
            break
        if len(commit.parents) > 1:
            continue
        changed_files = list(commit.stats.files.keys())
        commits.append({
            "hash": commit.hexsha,
            "timestamp": commit.committed_date,
            "author": str(commit.author),
            "changed_files": changed_files,
        })
    return commits
