#!/bin/bash
python -m src.main -v vfs_test/multiple.zip <<EOF
ls
cd /
vfs-save vfs_test/multiple_saved.zip
exit
EOF