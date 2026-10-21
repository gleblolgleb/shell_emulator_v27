#!/bin/bash
# Stage 3 Test Script: VFS Loading & Saving
# Requires vfs_test/minimal.zip to be generated first

echo "=== 1. Verify VFS is loaded ==="
ls -la

echo "=== 2. Test vfs-save command ==="
vfs-save vfs_test/saved_output.zip

echo "=== 3. Test vfs-save without arguments (error case) ==="
vfs-save

echo "=== 4. Test unknown command handling ==="
invalid_vfs_command

echo "=== 5. Exit emulator ==="
exit