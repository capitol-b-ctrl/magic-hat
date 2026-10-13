"""Unit tests targeting database logic."""

from magic_hat.database import calculate_budget

def test_calculate_budget_initial():
    """Test initial state of budget calculation."""
    assert calculate_budget() == 0.0
