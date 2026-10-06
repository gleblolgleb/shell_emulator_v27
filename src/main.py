"""Entry point for the OS shell emulator."""

from src.repl import run_repl
from src.vfs import VFS


def main() -> None:
    """Main function to run the emulator."""
    vfs = VFS()
    run_repl(vfs)


if __name__ == "__main__":
    main()