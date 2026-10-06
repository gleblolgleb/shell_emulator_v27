"""REPL loop for the shell emulator."""

from src.commands import execute
from src.parser import parse_command
from src.vfs import VFS

PROMPT_SUFFIX = "$ "


def run_repl(vfs: VFS) -> None:
    """Run the read-eval-print loop until exit command."""
    prompt = f"{vfs.get_name()}{PROMPT_SUFFIX}"

    while True:
        try:
            line = input(prompt)
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not line.strip():
            continue

        name, args = parse_command(line)

        if not name:
            continue

        should_exit = execute(name, args)

        if should_exit:
            break