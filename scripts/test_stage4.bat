@echo off
echo === Test ls without flags ===
(
echo ls
echo exit
) | python -m src.main -v vfs_test/multiple.zip

echo === Test ls -a (show hidden) ===
(
echo ls -a
echo exit
) | python -m src.main -v vfs_test/multiple.zip

echo === Test ls -l (long format) ===
(
echo ls -l
echo exit
) | python -m src.main -v vfs_test/multiple.zip

echo === Test ls -lh (long + human) ===
(
echo ls -lh
echo exit
) | python -m src.main -v vfs_test/multiple.zip

echo === Test ls -la (all + long) ===
(
echo ls -la
echo exit
) | python -m src.main -v vfs_test/multiple.zip

echo === Test cd command ===
(
echo ls
echo cd level1
echo ls
echo cd level2
echo ls
echo cd ..
echo ls
echo exit
) | python -m src.main -v vfs_test/nested.zip

echo === Test uptime command ===
(
echo uptime
echo exit
) | python -m src.main -v vfs_test/minimal.zip

echo === Test echo command ===
(
echo echo hello world
echo exit
) | python -m src.main -v vfs_test/minimal.zip