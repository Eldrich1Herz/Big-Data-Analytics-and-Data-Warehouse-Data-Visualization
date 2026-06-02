#!/usr/bin/env python3
import sys

for line in sys.stdin:
    # Читаем строку: ключ -> значение
    k, v = line.strip().split('\t')
    # k = ключ 
    # v = значение

    print(f"{k}\t{int(v)}\t1")
    # Выводим три колонки:
    # 1. Ключ (k).
    # 2. Значение, преобразованное в число (int(v)).
    # 3. Единица (счётчик количества).