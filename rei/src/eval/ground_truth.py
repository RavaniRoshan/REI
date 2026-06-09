SPLIT_DATE = 1672531200  # 2023-01-01 00:00:00 UTC


def build_ground_truth(commits, split_date=None):
    if split_date is None:
        split_date = SPLIT_DATE
    train_commits = [c for c in commits if c["timestamp"] < split_date]
    test_commits = [c for c in commits if c["timestamp"] >= split_date]
    test_cases = []
    for commit in test_commits:
        files = commit["changed_files"]
        if len(files) < 2 or len(files) > 20:
            continue
        query = files[0]
        actual = files[1:]
        test_cases.append({"query": query, "actual": actual})
    return {"train": train_commits, "test": test_cases}
