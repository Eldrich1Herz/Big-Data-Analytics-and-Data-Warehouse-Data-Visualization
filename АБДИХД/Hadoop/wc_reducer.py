#!/usr/bin/env python3

import sys

cur, total = None, 0
# cur - текущее слово, total - накопленная сумма для него.

for line in sys.stdin:
    # Читаем строки из stdin (приходят от маппера после сортировки).
    w, c = line.strip().split('\t')
    # Разделяем строку на слово и число (частота = 1).
    
    if w == cur:
        # Если слово совпадает с предыдущим - суммируем.
        total += int(c)
    else:
        # Если встретили новое слово.
        if cur:
            # Выводим результат для предыдущего слова.
            print(f"{cur}\t{total}")
        # Начинаем новый подсчёт.
        cur, total = w, int(c)

if cur:
    # Выводим последнее слово.
    print(f"{cur}\t{total}")