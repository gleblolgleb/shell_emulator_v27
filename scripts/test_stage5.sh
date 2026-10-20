#!/bin/bash
# Test script for Stage 5 - cp command
# Uses nested.zip which has level1/level2/level3 structure

# 1. Show initial state
ls -la

# 2. Copy a file within the same directory
cp /level1/file.txt /level1/file_copy.txt
ls /level1

# 3. Copy file to another directory
cp /level1/file.txt /level1/level2/
cd /level1/level2
ls
cd /

# 4. Copy entire directory
cp /level1 /level1_backup
ls
cd /level1_backup
ls -la
cd /

# 5. Copy nested directory
cp /level1/level2 /level1/level2_backup
cd /level1
ls
cd /

# 6. ERROR HANDLING:
# Error: source file not found
cp /nonexistent.txt /dest.txt

# Error: wrong number of arguments
cp /level1/file.txt

# Error: source directory not found
cp /nonexistent_dir /dest_dir

# Finish
exit