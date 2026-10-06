"""Virtual file system module."""


class VFS:
    """Virtual file system with a name."""

    DEFAULT_NAME = "my_vfs"

    def __init__(self, name: str | None = None) -> None:
        """Initialize VFS with given name or default."""
        self._name = name if name else self.DEFAULT_NAME

    def get_name(self) -> str:
        """Return the name of the VFS."""
        return self._name