"""Virtual file system storage module."""
import base64
import hashlib
import time
import zipfile
from pathlib import Path


class FileMetadata:
    """Metadata for a file in VFS."""

    def __init__(self, size: int) -> None:
        """Initialize metadata with file size."""
        self.size = size
        self.created = time.time()
        self.modified = time.time()


class VFSStorage:
    """In-memory virtual file system storage."""

    def __init__(self) -> None:
        """Initialize empty VFS storage."""
        self._files: dict[str, bytes] = {}
        self._metadata: dict[str, FileMetadata] = {}
        self._dirs: set[str] = {"/"}
        self._current_dir = "/"

    def load_from_zip(self, path: str) -> None:
        """Load VFS structure from ZIP archive."""
        zip_path = Path(path)
        if not zip_path.exists():
            raise FileNotFoundError(
                f"VFS file not found: {path}"
            )
        if not zipfile.is_zipfile(zip_path):
            raise ValueError(
                f"Invalid VFS format: {path}"
            )
        with zipfile.ZipFile(zip_path, "r") as archive:
            for name in archive.namelist():
                full_path = "/" + name
                if name.endswith("/"):
                    self._dirs.add(full_path)
                else:
                    content = archive.read(name)
                    self._files[full_path] = content
                    self._metadata[full_path] = (
                        FileMetadata(len(content))
                    )
                    parent = self._get_parent(full_path)
                    self._dirs.add(parent)

    def save_to_zip(self, path: str) -> None:
        """Save VFS structure to ZIP archive."""
        with zipfile.ZipFile(path, "w") as archive:
            for dir_path in self._dirs:
                if dir_path != "/":
                    zip_name = dir_path.lstrip("/") + "/"
                    archive.writestr(zip_name, "")
            for file_path, content in self._files.items():
                zip_name = file_path.lstrip("/")
                encoded = base64.b64encode(content)
                archive.writestr(zip_name, encoded)

    def get_current_dir(self) -> str:
        """Return current working directory."""
        return self._current_dir

    def change_dir(self, path: str) -> None:
        """Change current working directory."""
        if path.startswith("/"):
            new_dir = path
        else:
            new_dir = self._join_path(
                self._current_dir, path
            )
        new_dir = self._normalize_path(new_dir)
        if new_dir not in self._dirs:
            raise FileNotFoundError(
                f"Directory not found: {new_dir}"
            )
        self._current_dir = new_dir

    def list_dir(self, path: str | None = None) -> list[str]:
        """List contents of directory."""
        if path is None:
            path = self._current_dir
        if path not in self._dirs:
            raise FileNotFoundError(
                f"Directory not found: {path}"
            )
        result: set[str] = set()
        if path == "/":
            prefix = "/"
        else:
            prefix = path if path.endswith("/") else path + "/"
        for file_path in self._files:
            if file_path.startswith(prefix):
                relative = file_path[len(prefix):]
                if "/" not in relative:
                    result.add(relative)
        for dir_path in self._dirs:
            if dir_path == path:
                continue
            if dir_path.startswith(prefix):
                relative = dir_path[len(prefix):]
                name = relative.rstrip("/")
                if "/" not in name:
                    result.add(name)
        return sorted(result)

    def get_file_content(self, path: str) -> bytes:
        """Get file content as bytes."""
        if path not in self._files:
            raise FileNotFoundError(
                f"File not found: {path}"
            )
        return self._files[path]

    def get_file_size(self, path: str) -> int:
        """Get file size in bytes."""
        if path in self._metadata:
            return self._metadata[path].size
        return 0

    def get_file_time(self, path: str) -> float:
        """Get file modification time."""
        if path in self._metadata:
            return self._metadata[path].modified
        return 0.0

    def get_vfs_hash(self) -> str:
        """Calculate SHA-256 hash of all VFS data."""
        hasher = hashlib.sha256()
        for file_path in sorted(self._files.keys()):
            hasher.update(file_path.encode())
            hasher.update(self._files[file_path])
        return hasher.hexdigest()

    def is_dir(self, path: str) -> bool:
        """Check if path is a directory."""
        if path == "/":
            return True
        if path.endswith("/"):
            return path in self._dirs
        return (
            path in self._dirs
            or (path + "/") in self._dirs
        )

    def is_file(self, path: str) -> bool:
        """Check if path is a file."""
        return path in self._files

    def _get_all_files_in_dir(
        self, dir_path: str
    ) -> list[str]:
        """Get all files recursively in a directory."""
        if not dir_path.endswith("/"):
            dir_path += "/"
        result = []
        for file_path in self._files:
            if file_path.startswith(dir_path):
                result.append(file_path)
        return result

    def _get_all_dirs_in_dir(
        self, dir_path: str
    ) -> list[str]:
        """Get all dirs recursively in a directory."""
        if not dir_path.endswith("/"):
            dir_path += "/"
        result = []
        for d in self._dirs:
            if d.startswith(dir_path):
                result.append(d)
        return result

    def copy_item(self, source: str, dest: str) -> None:
        """Copy file or directory within VFS."""
        source = self._normalize_path(source)
        dest = self._normalize_path(dest)

        if self.is_file(source):
            self._copy_file(source, dest)
        elif self.is_dir(source):
            self._copy_dir(source, dest)
        else:
            raise FileNotFoundError(
                f"Source not found: {source}"
            )

    def _copy_file(self, source: str, dest: str) -> None:
        """Copy a single file."""
        if self.is_dir(dest):
            if not dest.endswith("/"):
                dest += "/"
            file_name = source.split("/")[-1]
            dest = dest + file_name
        self._files[dest] = self._files[source]
        if source in self._metadata:
            self._metadata[dest] = self._metadata[source]
        parent = self._get_parent(dest)
        self._dirs.add(parent)

    def _copy_dir(self, source: str, dest: str) -> None:
        """Copy a directory and its contents."""
        if not source.endswith("/"):
            source += "/"
        if self.is_dir(dest):
            if not dest.endswith("/"):
                dest += "/"
            dir_name = source.rstrip("/").split("/")[-1]
            dest = dest + dir_name + "/"
        else:
            if not dest.endswith("/"):
                dest += "/"

        self._dirs.add(dest.rstrip("/"))

        for d in self._get_all_dirs_in_dir(source):
            relative = d[len(source):]
            self._dirs.add(dest + relative)

        for f in self._get_all_files_in_dir(source):
            relative = f[len(source):]
            new_f = dest + relative
            self._files[new_f] = self._files[f]
            if f in self._metadata:
                self._metadata[new_f] = self._metadata[f]

    def _get_parent(self, path: str) -> str:
        """Get parent directory path."""
        parts = path.rsplit("/", 1)
        if len(parts) == 1:
            return "/"
        parent = parts[0]
        return parent if parent else "/"

    def _join_path(self, base: str, relative: str) -> str:
        """Join base path with relative path."""
        if base.endswith("/"):
            return base + relative
        return base + "/" + relative

    def _normalize_path(self, path: str) -> str:
        """Normalize path by resolving . and .."""
        parts = path.split("/")
        result = []
        for part in parts:
            if part == "..":
                if result:
                    result.pop()
            elif part and part != ".":
                result.append(part)
        return "/" + "/".join(result)
