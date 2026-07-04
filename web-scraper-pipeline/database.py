import sqlite3
from datetime import datetime
from pathlib import Path

DB_FILE = Path(__file__).parent / "data" / "scraped_books.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    price REAL,
    rating INTEGER,
    availability TEXT,
    category TEXT,
    source_url TEXT,
    scraped_at TEXT
)
"""


def get_connection() -> sqlite3.Connection:
    DB_FILE.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    conn.execute(SCHEMA)
    return conn


def insert_item(conn: sqlite3.Connection, item: dict) -> None:
    conn.execute(
        "INSERT INTO books (title, price, rating, availability, category, source_url, scraped_at) "
        "VALUES (:title, :price, :rating, :availability, :category, :source_url, :scraped_at)",
        {**item, "scraped_at": datetime.now().isoformat(timespec="seconds")},
    )
    conn.commit()


def get_stats(conn: sqlite3.Connection) -> dict:
    count, avg_price, min_price, max_price = conn.execute(
        "SELECT COUNT(*), AVG(price), MIN(price), MAX(price) FROM books"
    ).fetchone()
    return {
        "count": count or 0,
        "avg_price": round(avg_price, 2) if avg_price else 0,
        "min_price": min_price or 0,
        "max_price": max_price or 0,
    }


def fetch_all(conn: sqlite3.Connection) -> list:
    cursor = conn.execute(
        "SELECT title, price, rating, availability, category, scraped_at "
        "FROM books ORDER BY id DESC"
    )
    columns = [d[0] for d in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def clear_all(conn: sqlite3.Connection) -> None:
    conn.execute("DELETE FROM books")
    conn.commit()
