"""Command handlers for the shell emulator."""

UNKNOWN_CMD_MSG = "Unknown command: {}"


def cmd_ls(args: list[str]) -> None:
    """Stub for ls command. Prints name and arguments."""
    print(f"ls: {' '.join(args)}")


def cmd_cd(args: list[str]) -> None:
    """Stub for cd command. Prints name and arguments."""
    print(f"cd: {' '.join(args)}")


def cmd_exit(args: list[str]) -> bool:
    """Handle exit command. Returns True to signal exit."""
    return True


def get_unknown_cmd_msg(name: str) -> str:
    """Return error message for unknown command."""
    return UNKNOWN_CMD_MSG.format(name)


COMMANDS = {
    "ls": cmd_ls,
    "cd": cmd_cd,
    "exit": cmd_exit,
}


def execute(name: str, args: list[str]) -> bool:
    """Execute command by name. Returns True if should exit."""
    if name in COMMANDS:
        result = COMMANDS[name](args)
        return result is True

    print(get_unknown_cmd_msg(name))
    return False