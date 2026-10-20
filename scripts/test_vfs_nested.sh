#!/bin/bash
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