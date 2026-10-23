"""Unit tests targeting database logic for Magic Hat."""

import os
import tempfile
import pytest
from unittest.mock import patch
from magic_hat.database import (
    init_db,
    get_connection,
    log_scan_result,
    get_scan_logs,
    clear_scan_logs
)


@pytest.fixture(autouse=True)
def temp_db(tmp_path):
    """Isolate testing database to a temporary directory."""
    test_db_path = str(tmp_path / "test_magic_hat.db")
    with patch("magic_hat.database.DB_PATH", test_db_path):
        init_db()
        yield test_db_path


def test_init_db_creates_table():
    """Test that database initializes and creates scan_logs table without errors."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='scan_logs'")
        assert cursor.fetchone() is not None


def test_log_scan_and_retrieve():
    """Test logging a scan result and retrieving it."""
    log_scan_result("Nmap Recon", "192.168.1.1", "Port 80 open", {"os": "Linux"})
    logs = get_scan_logs()
    
    assert len(logs) == 1
    assert logs[0]["tool_name"] == "Nmap Recon"
    assert logs[0]["target"] == "192.168.1.1"
    assert "Port 80 open" in logs[0]["output"]
    assert "Linux" in logs[0]["metadata"]


def test_clear_scan_logs():
    """Test clearing all logs from the database."""
    log_scan_result("Ping Sweep", "192.168.1.0/24", "Host is up")
    assert len(get_scan_logs()) == 1
    
    clear_scan_logs()
    assert len(get_scan_logs()) == 0


def test_persistence_across_connections():
    """Verify logs are not dropped when new connections or init_db are called."""
    log_scan_result("Tool A", "10.0.0.1", "Output A")
    # Calling init_db again should NOT wipe existing records
    init_db()
    logs = get_scan_logs()
    assert len(logs) == 1
    assert logs[0]["target"] == "10.0.0.1"
