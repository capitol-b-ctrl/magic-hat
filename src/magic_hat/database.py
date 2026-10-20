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

# Database path stored locally in project directory
DB_PATH = os.path.expanduser("~/Magic_Hat/magic_hat.db")

def init_db():
    """Initialize the SQLite database and required tables if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scan_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            scan_type TEXT,
            target TEXT,
            output TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_scan_result(scan_type, target, output):
    """Logs scan results or remote telemetry into the SQLite database."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO scan_logs (scan_type, target, output)
        VALUES (?, ?, ?)
    ''', (scan_type, target, output))
    conn.commit()
    conn.close()
    
    
def get_scan_logs():
    """Retrieve all logged scans."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, tool_name, target, timestamp FROM scan_logs ORDER BY id DESC")
        return [dict(row) for row in cursor.fetchall()]

def clear_scan_logs():
    """Purge all scan logs and telemetry records from the database."""
    init_db()
    with get_connection() as conn:
        conn.execute("DELETE FROM scan_logs")
        conn.execute("DELETE FROM sqlite_sequence WHERE name='scan_logs'")
        conn.commit()
