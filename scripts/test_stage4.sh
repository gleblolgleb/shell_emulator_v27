#!/bin/bash
echo "=== Test ls without flags ==="
python -m src.main -v vfs_test/multiple.zip <<EOF
ls
exit
EOF

echo "=== Test ls -a (show hidden) ==="
python -m src.main -v vfs_test/multiple.zip <<EOF
ls -a
exit
EOF

echo "=== Test ls -l (long format) ==="
python -m src.main -v vfs_test/multiple.zip <<EOF
ls -l
exit
EOF

echo "=== Test ls -lh (long + human) ==="
python -m src.main -v vfs_test/multiple.zip <<EOF
ls -lh
exit
EOF

echo "=== Test ls -la (all + long) ==="
python -m src.main -v vfs_test/multiple.zip <<EOF
ls -la
exit
EOF

echo "=== Test cd command ==="
python -m src.main -v vfs_test/nested.zip <<EOF
ls
cd level1
ls
cd level2
ls
cd ..
ls
exit
EOF

echo "=== Test uptime command ==="
python -m src.main -v vfs_test/minimal.zip <<EOF
uptime
exit
EOF

echo "=== Test echo command ==="
python -m src.main -v vfs_test/minimal.zip <<EOF
echo hello world
echo \$HOME
exit
EOF