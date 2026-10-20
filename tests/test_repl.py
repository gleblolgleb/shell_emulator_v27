"""Tests for the REPL loop."""
from unittest.mock import patch
from src.vfs import VFS
from src.vfs_storage import VFSStorage
from src.repl import run_repl


def _make_storage() -> VFSStorage:
    """Create empty VFS storage for tests."""
    return VFSStorage()


def test_repl_exit_command():
    """Test REPL exits on exit command."""
    vfs = VFS("test")
    with patch("builtins.input", side_effect=["exit"]):
        run_repl(vfs, _make_storage())


def test_repl_empty_input():
    """Test REPL handles empty input."""
    vfs = VFS("test")
    with patch("builtins.input", side_effect=["", "exit"]):
        run_repl(vfs, _make_storage())


def test_repl_unknown_command(capsys):
    """Test REPL handles unknown command."""
    vfs = VFS("test")
    with patch(
        "builtins.input", side_effect=["foobar", "exit"]
    ):
        run_repl(vfs, _make_storage())
    captured = capsys.readouterr()
    assert "Unknown command" in captured.out
