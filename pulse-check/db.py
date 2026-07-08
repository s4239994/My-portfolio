import sqlite3
from datetime import datetime
from pathlib import Path

DB_FILE = Path(__file__).parent / "data" / "pulse.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS checkins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person TEXT NOT NULL,
    mood_label TEXT NOT NULL,
    mood_emoji TEXT NOT NULL,
    mood_score INTEGER NOT NULL,
    note TEXT,
    created_at TEXT NOT NULL
)
"""


def get_connection() -> sqlite3.Connection:
    DB_FILE.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    conn.execute(SCHEMA)
    return conn


def insert_checkin(conn: sqlite3.Connection, checkin: dict) -> None:
    conn.execute(
        "INSERT INTO checkins (person, mood_label, mood_emoji, mood_score, note, created_at) "
        "VALUES (:person, :mood_label, :mood_emoji, :mood_score, :note, :created_at)",
        checkin,
    )
    conn.commit()


def fetch_recent(conn: sqlite3.Connection, days: int = 7) -> list:
    cursor = conn.execute(
        "SELECT person, mood_label, mood_emoji, mood_score, note, created_at FROM checkins "
        "WHERE created_at >= datetime('now', ? ) ORDER BY created_at ASC",
        (f"-{days} days",),
    )
    columns = [d[0] for d in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def fetch_all(conn: sqlite3.Connection) -> list:
    cursor = conn.execute(
        "SELECT person, mood_label, mood_emoji, mood_score, note, created_at "
        "FROM checkins ORDER BY created_at ASC"
    )
    columns = [d[0] for d in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def clear_all(conn: sqlite3.Connection) -> None:
    conn.execute("DELETE FROM checkins")
    conn.commit()


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")
