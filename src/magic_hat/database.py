"""SQLite database management and structured telemetry logging for Magic Hat."""

import sqlite3
import os
import json
from datetime import datetime
from magic_hat.utils import Colors

DB_PATH = os.path.expanduser("~/Magic_Hat/src/magic_hat/data/magic_hat.db")

def init_db():
    """Initialize the SQLite database and ensure schema is up to date."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Drop old table to enforce fresh schema during active development
    cursor.execute('DROP TABLE IF EXISTS scan_logs')
    cursor.execute('''
        CREATE TABLE scan_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            scan_type TEXT,
            target TEXT,
            output TEXT,
            metadata TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_scan_result(scan_type, target, output, metadata=None):
    """Logs scan results or remote telemetry into the SQLite database."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Safely convert dict/list metadata into JSON string if provided
    meta_str = json.dumps(metadata) if metadata is not None else None
    
    cursor.execute('''
        INSERT INTO scan_logs (scan_type, target, output, metadata)
        VALUES (?, ?, ?, ?)
    ''', (scan_type, target, output, meta_str))
    conn.commit()
    conn.close()

# Alias log_scan to log_scan_result
log_scan = log_scan_result

def get_scan_logs():
    """Retrieve all logged scan results from the database."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, timestamp, scan_type, target, output FROM scan_logs ORDER BY timestamp DESC')
    rows = cursor.fetchall()
    conn.close()
    
    # Format rows into standard list of dictionaries
    logs = []
    for row in rows:
        logs.append({
            'id': row[0],
            'timestamp': row[1],
            'tool_name': row[2],
            'target': row[3],
            'output': row[4]
        })
    return logs

def get_connection():
    """Return a direct sqlite3 connection for custom queries."""
    init_db()
    return sqlite3.connect(DB_PATH)