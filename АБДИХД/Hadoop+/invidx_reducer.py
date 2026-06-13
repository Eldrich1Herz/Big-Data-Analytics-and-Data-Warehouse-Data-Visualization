#!/usr/bin/env python3
import sys
cur, docs = None, set()
# cur - текущее слово, docs - множество документов, где оно встретилось.

for line in sys.stdin:
    # Читаем строку: слово -> документ.
    w, d = line.strip().split('\t')

    if w == cur:
        # То же слово - добавляем документ в множество.
        docs.add(d)
    else:
        # Новое слово.
        if cur:
            # Выводим результат для предыдущего слова.
            print(f"{cur}\t{','.join(sorted(docs))}")
        # Начинаем собирать для нового слова.
        cur, docs = w, {d}

if cur:
    # Выводим последнее слово.
    print(f"{cur}\t{','.join(sorted(docs))}")