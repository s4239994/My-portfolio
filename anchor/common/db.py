import sqlite3
from datetime import datetime
from pathlib import Path

DB_FILE = Path(__file__).parent.parent / "data" / "anchor.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS plan_meta (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    metaphor TEXT,
    future_message TEXT
);

CREATE TABLE IF NOT EXISTS warning_signs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS coping_strategies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS trusted_contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    relationship TEXT,
    phone TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS reasons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS mood_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mood INTEGER NOT NULL,
    note TEXT,
    logged_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS growth_reflections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    logged_at TEXT NOT NULL
);
"""

METAPHORS = {
    "storm": {"label": "A storm", "emoji": "\U0001F329", "color": "#5b6b8c"},
    "fog": {"label": "A fog", "emoji": "\U0001F32B", "color": "#8b93a1"},
    "wave": {"label": "A wave", "emoji": "\U0001F30A", "color": "#4a7fa5"},
    "static": {"label": "Static noise", "emoji": "\U0001F4FB", "color": "#7a6b8c"},
    "weight": {"label": "A weight", "emoji": "\U0001FAA8", "color": "#6b6b6b"},
}


def get_connection() -> sqlite3.Connection:
    DB_FILE.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    conn.executescript(SCHEMA)
    return conn


def get_meta(conn) -> dict:
    row = conn.execute("SELECT metaphor, future_message FROM plan_meta WHERE id = 1").fetchone()
    if not row:
        return {"metaphor": None, "future_message": ""}
    return {"metaphor": row[0], "future_message": row[1] or ""}


def set_meta(conn, metaphor: str = None, future_message: str = None):
    current = get_meta(conn)
    new_metaphor = metaphor if metaphor is not None else current["metaphor"]
    new_message = future_message if future_message is not None else current["future_message"]
    conn.execute(
        "INSERT INTO plan_meta (id, metaphor, future_message) VALUES (1, ?, ?) "
        "ON CONFLICT(id) DO UPDATE SET metaphor = excluded.metaphor, future_message = excluded.future_message",
        (new_metaphor, new_message),
    )
    conn.commit()


def _list(conn, table: str) -> list:
    rows = conn.execute(f"SELECT id, text FROM {table} ORDER BY id").fetchall()
    return [{"id": r[0], "text": r[1]} for r in rows]


def _add(conn, table: str, text: str):
    conn.execute(f"INSERT INTO {table} (text) VALUES (?)", (text,))
    conn.commit()


def _delete(conn, table: str, item_id: int):
    conn.execute(f"DELETE FROM {table} WHERE id = ?", (item_id,))
    conn.commit()


def list_warning_signs(conn): return _list(conn, "warning_signs")
def add_warning_sign(conn, text): _add(conn, "warning_signs", text)
def delete_warning_sign(conn, item_id): _delete(conn, "warning_signs", item_id)

def list_coping_strategies(conn): return _list(conn, "coping_strategies")
def add_coping_strategy(conn, text): _add(conn, "coping_strategies", text)
def delete_coping_strategy(conn, item_id): _delete(conn, "coping_strategies", item_id)

def list_reasons(conn): return _list(conn, "reasons")
def add_reason(conn, text): _add(conn, "reasons", text)
def delete_reason(conn, item_id): _delete(conn, "reasons", item_id)

def list_goals(conn): return _list(conn, "goals")
def add_goal(conn, text): _add(conn, "goals", text)
def delete_goal(conn, item_id): _delete(conn, "goals", item_id)


def list_contacts(conn) -> list:
    rows = conn.execute("SELECT id, name, relationship, phone FROM trusted_contacts ORDER BY id").fetchall()
    return [{"id": r[0], "name": r[1], "relationship": r[2], "phone": r[3]} for r in rows]


def add_contact(conn, name: str, relationship: str, phone: str):
    conn.execute(
        "INSERT INTO trusted_contacts (name, relationship, phone) VALUES (?, ?, ?)",
        (name, relationship, phone),
    )
    conn.commit()


def delete_contact(conn, item_id: int): _delete(conn, "trusted_contacts", item_id)


def log_mood(conn, mood: int, note: str = ""):
    conn.execute(
        "INSERT INTO mood_log (mood, note, logged_at) VALUES (?, ?, ?)",
        (mood, note, datetime.now().isoformat(timespec="seconds")),
    )
    conn.commit()


def list_mood_log(conn, limit: int = 30) -> list:
    rows = conn.execute(
        "SELECT mood, note, logged_at FROM mood_log ORDER BY logged_at DESC LIMIT ?", (limit,)
    ).fetchall()
    return [{"mood": r[0], "note": r[1], "logged_at": r[2]} for r in rows]


def add_growth_reflection(conn, text: str):
    conn.execute(
        "INSERT INTO growth_reflections (text, logged_at) VALUES (?, ?)",
        (text, datetime.now().isoformat(timespec="seconds")),
    )
    conn.commit()


def list_growth_reflections(conn) -> list:
    rows = conn.execute(
        "SELECT text, logged_at FROM growth_reflections ORDER BY logged_at DESC"
    ).fetchall()
    return [{"text": r[0], "logged_at": r[1]} for r in rows]


def plan_is_complete(conn) -> bool:
    meta = get_meta(conn)
    return bool(
        meta["metaphor"]
        and list_warning_signs(conn)
        and list_coping_strategies(conn)
        and list_reasons(conn)
    )
