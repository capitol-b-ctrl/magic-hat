"""SQLite database management and structured telemetry logging for Magic Hat."""

import sqlite3
import os
import json
from datetime import datetime
from magic_hat.utils import Colors

DB_PATH = os.path.expanduser("~/magic_hat_telemetry.db")

def get_connection():
    """Establish a connection to the SQLite telemetry database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database tables and ensure required columns exist."""
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
        # Safely add metadata_json column if an older database file exists
        cursor = conn.execute("PRAGMA table_info(scan_logs)")
        columns = [col["name"] for col in cursor.fetchall()]
        if "metadata_json" not in columns:
            conn.execute("ALTER TABLE scan_logs ADD COLUMN metadata_json TEXT")
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
