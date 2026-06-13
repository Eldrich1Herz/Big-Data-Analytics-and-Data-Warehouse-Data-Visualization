#!/bin/bash
echo "Загрузка данных в HDFS"

# Создание директорий.
hdfs dfs -mkdir -p /user/enovo/wc/input
hdfs dfs -mkdir -p /user/enovo/invidx/input
hdfs dfs -mkdir -p /user/enovo/avg/input
hdfs dfs -mkdir -p /user/enovo/secondary/input
hdfs dfs -mkdir -p /user/enovo/join/input

# Копирование файлов.
hdfs dfs -put -f data/input.txt /user/enovo/wc/input/
hdfs dfs -put -f data/docs.txt /user/enovo/invidx/input/
hdfs dfs -put -f data/avg.txt /user/enovo/avg/input/
hdfs dfs -put -f data/secondary.txt /user/enovo/secondary/input/
hdfs dfs -put -f data/users_tagged.txt /user/enovo/join/input/
hdfs dfs -put -f data/orders_tagged.txt /user/enovo/join/input/

echo "Данные загружены"