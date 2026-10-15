python


"""Database and data handling module for Magic Hat using SQLite."""

import sqlite3
import os
from datetime import datetime

# Store the database file in the user's home directory for persistence
DB_PATH = os.path.expanduser("~/.magic_hat.db")

def get_connection():
    """Establish a database connection and return row objects as dictionaries."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database tables if they don't exist."""
    with get_connection() as conn:
        # Original inventory table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                supplier TEXT NOT NULL
            )
        """)
        # Scan logging table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS scan_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tool_name TEXT NOT NULL,
                target TEXT NOT NULL,
                output TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)
        conn.commit()

# Initialize tables when the module loads
init_db()

# --- Inventory Functions ---

def save_item(name, price, supplier):
    """Save an item to the SQLite database."""
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO items (name, price, supplier) VALUES (?, ?, ?)",
            (name, price, supplier)
        )
        conn.commit()

def get_all_items():
    """Retrieve all items from the SQLite database."""
    with get_connection() as conn:
        cursor = conn.execute("SELECT name, price, supplier FROM items ORDER BY id DESC")
        return [dict(row) for row in cursor.fetchall()]

def search_items(query):
    """Search items by keyword in name or supplier."""
    with get_connection() as conn:
        pattern = f"%{query}%"
        cursor = conn.execute(
            "SELECT name, price, supplier FROM items WHERE name LIKE ? OR supplier LIKE ? ORDER BY id DESC",
            (pattern, pattern)
        )
        return [dict(row) for row in cursor.fetchall()]

def calculate_budget():
    """Calculate the total budget sum of all items."""
    with get_connection() as conn:
        cursor = conn.execute("SELECT SUM(price) FROM items")
        result = cursor.fetchone()[0]
        return float(result) if result is not None else 0.0

# --- Pentest Log Functions ---

def log_scan(tool_name, target, output):
    """Save tool execution output to the database."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO scan_logs (tool_name, target, output, timestamp) VALUES (?, ?, ?, ?)",
            (tool_name, target, output, timestamp)
        )
        conn.commit()

def get_scan_logs():
    """Retrieve all past scan logs summary with their database IDs."""
    with get_connection() as conn:
        cursor = conn.execute("SELECT id, tool_name, target, timestamp FROM scan_logs ORDER BY id DESC")
        return [dict(row) for row in cursor.fetchall()]


