#!/usr/bin/env python3
import sys
for line in sys.stdin:
    # Читаем каждую строку входа.
    print(line.strip())
    # Выводим её же, убрав лишние пробелы и переносы строк.