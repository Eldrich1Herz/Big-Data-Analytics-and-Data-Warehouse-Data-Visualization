#!/usr/bin/env python3
import sys

cur = None
# cur = текущий user_id (пока None).

users = []
# Список имён пользователей для текущего id.

orders = []
# Список товаров для текущего id.

for line in sys.stdin:
    # Читаем строки из stdin (от маппера).
    
    tag, uid, val = line.strip().split('\t')
    # Разделяем строку по табуляции.
    # tag = 'U' (пользователь) или 'O' (товар).
    # uid = id пользователя.
    # val = имя пользователя или название товара.
    
    if uid != cur:
        # Если встретился новый id (или самый первый)
        
        # Выводим все комбинации для предыдущего id.
        for u in users:
            for o in orders:
                print(f"{u}\t{o}")
        
        # Очищаем списки и запоминаем новый id.
        users = []
        orders = []
        cur = uid
    
    # Добавляем данные в соответствующий список.
    if tag == 'U':
        users.append(val)
    else:  # tag == 'O'
        orders.append(val) 

# После цикла: выводим для последнего id.
for u in users:
    for o in orders:
        print(f"{u}\t{o}")