"""SQLite database management and telemetry logging for Magic Hat."""

import sqlite3
import os
import json
from datetime import datetime





DB_PATH = os.path.expanduser("~/Magic_Hat/src/magic_hat/data/magic_hat_telemetry.db")

def get_connection():
    """Establish a connection to the SQLite telemetry database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database tables with structured metadata columns."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS scan_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tool_name TEXT NOT NULL,
                target TEXT NOT NULL,
                metadata_json TEXT,
                output TEXT,
                timestamp TEXT NOT NULL
            )
        """)
        conn.commit()

def log_scan(tool_name, target, output, metadata=None):
    """Log scan results with raw output and structured metadata."""
    init_db()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    meta_str = json.dumps(metadata) if metadata else "{}"
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO scan_logs (tool_name, target, metadata_json, output, timestamp) VALUES (?, ?, ?, ?, ?)",
            (tool_name, target, meta_str, output, timestamp)
        )
        conn.commit()

def get_scan_logs():
    """Retrieve all logged scans."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, tool_name, target, timestamp FROM scan_logs ORDER BY id DESC")
        return [dict(row) for row in cursor.fetchall()]



#____________________________________



# Anchor database locally inside the package directory
PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PACKAGE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, "magic_hat.db")

def get_connection():
    """Create and return a SQLite database connection with row factory and auto-table creation."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    
    # Auto-initialize tables on every connection to prevent 'no such table' errors
    conn.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            supplier TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS scan_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tool_name TEXT NOT NULL,
            target TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            output TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn

def init_db():
    """Explicit database initialization helper."""
    with get_connection():
        pass

def save_item(name, price, supplier):
    """Save an inventory item to the database."""
    with get_connection() as conn:
        conn.execute("INSERT INTO items (name, price, supplier) VALUES (?, ?, ?)", (name, price, supplier))
        conn.commit()

def get_all_items():
    """Retrieve all inventory items."""
    with get_connection() as conn:
        cursor = conn.execute("SELECT * FROM items")
        return [dict(row) for row in cursor.fetchall()]

def search_items(query):
    """Search inventory items by keyword."""
    with get_connection() as conn:
        cursor = conn.execute("SELECT * FROM items WHERE name LIKE ? OR supplier LIKE ?", (f"%{query}%", f"%{query}%"))
        return [dict(row) for row in cursor.fetchall()]

def calculate_budget():
    """Calculate total cost of all inventory items."""
    with get_connection() as conn:
        cursor = conn.execute("SELECT SUM(price) as total FROM items")
        row = cursor.fetchone()
        return row["total"] if row["total"] else 0.0

def log_scan(tool_name, target, output):
    """Log tool execution telemetry into SQLite."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        conn.execute("INSERT INTO scan_logs (tool_name, target, timestamp, output) VALUES (?, ?, ?, ?)", 
                     (tool_name, target, timestamp, output))
        conn.commit()

def get_scan_logs():
    """Retrieve all past scan logs summary with their database IDs."""
    with get_connection() as conn:
        cursor = conn.execute("SELECT id, tool_name, target, timestamp FROM scan_logs ORDER BY id DESC")
        return [dict(row) for row in cursor.fetchall()]
