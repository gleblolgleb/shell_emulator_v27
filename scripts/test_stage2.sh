#!/bin/bash
# Stage 2 Test: Configuration & Script Execution
# Note: Run with -v and -s flags to fully test this stage

echo "=== 1. Verify debug output is present ==="
# Debug output appears automatically before script execution

echo "=== 2. Test sequential command execution ==="
ls -l
cd /var/log

echo "=== 3. Test comment skipping ==="
# This line should be skipped by the runner

echo "=== 4. Test error handling in script ==="
# Next line will fail but script must continue
bad_command_here

echo "=== 5. Test empty line skipping ==="


echo "=== 6. Final command ==="
uptime

echo "=== Done ==="
exit