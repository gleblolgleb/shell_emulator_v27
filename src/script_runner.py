"""Startup script runner for the shell emulator."""

from pathlib import Path
from typing import Callable

COMMENT_PREFIX = "#"


def _is_valid_line(line: str) -> bool:
    """Return True if line is not empty and not a comment."""
    stripped = line.strip()
    return bool(stripped) and not stripped.startswith(
        COMMENT_PREFIX
    )


def run_script(
    script_path: str,
    execute_func: Callable[[str, list[str]], bool],
    parse_func: Callable[[str], tuple[str, list[str]]],
) -> None:
    """Run startup script, skipping erroneous lines."""
    path = Path(script_path)

    if not path.exists():
        print(f"Error: script not found: {script_path}")
        return

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not _is_valid_line(line):
                continue

            print(f"> {line}")

            try:
                name, args = parse_func(line)
                if name:
                    execute_func(name, args)
            except Exception as exc:
                print(f"Error: {exc}")