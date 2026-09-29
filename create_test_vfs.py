import zipfile

def create_minimal_vfs():
    with zipfile.ZipFile('test_vfs_minimal.zip', 'w') as zf:
        zf.writestr('readme.txt', 'Minimal VFS content')

def create_complex_vfs():
    with zipfile.ZipFile('test_vfs_complex.zip', 'w') as zf:
        zf.writestr('folder1/', '')
        zf.writestr('folder1/file1.txt', 'Content 1')
        zf.writestr('folder1/subfolder/', '')
        zf.writestr('folder1/subfolder/file2.txt', 'Content 2')
        zf.writestr('folder2/', '')
        zf.writestr('folder2/data.bin', b'\x00\x01\x02\x03')

if __name__ == '__main__':
    create_minimal_vfs()
    create_complex_vfs()
    print("Тестовые VFS архивы созданы.")