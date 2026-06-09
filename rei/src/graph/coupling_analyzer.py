import itertools
from collections import defaultdict

from rei.src.storage.commit_store import load_commits


def build_cochange_matrix(commits):
    matrix = defaultdict(int)
    file_change_counts = defaultdict(int)

    for commit in commits:
        files = [f for f in commit["changed_files"] if f.endswith(".py")]
        if len(files) < 2 or len(files) > 50:
            continue
        unique_files = list(dict.fromkeys(files))
        for f in unique_files:
            file_change_counts[f] += 1
        for a, b in itertools.combinations(sorted(unique_files), 2):
            matrix[(a, b)] += 1

    return dict(matrix), dict(file_change_counts)
