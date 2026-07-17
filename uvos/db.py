import sqlite3
from datetime import datetime
from pathlib import Path

DB_FILE = Path(__file__).parent / "data" / "sessions.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT NOT NULL,
    skin_type TEXT NOT NULL,
    uv_index REAL NOT NULL,
    burn_time_minutes REAL,
    elapsed_minutes REAL NOT NULL,
    exceeded_budget INTEGER NOT NULL,
    logged_at TEXT NOT NULL
)
"""


def get_connection() -> sqlite3.Connection:
    DB_FILE.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    conn.execute(SCHEMA)
    return conn


def log_session(conn: sqlite3.Connection, entry: dict) -> None:
    conn.execute(
        "INSERT INTO sessions (city, skin_type, uv_index, burn_time_minutes, "
        "elapsed_minutes, exceeded_budget, logged_at) VALUES "
        "(:city, :skin_type, :uv_index, :burn_time_minutes, :elapsed_minutes, "
        ":exceeded_budget, :logged_at)",
        entry,
    )
    conn.commit()


def fetch_history(conn: sqlite3.Connection) -> list:
    cursor = conn.execute(
        "SELECT city, skin_type, uv_index, burn_time_minutes, elapsed_minutes, "
        "exceeded_budget, logged_at FROM sessions ORDER BY logged_at DESC"
    )
    columns = [d[0] for d in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")
