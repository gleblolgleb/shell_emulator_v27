"""Command handlers for the shell emulator."""
import time
from src.vfs_storage import VFSStorage

UNKNOWN_CMD_MSG = "Unknown command: {}"
START_TIME = time.time()

LS_FLAG_LONG = "l"
LS_FLAG_ALL = "a"
LS_FLAG_HUMAN = "h"

HIDDEN_PREFIX = "."
SIZE_KB = 1024
SIZE_MB = 1024 * 1024
SIZE_GB = 1024 * 1024 * 1024


def _parse_ls_flags(args: list[str]) -> tuple[set[str], str]:
    """Parse ls flags from arguments.

    Returns tuple of (flags set, target path).
    """
    flags: set[str] = set()
    target_path: str = ""
    for arg in args:
        if arg.startswith("-"):
            for char in arg[1:]:
                flags.add(char)
        else:
            target_path = arg
    return flags, target_path


def _format_size(size: int) -> str:
    """Format file size in human-readable form."""
    if size >= SIZE_GB:
        return f"{size / SIZE_GB:.1f}G"
    if size >= SIZE_MB:
        return f"{size / SIZE_MB:.1f}M"
    if size >= SIZE_KB:
        return f"{size / SIZE_KB:.1f}K"
    return f"{size}B"


def _format_time(timestamp: float) -> str:
    """Format timestamp as date string."""
    return time.strftime(
        "%Y-%m-%d %H:%M", time.localtime(timestamp)
    )


def cmd_ls(
    args: list[str], storage: VFSStorage
) -> None:
    """Execute ls command with flags support."""
    flags, target_path = _parse_ls_flags(args)
    if not target_path:
        target_path = storage.get_current_dir()
    try:
        items = storage.list_dir(target_path)
    except FileNotFoundError as exc:
        print(f"Error: {exc}")
        return
    show_hidden = LS_FLAG_ALL in flags
    if not show_hidden:
        items = [
            item for item in items
            if not item.startswith(HIDDEN_PREFIX)
        ]
    if LS_FLAG_LONG in flags:
        for item in items:
            full_path = (
                target_path.rstrip("/")
                + "/" + item
            )
            size = storage.get_file_size(full_path)
            mtime = storage.get_file_time(full_path)
            size_str = (
                _format_size(size)
                if LS_FLAG_HUMAN in flags
                else str(size)
            )
            time_str = _format_time(mtime)
            print(
                f"{size_str:>8} {time_str} {item}"
            )
    else:
        print(" ".join(items))


def cmd_cd(
    args: list[str], storage: VFSStorage
) -> None:
    """Execute cd command to change directory."""
    if not args:
        return
    target = args[0]
    try:
        storage.change_dir(target)
    except FileNotFoundError as exc:
        print(f"Error: {exc}")


def cmd_exit(
    args: list[str], storage: VFSStorage
) -> bool:
    """Handle exit command. Returns True to signal exit."""
    return True


def cmd_uptime(
    args: list[str], storage: VFSStorage
) -> None:
    """Show emulator uptime in seconds."""
    elapsed = time.time() - START_TIME
    print(f"up {elapsed:.0f} seconds")


def cmd_echo(
    args: list[str], storage: VFSStorage
) -> None:
    """Print arguments to stdout."""
    print(" ".join(args))


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


def cmd_cp(
    args: list[str], storage: VFSStorage
) -> None:
    """Copy file or directory within VFS."""
    if len(args) != 2:
        print(
            "Error: cp requires source "
            "and destination"
        )
        return
    source, dest = args
    try:
        storage.copy_item(source, dest)
        print(f"Copied: {source} -> {dest}")
    except FileNotFoundError as exc:
        print(f"Error: {exc}")


def get_unknown_cmd_msg(name: str) -> str:
    """Return error message for unknown command."""
    return UNKNOWN_CMD_MSG.format(name)


COMMANDS = {
    "ls": cmd_ls,
    "cd": cmd_cd,
    "exit": cmd_exit,
    "uptime": cmd_uptime,
    "echo": cmd_echo,
    "vfs-save": cmd_vfs_save,
    "cp": cmd_cp,
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
