#!/bin/bash
python -m src.main -v vfs_test/minimal.zip <<EOF
ls
vfs-save vfs_test/minimal_saved.zip
exit
EOF