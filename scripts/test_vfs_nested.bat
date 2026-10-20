@echo off
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