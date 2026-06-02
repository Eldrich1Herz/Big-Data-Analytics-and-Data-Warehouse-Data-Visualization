#!/usr/bin/env python3
import sys
for line in sys.stdin:
    # Читаем строку: ID документа -> текст
    doc_id, text = line.strip().split('\t', 1)
    # split('\t', 1) - разделяем только по первому табу, остальное - текст
    # doc_id = "doc1", text = "hello world"

    for w in text.split():
        # Разбиваем текст на отдельные слова.
        # "hello world" -> ["hello", "world"]

        print(f"{w}\t{doc_id}")
        # Выводим пару: слово -> ID документа
