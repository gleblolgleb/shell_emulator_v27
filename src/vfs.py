import os
import zipfile
import hashlib

VFS_DATA = {}
VFS_DIRS = set()
VFS_SOURCE_PATH = None

def load_vfs(zip_path: str) -> bool:
    global VFS_DATA, VFS_DIRS, VFS_SOURCE_PATH
    if not os.path.exists(zip_path):
        print(f"Ошибка: файл VFS '{zip_path}' не найден.")
        return False
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            VFS_DATA = {}
            VFS_DIRS = set()
            for name in zf.namelist():
                if name.endswith('/'):
                    VFS_DIRS.add(name.rstrip('/'))
                else:
                    VFS_DATA[name] = zf.read(name)
            VFS_SOURCE_PATH = zip_path
        return True
    except zipfile.BadZipFile:
        print(f"Ошибка: неверный формат ZIP '{zip_path}'.")
        return False

def save_vfs(output_path: str) -> None:
    try:
        with zipfile.ZipFile(output_path, 'w') as zf:
            for dir_path in VFS_DIRS:
                zf.writestr(dir_path + '/', '')
            for file_path, content in VFS_DATA.items():
                zf.writestr(file_path, content)
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