# Тестирование Этапа 5 - команда cp
echo "=== Тест cp ==="
ls
echo "--- Копируем root_file.txt в root_copy.txt ---"
cp root_file.txt root_copy.txt
ls
echo "--- Копируем file1.txt из folder1 в корень ---"
cp folder1/file1.txt copied_file1.txt
ls
echo "--- Копируем в несуществующий файл (должно создать) ---"
cp root_copy.txt new_file.txt
ls
echo "--- Тест ошибки: копируем несуществующий файл ---"
cp nonexistent.txt error_copy.txt
echo "--- Тест ошибки: cp без аргументов ---"
cp
exit