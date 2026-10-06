"""Tests for the VFS module."""

from src.vfs import VFS


def test_vfs_default_name():
    """Test VFS default name."""
    vfs = VFS()
    assert vfs.get_name() == "my_vfs"


def test_vfs_custom_name():
    """Test VFS with custom name."""
    vfs = VFS("test_vfs")
    assert vfs.get_name() == "test_vfs"


def test_vfs_none_name():
    """Test VFS with None name uses default."""
    vfs = VFS(None)
    assert vfs.get_name() == "my_vfs"