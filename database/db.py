import sqlite3
import os
from werkzeug.security import generate_password_hash

DB_PATH = "spendly.db"

def get_db():
    """Returns a SQLite connection with row_factory and foreign keys enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    """Creates all tables using CREATE TABLE IF NOT EXISTS."""
    conn = get_db()
    try:
        with conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TEXT DEFAULT (datetime('now'))
                );
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
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                );
            """)
    finally:
        conn.close()

def seed_db():
    """Inserts sample data for development."""
    conn = get_db()
    try:
        with conn:
            # Check if users table already has data to prevent duplication
            user = conn.execute("SELECT id FROM users LIMIT 1").fetchone()
            if user:
                return

            # Demo User
            demo_user_id = 1
            hashed_password = generate_password_hash("demo123")
            conn.execute(
                "INSERT INTO users (id, name, email, password_hash) VALUES (?, ?, ?, ?)",
                (demo_user_id, "Demo User", "demo@spendly.com", hashed_password)
            )

            # Sample expenses - 8 entries covering all required categories
            # Categories: Food, Transport, Bills, Health, Entertainment, Shopping, Other
            expenses = [
                (demo_user_id, 12.50, "Food", "2023-11-01", "Lunch at Cafe"),
                (demo_user_id, 5.00, "Transport", "2023-11-02", "Bus fare"),
                (demo_user_id, 80.00, "Bills", "2023-11-03", "Electricity bill"),
                (demo_user_id, 40.00, "Health", "2023-11-04", "Pharmacy"),
                (demo_user_id, 15.00, "Entertainment", "2023-11-05", "Movie ticket"),
                (demo_user_id, 60.00, "Shopping", "2023-11-06", "New shirt"),
                (demo_user_id, 20.00, "Other", "2023-11-07", "Gift wrap"),
                (demo_user_id, 30.00, "Food", "2023-11-08", "Dinner party"),
            ]
            conn.executemany(
                "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
                expenses
            )
    except sqlite3.IntegrityError as e:
        print(f"Seed error: {e}")
    finally:
        conn.close()
