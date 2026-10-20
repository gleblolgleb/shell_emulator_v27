"""Virtual file system storage module."""
import base64
import zipfile
from pathlib import Path


class VFSStorage:
    """In-memory virtual file system storage."""

    def __init__(self) -> None:
        """Initialize empty VFS storage."""
        self._files: dict[str, bytes] = {}
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
        result = []
        prefix = path if path.endswith("/") else path + "/"
        if path == "/":
            prefix = "/"
        for file_path in self._files:
            if file_path.startswith(prefix):
                relative = file_path[len(prefix):]
                if "/" not in relative:
                    result.append(relative)
        for dir_path in self._dirs:
            if dir_path == path:
                continue
            if dir_path.startswith(prefix):
                relative = dir_path[len(prefix):]
                name = relative.rstrip("/")
                if "/" not in name:
                    result.append(name)
        return sorted(result)

    def get_file_content(self, path: str) -> bytes:
        """Get file content as bytes."""
        if path not in self._files:
            raise FileNotFoundError(
                f"File not found: {path}"
            )
        return self._files[path]

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
