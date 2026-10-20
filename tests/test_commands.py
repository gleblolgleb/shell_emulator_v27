"""Tests for command handlers."""
import os
import tempfile
from src.vfs_storage import VFSStorage, FileMetadata
from src.commands import execute, get_unknown_cmd_msg


def _make_storage() -> VFSStorage:
    """Create VFS storage with test data."""
    storage = VFSStorage()
    storage._files["/file1.txt"] = b"hello"
    storage._files["/file2.txt"] = b"world" * 100
    storage._files["/.hidden"] = b"secret"
    storage._metadata["/file1.txt"] = FileMetadata(5)
    storage._metadata["/file2.txt"] = FileMetadata(500)
    storage._metadata["/.hidden"] = FileMetadata(6)
    storage._dirs.add("/subdir")
    return storage


def test_execute_ls(capsys):
    """Test ls command without flags."""
    storage = _make_storage()
    execute("ls", [], storage)
    captured = capsys.readouterr()
    assert "file1.txt" in captured.out
    assert "file2.txt" in captured.out
    assert ".hidden" not in captured.out


def test_execute_ls_all(capsys):
    """Test ls -a shows hidden files."""
    storage = _make_storage()
    execute("ls", ["-a"], storage)
    captured = capsys.readouterr()
    assert ".hidden" in captured.out


def test_execute_ls_long(capsys):
    """Test ls -l shows detailed info."""
    storage = _make_storage()
    execute("ls", ["-l"], storage)
    captured = capsys.readouterr()
    assert "file1.txt" in captured.out
    assert "5" in captured.out


def test_execute_ls_human(capsys):
    """Test ls -lh shows human-readable size."""
    storage = _make_storage()
    execute("ls", ["-lh"], storage)
    captured = capsys.readouterr()
    assert "file2.txt" in captured.out
    assert "K" in captured.out or "B" in captured.out


def test_execute_ls_combined_flags(capsys):
    """Test ls with combined flags like -la."""
    storage = _make_storage()
    execute("ls", ["-la"], storage)
    captured = capsys.readouterr()
    assert ".hidden" in captured.out
    assert "file1.txt" in captured.out


def test_execute_cd(capsys):
    """Test cd command changes directory."""
    storage = _make_storage()
    execute("cd", ["/subdir"], storage)
    assert storage.get_current_dir() == "/subdir"


def test_execute_cd_not_found(capsys):
    """Test cd to nonexistent directory."""
    storage = _make_storage()
    execute("cd", ["/nonexistent"], storage)
    captured = capsys.readouterr()
    assert "Error" in captured.out


def test_execute_exit():
    """Test exit command returns True."""
    storage = _make_storage()
    result = execute("exit", [], storage)
    assert result is True


def test_execute_uptime(capsys):
    """Test uptime command shows seconds."""
    storage = _make_storage()
    execute("uptime", [], storage)
    captured = capsys.readouterr()
    assert "up" in captured.out
    assert "seconds" in captured.out


def test_execute_echo(capsys):
    """Test echo command prints arguments."""
    storage = _make_storage()
    execute("echo", ["hello", "world"], storage)
    captured = capsys.readouterr()
    assert "hello world" in captured.out


def test_execute_vfs_save(capsys):
    """Test vfs-save command."""
    storage = _make_storage()
    with tempfile.NamedTemporaryFile(
        suffix=".zip", delete=False
    ) as f:
        path = f.name
    try:
        execute("vfs-save", [path], storage)
        captured = capsys.readouterr()
        assert "VFS saved" in captured.out
        assert os.path.exists(path)
    finally:
        os.unlink(path)


def test_execute_vfs_save_no_args(capsys):
    """Test vfs-save without arguments."""
    storage = _make_storage()
    execute("vfs-save", [], storage)
    captured = capsys.readouterr()
    assert "Error" in captured.out


def test_execute_unknown(capsys):
    """Test unknown command error message."""
    storage = _make_storage()
    execute("foobar", [], storage)
    captured = capsys.readouterr()
    assert "Unknown command" in captured.out


def test_get_unknown_cmd_msg():
    """Test unknown command message format."""
    msg = get_unknown_cmd_msg("test_cmd")
    assert "test_cmd" in msg
