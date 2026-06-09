import json
import sqlite3
from pathlib import Path
from typing import List


def _default_db_path() -> str:
    return str(Path(__file__).resolve().parent.parent.parent / "data" / "commits.db")


def save_commits(commits: List[dict], db_path: str = None) -> None:
    if db_path is None:
        db_path = _default_db_path()
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS commits (
            hash TEXT PRIMARY KEY,
            timestamp INTEGER,
            author TEXT,
            changed_files TEXT
        )
    """)
    for c in commits:
        conn.execute(
            "INSERT OR REPLACE INTO commits (hash, timestamp, author, changed_files) VALUES (?, ?, ?, ?)",
            (c["hash"], c["timestamp"], c["author"], json.dumps(c["changed_files"])),
        )
    conn.commit()
    conn.close()


def load_commits(db_path: str = None) -> List[dict]:
    if db_path is None:
        db_path = _default_db_path()
    conn = sqlite3.connect(db_path)
    rows = conn.execute("SELECT hash, timestamp, author, changed_files FROM commits ORDER BY timestamp").fetchall()
    conn.close()
    return [
        {
            "hash": r[0],
            "timestamp": r[1],
            "author": r[2],
            "changed_files": json.loads(r[3]),
        }
        for r in rows
    ]
