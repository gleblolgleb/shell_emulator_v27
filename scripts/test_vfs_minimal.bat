@echo off
(
echo ls
echo vfs-save vfs_test/minimal_saved.zip
echo exit
) | python -m src.main -v vfs_test/minimal.zip