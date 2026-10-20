@echo off
(
echo ls
echo cd /
echo vfs-save vfs_test/multiple_saved.zip
echo exit
) | python -m src.main -v vfs_test/multiple.zip