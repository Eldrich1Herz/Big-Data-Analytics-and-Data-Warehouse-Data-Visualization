#!/usr/bin/env python3
import sys
for line in sys.stdin:
    for w in line.strip().split(): # разбиваем строку на слова
        print(f"{w}\t1") # для каждого слова пару # коэждае слово - одельная единица 
