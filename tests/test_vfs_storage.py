"""Tests for VFS storage module."""
import os
import tempfile
import zipfile
from src.vfs_storage import VFSStorage, FileMetadata


def _create_test_zip(
    path: str, files: dict[str, bytes]
) -> None:
    """Create a test ZIP archive with given files."""
    with zipfile.ZipFile(path, "w") as archive:
        for name, content in files.items():
            archive.writestr(name, content)


def test_load_from_zip():
    """Test loading VFS from ZIP archive."""
    with tempfile.NamedTemporaryFile(
        suffix=".zip", delete=False
    ) as f:
        zip_path = f.name
    try:
        _create_test_zip(
            zip_path, {"file1.txt": b"hello"}
        )
        storage = VFSStorage()
        storage.load_from_zip(zip_path)
        content = storage.get_file_content(
            "/file1.txt"
        )
        assert content == b"hello"
    finally:
        os.unlink(zip_path)


def test_load_from_zip_not_found():
    """Test error when ZIP file not found."""
    storage = VFSStorage()
    try:
        storage.load_from_zip("/nonexistent.zip")
        assert False, "Should raise FileNotFoundError"
    except FileNotFoundError:
        pass


def test_load_from_zip_invalid():
    """Test error when file is not a valid ZIP."""
    with tempfile.NamedTemporaryFile(
        suffix=".txt", delete=False
    ) as f:
        f.write(b"not a zip")
        txt_path = f.name
    try:
        storage = VFSStorage()
        try:
            storage.load_from_zip(txt_path)
            assert False, "Should raise ValueError"
        except ValueError:
            pass
    finally:
        os.unlink(txt_path)


def test_save_to_zip():
    """Test saving VFS to ZIP archive."""
    storage = VFSStorage()
    storage._files["/test.txt"] = b"world"
    storage._dirs.add("/folder")
    with tempfile.NamedTemporaryFile(
        suffix=".zip", delete=False
    ) as f:
        zip_path = f.name
    try:
        storage.save_to_zip(zip_path)
        assert os.path.exists(zip_path)
        with zipfile.ZipFile(
            zip_path, "r"
        ) as archive:
            names = archive.namelist()
            assert "test.txt" in names
    finally:
        os.unlink(zip_path)


def test_list_dir():
    """Test listing directory contents."""
    storage = VFSStorage()
    storage._files["/file1.txt"] = b"a"
    storage._files["/file2.txt"] = b"b"
    storage._dirs.add("/subdir")
    items = storage.list_dir("/")
    assert "file1.txt" in items
    assert "file2.txt" in items
    assert "subdir" in items


def test_change_dir():
    """Test changing current directory."""
    storage = VFSStorage()
    storage._dirs.add("/home")
    storage.change_dir("/home")
    assert storage.get_current_dir() == "/home"


def test_change_dir_not_found():
    """Test error when directory not found."""
    storage = VFSStorage()
    try:
        storage.change_dir("/nonexistent")
        assert False, "Should raise FileNotFoundError"
    except FileNotFoundError:
        pass


def test_get_file_size():
    """Test getting file size."""
    storage = VFSStorage()
    storage._files["/test.txt"] = b"hello"
    storage._metadata["/test.txt"] = FileMetadata(5)
    size = storage.get_file_size("/test.txt")
    assert size == 5


def test_get_vfs_hash():
    """Test VFS hash calculation."""
    storage = VFSStorage()
    storage._files["/test.txt"] = b"hello"
    hash1 = storage.get_vfs_hash()
    assert len(hash1) == 64
    storage._files["/test.txt"] = b"world"
    hash2 = storage.get_vfs_hash()
    assert hash1 != hash2
