"""Entry point for the OS shell emulator."""
from src.commands import execute
from src.config import parse_args, print_debug_info
from src.parser import parse_command
from src.repl import run_repl
from src.script_runner import run_script
from src.vfs import VFS
from src.vfs_storage import VFSStorage


def load_vfs(storage: VFSStorage, path: str) -> None:
    """Load VFS from ZIP archive with error handling."""
    try:
        storage.load_from_zip(path)
        print(f"VFS loaded from: {path}")
    except FileNotFoundError as exc:
        print(f"Error: {exc}")
    except ValueError as exc:
        print(f"Error: {exc}")


def main() -> None:
    """Main function to run the emulator."""
    args = parse_args()
    print_debug_info(args)
    vfs = VFS()
    storage = VFSStorage()
    if args.vfs_path:
        load_vfs(storage, args.vfs_path)
    if args.script:
        run_script(
            args.script,
            execute,
            parse_command,
            storage,
        )
    else:
        run_repl(vfs, storage)


if __name__ == "__main__":
    main()
