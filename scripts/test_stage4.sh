#!/bin/bash
# Stage 4 Test Script: Basic Commands & Flags
# Note: ls/cd are stubs in current version

echo "=== 1. Test ls without flags ==="
ls

echo "=== 2. Test ls -a flag ==="
ls -a

echo "=== 3. Test ls -l flag ==="
ls -l

echo "=== 4. Test ls -lh flag ==="
ls -lh

echo "=== 5. Test combined flags ls -la ==="
ls -la

echo "=== 6. Test cd command ==="
cd /home/user
cd ..
cd /tmp

echo "=== 7. Test uptime command ==="
uptime

echo "=== 8. Test echo command ==="
echo Hello World from Stage 4

echo "=== 9. Test echo with env var ==="
echo User: $USERNAME

echo "=== 10. Test error handling ==="
unknown_command_test

echo "=== Done ==="
exit