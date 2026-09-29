import os
import zipfile
import hashlib

VFS_DATA = {}
VFS_DIRS = set()
VFS_SOURCE_PATH = None
CURRENT_DIR = "/"


def load_vfs(zip_path: str) -> bool:
    global VFS_DATA, VFS_DIRS, VFS_SOURCE_PATH, CURRENT_DIR
    if not os.path.exists(zip_path):
        print(f"Ошибка: файл VFS '{zip_path}' не найден.")
        return False
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            VFS_DATA = {}
            VFS_DIRS = set()
            for name in zf.namelist():
                if name.endswith('/'):
                    dir_name = '/' + name.rstrip('/')
                    VFS_DIRS.add(dir_name)
                else:
                    file_name = '/' + name
                    VFS_DATA[file_name] = zf.read(name)
            VFS_DIRS.add('/')
            VFS_SOURCE_PATH = zip_path
            CURRENT_DIR = "/"
        return True
    except zipfile.BadZipFile:
        print(f"Ошибка: неверный формат ZIP '{zip_path}'.")
        return False


def save_vfs(output_path: str) -> None:
    try:
        with zipfile.ZipFile(output_path, 'w') as zf:
            for dir_path in VFS_DIRS:
                if dir_path != '/':
                    zf.writestr(dir_path.lstrip('/') + '/', '')
            for file_path, content in VFS_DATA.items():
                zf.writestr(file_path.lstrip('/'), content)
    except Exception as e:
        print(f"Ошибка при сохранении VFS: {e}")


def get_vfs_info() -> str:
    if not VFS_SOURCE_PATH:
        return "VFS не загружена."
    try:
        with open(VFS_SOURCE_PATH, 'rb') as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        name = os.path.basename(VFS_SOURCE_PATH)
        return f"Имя: {name}, SHA-256: {file_hash}"
    except Exception:
        return "Не удалось получить информацию."


def list_dir(path: str = None) -> str:
    if path is None:
        target_dir = CURRENT_DIR
    else:
        target_dir = _resolve_path(path)

    if target_dir not in VFS_DIRS:
        return f"ls: '{path}': Нет такого файла или каталога"

    items = []
    prefix = target_dir if target_dir == '/' else target_dir + '/'

    for dir_path in VFS_DIRS:
        if dir_path.startswith(prefix) and dir_path != target_dir:
            remainder = dir_path[len(prefix):]
            if '/' not in remainder:
                items.append(remainder + '/')

    for file_path in VFS_DATA:
        if file_path.startswith(prefix):
            remainder = file_path[len(prefix):]
            if '/' not in remainder:
                items.append(remainder)

    if not items:
        return ""
    return "  ".join(sorted(items))


def change_dir(path: str) -> str:
    global CURRENT_DIR

    if not path or path == "~":
        CURRENT_DIR = "/"
        return ""

    new_dir = _resolve_path(path)

    if new_dir not in VFS_DIRS:
        return f"cd: '{path}': Нет такого файла или каталога"

    CURRENT_DIR = new_dir
    return ""


def _resolve_path(path: str) -> str:
    if path.startswith("/"):
        return path.rstrip("/") or "/"

    if path == ".":
        return CURRENT_DIR

    if path == "..":
        if CURRENT_DIR == "/":
            return "/"
        parts = CURRENT_DIR.strip("/").split("/")
        if len(parts) == 1:
            return "/"
        return "/" + "/".join(parts[:-1])

    if CURRENT_DIR == "/":
        return "/" + path
    return CURRENT_DIR + "/" + path