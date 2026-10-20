"""Generate test VFS ZIP archives."""
import os
import zipfile


def create_minimal_vfs(path: str) -> None:
    """Create minimal VFS with one file and hidden file."""
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("readme.txt", "Hello VFS")
        archive.writestr(".hidden", "secret data")


def create_multiple_vfs(path: str) -> None:
    """Create VFS with multiple files."""
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("file1.txt", "Content 1")
        archive.writestr("file2.txt", "Content 2" * 100)
        archive.writestr("file3.txt", "Content 3")
        archive.writestr(".config", "config data")


def create_nested_vfs(path: str) -> None:
    """Create VFS with 3+ levels of folders."""
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("level1/", "")
        archive.writestr("level1/file.txt", "Level 1 file")
        archive.writestr("level1/.hidden", "hidden in level1")
        archive.writestr("level1/level2/", "")
        archive.writestr(
            "level1/level2/file.txt", "Level 2 file"
        )
        archive.writestr("level1/level2/level3/", "")
        archive.writestr(
            "level1/level2/level3/file.txt",
            "Level 3 file",
        )


def main() -> None:
    """Generate all test VFS archives."""
    os.makedirs("vfs_test", exist_ok=True)
    create_minimal_vfs("vfs_test/minimal.zip")
    create_multiple_vfs("vfs_test/multiple.zip")
    create_nested_vfs("vfs_test/nested.zip")
    print("Test VFS archives created in vfs_test/")


if __name__ == "__main__":
    main()