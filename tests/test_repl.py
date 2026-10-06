"""Tests for the REPL loop."""

from unittest.mock import patch
from src.vfs import VFS
from src.repl import run_repl


def test_repl_exit_command():
    """Test REPL exits on exit command."""
    vfs = VFS("test")
    with patch("builtins.input", side_effect=["exit"]):
        run_repl(vfs)


def test_repl_empty_input():
    """Test REPL handles empty input."""
    vfs = VFS("test")
    with patch("builtins.input", side_effect=["", "exit"]):
        run_repl(vfs)


def test_repl_unknown_command(capsys):
    """Test REPL handles unknown command."""
    vfs = VFS("test")
    with patch("builtins.input", side_effect=["foobar", "exit"]):
        run_repl(vfs)
    captured = capsys.readouterr()
    assert "Unknown command" in captured.out