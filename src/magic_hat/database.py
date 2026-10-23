"""SQLite database management and structured telemetry logging for Magic Hat."""

import sqlite3
import os
import json
from datetime import datetime
from magic_hat.utils import Colors

DB_PATH = os.path.expanduser("~/Magic_Hat/src/magic_hat/data/magic_hat.db")


def init_db():
    """Initialize the SQLite database, ensuring table exists and schema is migrated."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scan_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            tool_name TEXT,
            target TEXT,
            output TEXT,
            metadata TEXT
        )
    ''')
    
    # 2. Inspect existing columns to auto-migrate old databases
    cursor.execute("PRAGMA table_info(scan_logs)")
    columns = [row[1] for row in cursor.fetchall()]
    
    # Migrate 'scan_type' -> 'tool_name' if old column exists
    if "tool_name" not in columns:
        if "scan_type" in columns:
            try:
                cursor.execute("ALTER TABLE scan_logs RENAME COLUMN scan_type TO tool_name")
            except Exception:
                cursor.execute("ALTER TABLE scan_logs ADD COLUMN tool_name TEXT")
                cursor.execute("UPDATE scan_logs SET tool_name = scan_type")
        else:
            cursor.execute("ALTER TABLE scan_logs ADD COLUMN tool_name TEXT")
            
    # Migrate 'metadata_json' -> 'metadata'
    if "metadata" not in columns:
        if "metadata_json" in columns:
            try:
                cursor.execute("ALTER TABLE scan_logs RENAME COLUMN metadata_json TO metadata")
            except Exception:
                cursor.execute("ALTER TABLE scan_logs ADD COLUMN metadata TEXT")
                cursor.execute("UPDATE scan_logs SET metadata = metadata_json")
        else:
            cursor.execute("ALTER TABLE scan_logs ADD COLUMN metadata TEXT")

    if "target" not in columns:
        cursor.execute("ALTER TABLE scan_logs ADD COLUMN target TEXT")
        
    if "output" not in columns:
        cursor.execute("ALTER TABLE scan_logs ADD COLUMN output TEXT")
        
    conn.commit()
    conn.close()


def get_connection():
    """Return a direct sqlite3 connection with Row factory for dict-like column access."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def log_scan_result(tool_name, target, output, metadata=None):
    """Logs scan results or remote telemetry into the SQLite database safely."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    meta_str = json.dumps(metadata) if metadata is not None else None
    
    cursor.execute("PRAGMA table_info(scan_logs)")
    columns = [row[1] for row in cursor.fetchall()]
    
    target_tool_col = "tool_name" if "tool_name" in columns else "scan_type"
    target_meta_col = "metadata" if "metadata" in columns else "metadata_json"
    
    cursor.execute(f'''
        INSERT INTO scan_logs ({target_tool_col}, target, output, {target_meta_col})
        VALUES (?, ?, ?, ?)
    ''', (tool_name, target, output, meta_str))
    conn.commit()
    conn.close()


# Alias log_scan to log_scan_result for backward compatibility
log_scan = log_scan_result


def get_scan_logs():
    """Retrieve all logged scan results from the database safely."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("PRAGMA table_info(scan_logs)")
    columns = [row[1] for row in cursor.fetchall()]
    
    tool_col = "tool_name" if "tool_name" in columns else ("scan_type" if "scan_type" in columns else "'' AS tool_name")
    meta_col = "metadata" if "metadata" in columns else ("metadata_json" if "metadata_json" in columns else "'' AS metadata")
    
    query = f"SELECT id, timestamp, {tool_col} AS tool_name, target, output, {meta_col} AS metadata FROM scan_logs ORDER BY timestamp DESC"
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    
    logs = []
    for row in rows:
        logs.append({
            'id': row['id'],
            'timestamp': row['timestamp'],
            'tool_name': row['tool_name'],
            'target': row['target'],
            'output': row['output'],
            'metadata': row['metadata']
        })
    return logs


def clear_scan_logs():
    """Purge all scan logs from the database without deleting the table."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM scan_logs')
    conn.commit()
    conn.close()


def reset_database():
    """Hard-resets the database schema and recreates a fresh scan_logs table."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS scan_logs')
    cursor.execute('''
        CREATE TABLE scan_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            tool_name TEXT,
            target TEXT,
            output TEXT,
            metadata TEXT
        )
    ''')
    conn.commit()
    conn.close()
