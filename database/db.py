import os
import sqlite3
from calendar import monthrange
from datetime import date

from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "expense_tracker.db")

CATEGORIES = ["Food", "Transport", "Bills", "Health", "Entertainment", "Shopping", "Other"]


def get_db():
    """Open a new connection to the SQLite database.

    Row access is dict-like (sqlite3.Row) and foreign key enforcement is
    enabled for this connection. Caller is responsible for closing it.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create the users and expenses tables if they don't already exist."""
    conn = get_db()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now'))
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        conn.commit()
    finally:
        conn.close()


def seed_db():
    """Insert one demo user and 8 sample expenses, only if users is empty."""
    conn = get_db()
    try:
        existing = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        if existing > 0:
            return

        password_hash = generate_password_hash("demo123")
        cursor = conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            ("Demo User", "demo@spendly.com", password_hash),
        )
        user_id = cursor.lastrowid

        today = date.today()
        days_in_month = monthrange(today.year, today.month)[1]

        def day_of_month(day):
            return today.replace(day=min(day, days_in_month)).isoformat()

        expenses = [
            (user_id, 450.00, "Food",         day_of_month(2),  "Groceries"),
            (user_id, 120.50, "Transport",     day_of_month(4),  "Bus pass top-up"),
            (user_id, 1500.00, "Bills",        day_of_month(5),  "Electricity bill"),
            (user_id, 300.00, "Health",        day_of_month(9),  "Pharmacy"),
            (user_id, 600.00, "Entertainment", day_of_month(12), "Movie night"),
            (user_id, 899.00, "Shopping",      day_of_month(16), "New shoes"),
            (user_id, 250.75, "Food",          day_of_month(20), "Restaurant dinner"),
            (user_id, 100.00, "Other",         day_of_month(24), "Miscellaneous"),
        ]
        conn.executemany(
            "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
            expenses,
        )
        conn.commit()
    finally:
        conn.close()
