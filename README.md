# Shell Emulator (Variant 27)

## 1. Общее описание
Консольный эмулятор оболочки UNIX-подобной ОС. Поддерживает виртуальную файловую систему (VFS) на базе ZIP-архивов, выполнение стартовых скриптов и набор базовых команд. Все операции изменения VFS производятся только в памяти.

## 2. Описание функций и настроек

### Параметры командной строки
- `--vfs-path <путь>` — путь к ZIP-архиву, используемому как источник VFS.
- `--script <путь>` — путь к стартовому скрипту для автоматического выполнения команд.

### Поддерживаемые команды
- `ls [путь]` — вывод содержимого директории VFS.
- `cd <путь>` — смена текущей директории внутри VFS.
- `uptime` — вывод времени, прошедшего с момента запуска эмулятора.
- `echo <текст>` — вывод текста в консоль.
- `cp <источник> <назначение>` — копирование файла внутри VFS.
- `vfs-save <путь>` — сохранение текущего состояния VFS на диск в формате ZIP.
- `exit` — завершение работы эмулятора.

### Особенности работы
- Парсер поддерживает раскрытие переменных окружения реальной ОС (например, `$HOME`) и корректно обрабатывает аргументы в кавычках.
- При выполнении стартового скрипта команды выполняются последовательно, ошибочные строки пропускаются. На экран выводится как ввод, так и вывод команд.

## 3. Запуск и тестирование

### Генерация тестовых архивов VFS
```
python create_test_vfs.py
```
Интерактивный запуск
```
python src/repl.py --vfs-path test_vfs_complex.zip
```
Запуск со стартовым скриптом
```
python src/repl.py --vfs-path test_vfs_complex.zip --script test_stage5.sh
```
## 4. Примеры использования
Интерактивный режим
```
test_vfs_complex.zip$ ls
folder1/  folder2/  root_file.txt
test_vfs_complex.zip$ cd folder1
test_vfs_complex.zip$ ls
file1.txt  subfolder/
test_vfs_complex.zip$ cp file1.txt ../file1_copy.txt
test_vfs_complex.zip$ vfs-save saved.zip
test_vfs_complex.zip$ exit
```
Выполнение скрипта
```
--- Выполнение скрипта: test_stage5.sh ---
[Input] echo "=== Тест cp ==="
=== Тест cp ===
[Input] ls
folder1/  folder2/  root_file.txt
[Input] echo "--- Копируем root_file.txt в root_copy.txt ---"
--- Копируем root_file.txt в root_copy.txt ---
[Input] cp root_file.txt root_copy.txt
[Input] ls
folder1/  folder2/  root_copy.txt  root_file.txt
[Input] echo "--- Копируем file1.txt из folder1 в корень ---"
--- Копируем file1.txt из folder1 в корень ---
[Input] cp folder1/file1.txt copied_file1.txt
[Input] ls
copied_file1.txt  folder1/  folder2/  root_copy.txt  root_file.txt
[Input] echo "--- Копируем в несуществующий файл (должно создать) ---"
--- Копируем в несуществующий файл (должно создать) ---
[Input] cp root_copy.txt new_file.txt
[Input] ls
copied_file1.txt  folder1/  folder2/  new_file.txt  root_copy.txt  root_file.txt
[Input] echo "--- Тест ошибки: копируем несуществующий файл ---"
--- Тест ошибки: копируем несуществующий файл ---
[Input] cp nonexistent.txt error_copy.txt
cp: 'nonexistent.txt': Нет такого файла
[Input] echo "--- Тест ошибки: cp без аргументов ---"
--- Тест ошибки: cp без аргументов ---
[Input] cp
Ошибка: cp требует два аргумента (источник и назначение).
[Input] exit
--- Скрипт завершен ---
```