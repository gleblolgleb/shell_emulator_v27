"""Tests for the command parser."""

import os
from src.parser import expand_env_vars, parse_command


def test_expand_simple_var():
    """Test expansion of simple $VAR."""
    os.environ["TEST_VAR"] = "hello"
    result = expand_env_vars("$TEST_VAR")
    assert result == "hello"
    del os.environ["TEST_VAR"]


def test_expand_braced_var():
    """Test expansion of ${VAR}."""
    os.environ["TEST_VAR"] = "world"
    result = expand_env_vars("${TEST_VAR}")
    assert result == "world"
    del os.environ["TEST_VAR"]


def test_expand_missing_var():
    """Test expansion of missing variable."""
    result = expand_env_vars("$NONEXISTENT_VAR_XYZ")
    assert result == ""


def test_parse_simple_command():
    """Test parsing simple command without args."""
    name, args = parse_command("ls")
    assert name == "ls"
    assert args == []


def test_parse_command_with_args():
    """Test parsing command with arguments."""
    name, args = parse_command("cd /home/user")
    assert name == "cd"
    assert args == ["/home/user"]


def test_parse_quoted_args():
    """Test parsing with quoted arguments."""
    name, args = parse_command('ls "my folder"')
    assert name == "ls"
    assert args == ["my folder"]


def test_parse_empty_line():
    """Test parsing empty line."""
    name, args = parse_command("")
    assert name == ""
    assert args == []
def test_expand_windows_vars():
    """Test expansion of Windows environment variables."""
    import os
    userprofile = os.environ.get("USERPROFILE", "")
    username = os.environ.get("USERNAME", "")
    result = expand_env_vars("$USERPROFILE/$USERNAME")
    expected = f"{userprofile}/{username}"
    assert result == expected