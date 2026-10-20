"""Tests for command handlers."""
from src.commands import execute, get_unknown_cmd_msg
from src.vfs_storage import VFSStorage


def _make_storage() -> VFSStorage:
    """Create empty VFS storage for tests."""
    return VFSStorage()


def test_execute_ls(capsys):
    """Test ls stub command."""
    result = execute("ls", ["-l", "/tmp"], _make_storage())
    captured = capsys.readouterr()
    assert "ls" in captured.out
    assert result is False


def test_execute_cd(capsys):
    """Test cd stub command."""
    result = execute("cd", ["/home"], _make_storage())
    captured = capsys.readouterr()
    assert "cd" in captured.out
    assert result is False


def test_execute_exit():
    """Test exit command returns True."""
    result = execute("exit", [], _make_storage())
    assert result is True


def test_execute_unknown(capsys):
    """Test unknown command error message."""
    result = execute("foobar", [], _make_storage())
    captured = capsys.readouterr()
    assert "Unknown command" in captured.out
    assert result is False


def test_get_unknown_cmd_msg():
    """Test unknown command message format."""
    msg = get_unknown_cmd_msg("test_cmd")
    assert "test_cmd" in msg
