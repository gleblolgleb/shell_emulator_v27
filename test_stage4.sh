# Тестирование Этапа 4
echo "=== Тест ls ==="
ls
echo "=== Тест cd ==="
cd folder1
ls
cd ..
ls
echo "=== Тест uptime ==="
uptime
echo "=== Тест echo ==="
echo "Hello from VFS"
echo "Current dir:"
cd /
echo "=== Тест ошибок ==="
cd nonexistent_folder
ls nonexistent_file
unknown_command
exit