@echo off
echo === Test minimal VFS ===
(
echo ls
echo vfs-save vfs_test/minimal_saved.zip
echo exit
) | python -m src.main -v vfs_test/minimal.zip

echo === Test multiple files VFS ===
(
echo ls
echo cd /
echo vfs-save vfs_test/multiple_saved.zip
echo exit
) | python -m src.main -v vfs_test/multiple.zip

echo === Test nested VFS ===
(
echo ls
echo cd level1
echo ls
echo cd level2
echo ls
echo cd level3
echo ls
echo cd /
echo vfs-save vfs_test/nested_saved.zip
echo exit
) | python -m src.main -v vfs_test/nested.zip

echo === Test VFS not found ===
(
echo exit
) | python -m src.main -v vfs_test/nonexistent.zip

echo === Test vfs-save without path ===
(
echo vfs-save
echo exit
) | python -m src.main -v vfs_test/minimal.zip