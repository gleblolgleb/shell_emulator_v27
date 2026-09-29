# Shell Emulator (Variant 27)

## Description

Console-based emulator of a UNIX-like OS shell. This project is part of the "Configuration Management" course at RTU MIREA.

## Stage 1 Features

- CLI interface with a custom prompt containing the VFS name.
- Parser supports environment variable expansion (e.g., `$HOME`).
- Stub commands: `ls`, `cd`.
- `exit` command to terminate the session.
- Unknown commands are handled with an error message.
- Empty commands are ignored.

## How to Run

1. Ensure that Python is installed.
2. Use the provided script:

```text
run.bat
```
Or run directly from the terminal:
```
python src/repl.py
```

## Author
Chernyshkov Gleb Eduardovich