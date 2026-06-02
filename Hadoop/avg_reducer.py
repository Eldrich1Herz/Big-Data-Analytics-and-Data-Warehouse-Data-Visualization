#!/usr/bin/env python3
import sys

cur, total, cnt = None, 0, 0
# cur   - текущий ключ
# total - сумма значений для текущего ключа
# cnt   - количество значений для текущего ключа

for line in sys.stdin:
    # Читаем строку: ключ, значение, счётчик.
    k, v, one = line.strip().split('\t')
    # v = значение
    # one = "1" (всегда).

    if k == cur:
        # Тот же ключ - суммируем
        total += int(v)
        cnt += 1
    else:
        # Новый ключ.
        if cur:
            # Выводим среднее для предыдущего ключа.
            print(f"{cur}\t{total/cnt}")
        # Начинаем новый подсчёт.
        cur, total, cnt = k, int(v), 1

if cur:
    # Выводим среднее для последнего ключа.
    print(f"{cur}\t{total/cnt}")