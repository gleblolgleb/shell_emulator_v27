"""Command-line argument parser for the shell emulator."""

import argparse


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments and return namespace."""
    parser = argparse.ArgumentParser(
        description="OS Shell Emulator"
    )
    parser.add_argument(
        "-v", "--vfs-path",
        type=str,
        default=None,
        help="Path to VFS location"
    )
    parser.add_argument(
        "-s", "--script",
        type=str,
        default=None,
        help="Path to startup script"
    )
    return parser.parse_args()


def print_debug_info(args: argparse.Namespace) -> None:
    """Print debug information about parsed arguments."""
    vfs_val = args.vfs_path or "(not set)"
    script_val = args.script or "(not set)"

    print("=== Debug: Configuration ===")
    print(f"VFS path: {vfs_val}")
    print(f"Script path: {script_val}")
    print("============================")