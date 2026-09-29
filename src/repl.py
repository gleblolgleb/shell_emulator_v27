import os
import shlex
VFS_NAME = "vfs"

def expand_environment_variables(command: str) -> str:
    
    return os.path.expandvars(command)


def execute_command(command: str) -> bool:
    
    parts = shlex.split(command)

    if not parts:
        return True

    command_name = parts[0]
    arguments = parts[1:]

    if command_name == "exit":
        return False

    if command_name in ("ls", "cd"):
        print(command_name, *arguments)
        return True

    print(f"Ошибка: неизвестная команда '{command_name}'")
    return True


def run_shell() -> None:
    
    while True:
        command = input(f"{VFS_NAME}$ ")
        command = expand_environment_variables(command)

        if not execute_command(command):
            break


if __name__ == "__main__":
    run_shell()