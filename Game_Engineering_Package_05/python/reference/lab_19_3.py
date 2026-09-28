"""SQLite is the no-server lab backend, not a substitute for PostgreSQL semantics."""
import sqlite3
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS players (
    id TEXT PRIMARY KEY NOT NULL, name TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS inventory (
    player_id TEXT NOT NULL REFERENCES players(id),
    item_id TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK(typeof(quantity)='integer'
                                   AND quantity BETWEEN 0 AND 1000000),
    PRIMARY KEY(player_id, item_id)
);
CREATE TABLE IF NOT EXISTS operations (
    id TEXT PRIMARY KEY NOT NULL, payload TEXT NOT NULL, response TEXT NOT NULL
);
"""

def connect_store(path: str | Path = ":memory:") -> sqlite3.Connection:
    # Explicit SQL BEGIN/COMMIT below; avoid implicit transaction ambiguity.
    db = sqlite3.connect(str(path), isolation_level=None, timeout=1.0)
    db.execute("PRAGMA foreign_keys = ON")
    db.executescript(SCHEMA)
    return db

def seed_inventory(db: sqlite3.Connection) -> None:
    db.execute("BEGIN IMMEDIATE")
    try:
        db.executemany("INSERT INTO players(id,name) VALUES (?,?)", [("A","Ada"),("B","Bo")])
        db.executemany("INSERT INTO inventory VALUES (?,?,?)", [("A","ore",20),("B","ore",3)])
        db.execute("COMMIT")
    except BaseException:
        if db.in_transaction:
            db.execute("ROLLBACK")
        raise
