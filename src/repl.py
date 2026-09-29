import os
import shlex
import argparse


VFS_NAME = "default_vfs"


def expand_environment_variables(command: str) -> str:
    return os.path.expandvars(command)


def execute_command(command: str, is_script: bool = False) -> bool:
    parts = shlex.split(command)

    if not parts:
        return True

    command_name = parts[0]
    arguments = parts[1:]

    if command_name == "exit":
        return False

    if command_name in ("ls", "cd"):
        print(f"{command_name} {' '.join(arguments)}".strip())
        return True

    error_msg = f"Ошибка: неизвестная команда '{command_name}'"
    if is_script:
        print(f"[Script Error] {error_msg}")
    else:
        print(error_msg)
    
    return True


def run_script(script_path: str) -> None:
    if not os.path.exists(script_path):
        print(f"Ошибка: файл скрипта '{script_path}' не найден.")
        return

    print(f"--- Выполнение скрипта: {script_path} ---")
    with open(script_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            expanded_line = expand_environment_variables(line)
            print(f"[Input] {expanded_line}")
            
            if not execute_command(expanded_line, is_script=True):
                break
                
    print("--- Скрипт завершен ---")


def run_shell(vfs_path: str = None, script_path: str = None) -> None:
    global VFS_NAME
    
    if vfs_path:
        VFS_NAME = os.path.basename(vfs_path)
    
    prompt = f"{VFS_NAME}$ "

    if script_path:
        run_script(script_path)
        print("Переход в интерактивный режим после скрипта...")

    while True:
        try:
            command = input(prompt)
            command = expand_environment_variables(command)

            if not execute_command(command):
                break
        except EOFError:
            break
        except KeyboardInterrupt:
            print("\nИспользуйте 'exit' для корректного выхода.")


def main():
    parser = argparse.ArgumentParser(description="Shell Emulator CLI")
    parser.add_argument('--vfs-path', type=str, help='Path to VFS source')
    parser.add_argument('--script', type=str, help='Path to startup script')
    
    args = parser.parse_args()
    run_shell(vfs_path=args.vfs_path, script_path=args.script)


if __name__ == "__main__":
    main()