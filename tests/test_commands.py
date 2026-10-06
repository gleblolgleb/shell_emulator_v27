"""Tests for command handlers."""

from src.commands import execute, get_unknown_cmd_msg


def test_execute_ls(capsys):
    """Test ls stub command."""
    result = execute("ls", ["-l", "/tmp"])
    captured = capsys.readouterr()
    assert "ls" in captured.out
    assert result is False


def test_execute_cd(capsys):
    """Test cd stub command."""
    result = execute("cd", ["/home"])
    captured = capsys.readouterr()
    assert "cd" in captured.out
    assert result is False


def test_execute_exit():
    """Test exit command returns True."""
    result = execute("exit", [])
    assert result is True


def test_execute_unknown(capsys):
    """Test unknown command error message."""
    result = execute("foobar", [])
    captured = capsys.readouterr()
    assert "Unknown command" in captured.out
    assert result is False


def test_get_unknown_cmd_msg():
    """Test unknown command message format."""
    msg = get_unknown_cmd_msg("test_cmd")
    assert "test_cmd" in msg