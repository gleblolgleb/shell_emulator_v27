@echo off
echo === Test cp with nested.zip ===

(
echo ls -la
echo cp /level1/file.txt /level1/file_copy.txt
echo ls /level1
echo cp /level1/file.txt /level1/level2/
echo cd /level1/level2
echo ls
echo cd /
echo cp /level1 /level1_backup
echo ls
echo cd /level1_backup
echo ls -la
echo cd /
echo cp /level1/level2 /level1/level2_backup
echo cd /level1
echo ls
echo cd /
echo cp /nonexistent.txt /dest.txt
echo cp /level1/file.txt
echo cp /nonexistent_dir /dest_dir
echo exit
) | python -m src.main -v vfs_test/nested.zip