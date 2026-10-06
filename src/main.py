"""Entry point for the OS shell emulator."""

from src.commands import execute
from src.config import parse_args, print_debug_info
from src.parser import parse_command
from src.repl import run_repl
from src.script_runner import run_script
from src.vfs import VFS


def main() -> None:
    """Main function to run the emulator."""
    args = parse_args()
    print_debug_info(args)

    vfs = VFS()

    if args.script:
        run_script(
            args.script,
            execute,
            parse_command,
        )
    else:
        run_repl(vfs)


if __name__ == "__main__":
    main()