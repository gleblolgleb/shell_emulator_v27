"""Command handlers for the shell emulator."""
from src.vfs_storage import VFSStorage

UNKNOWN_CMD_MSG = "Unknown command: {}"


def cmd_ls(
    args: list[str], storage: VFSStorage
) -> None:
    """Stub for ls command. Prints name and arguments."""
    print(f"ls: {' '.join(args)}")


def cmd_cd(
    args: list[str], storage: VFSStorage
) -> None:
    """Stub for cd command. Prints name and arguments."""
    print(f"cd: {' '.join(args)}")


def cmd_exit(
    args: list[str], storage: VFSStorage
) -> bool:
    """Handle exit command. Returns True to signal exit."""
    return True


def cmd_vfs_save(
    args: list[str], storage: VFSStorage
) -> None:
    """Save VFS state to ZIP archive."""
    if not args:
        print(
            "Error: vfs-save requires a path argument"
        )
        return
    path = args[0]
    try:
        storage.save_to_zip(path)
        print(f"VFS saved to: {path}")
    except OSError as exc:
        print(f"Error saving VFS: {exc}")


def get_unknown_cmd_msg(name: str) -> str:
    """Return error message for unknown command."""
    return UNKNOWN_CMD_MSG.format(name)


COMMANDS = {
    "ls": cmd_ls,
    "cd": cmd_cd,
    "exit": cmd_exit,
    "vfs-save": cmd_vfs_save,
}


def execute(
    name: str, args: list[str], storage: VFSStorage
) -> bool:
    """Execute command by name. Returns True if exit."""
    if name in COMMANDS:
        result = COMMANDS[name](args, storage)
        return result is True
    print(get_unknown_cmd_msg(name))
    return False
