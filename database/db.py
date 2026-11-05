import sqlite3
import os

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
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    amount REAL NOT NULL,
                    category TEXT NOT NULL,
                    description TEXT,
                    date DATE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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
            # Sample user (Password is 'password123' in plain text for simplicity in seed,
            # but in real app should be hashed)
            conn.execute(
                "INSERT OR IGNORE INTO users (id, username, password) VALUES (?, ?, ?)",
                (1, "testuser", "password123")
            )

            # Sample expenses for user 1
            expenses = [
                (1, 25.50, "Food", "Lunch at Cafe", "2023-10-01"),
                (1, 15.00, "Transport", "Bus ticket", "2023-10-02"),
                (1, 120.00, "Utilities", "Electricity bill", "2023-10-03"),
                (1, 45.00, "Entertainment", "Movie ticket", "2023-10-04"),
                (1, 12.99, "Subscriptions", "Music streaming", "2023-10-05"),
            ]
            conn.executemany(
                "INSERT INTO expenses (user_id, amount, category, description, date) VALUES (?, ?, ?, ?, ?)",
                expenses
            )
    except sqlite3.IntegrityError:
        # Handle cases where data already exists
        pass
    finally:
        conn.close()
