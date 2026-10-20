#!/bin/bash
echo "=== Test minimal VFS ==="
python -m src.main -v vfs_test/minimal.zip <<EOF
ls
vfs-save vfs_test/minimal_saved.zip
exit
EOF

echo "=== Test multiple files VFS ==="
python -m src.main -v vfs_test/multiple.zip <<EOF
ls
cd /
vfs-save vfs_test/multiple_saved.zip
exit
EOF

echo "=== Test nested VFS ==="
python -m src.main -v vfs_test/nested.zip <<EOF
ls
cd level1
ls
cd level2
ls
cd level3
ls
cd /
vfs-save vfs_test/nested_saved.zip
exit
EOF

echo "=== Test VFS not found ==="
python -m src.main -v vfs_test/nonexistent.zip <<EOF
exit
EOF

echo "=== Test vfs-save without path ==="
python -m src.main -v vfs_test/minimal.zip <<EOF
vfs-save
exit
EOF