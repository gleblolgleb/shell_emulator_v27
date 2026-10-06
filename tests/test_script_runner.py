"""Tests for startup script runner."""

import os
import tempfile
from src.script_runner import run_script


def _dummy_execute(name: str, args: list[str]) -> bool:
    """Dummy execute function for testing."""
    if name == "exit":
        return True
    print(f"exec: {name} {args}")
    return False


def _dummy_parse(line: str) -> tuple[str, list[str]]:
    """Dummy parse function for testing."""
    parts = line.split()
    if not parts:
        return "", []
    return parts[0], parts[1:]


def test_run_script_basic(capsys):
    """Test basic script execution."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".sh", delete=False
    ) as f:
        f.write("ls -la\ncd /home\n")
        f.flush()
        path = f.name

    try:
        run_script(path, _dummy_execute, _dummy_parse)
    finally:
        os.unlink(path)

    captured = capsys.readouterr()
    assert "> ls -la" in captured.out
    assert "exec: ls" in captured.out
    assert "> cd /home" in captured.out


def test_run_script_skips_comments(capsys):
    """Test that comments are skipped."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".sh", delete=False
    ) as f:
        f.write("# comment\nls\n")
        f.flush()
        path = f.name

    try:
        run_script(path, _dummy_execute, _dummy_parse)
    finally:
        os.unlink(path)

    captured = capsys.readouterr()
    assert "# comment" not in captured.out
    assert "> ls" in captured.out


def test_run_script_skips_empty_lines(capsys):
    """Test that empty lines are skipped."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".sh", delete=False
    ) as f:
        f.write("\n\nls\n\n")
        f.flush()
        path = f.name

    try:
        run_script(path, _dummy_execute, _dummy_parse)
    finally:
        os.unlink(path)

    captured = capsys.readouterr()
    assert captured.out.count(">") == 1


def test_run_script_file_not_found(capsys):
    """Test error when script file not found."""
    run_script(
        "/nonexistent/script.sh",
        _dummy_execute,
        _dummy_parse,
    )
    captured = capsys.readouterr()
    assert "Error" in captured.out


def test_run_script_skips_errors(capsys):
    """Test that erroneous lines are skipped."""

    def failing_execute(name, args):
        if name == "bad":
            raise ValueError("bad cmd")
        print(f"ok: {name}")
        return False

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".sh", delete=False
    ) as f:
        f.write("good\nbad\ngood2\n")
        f.flush()
        path = f.name

    try:
        run_script(path, failing_execute, _dummy_parse)
    finally:
        os.unlink(path)

    captured = capsys.readouterr()
    assert "ok: good" in captured.out
    assert "Error" in captured.out
    assert "ok: good2" in captured.out