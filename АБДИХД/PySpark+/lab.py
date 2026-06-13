from pyspark.sql import SparkSession
from pyspark.sql.functions import *

spark = SparkSession.builder.appName("Lab").getOrCreate()

# Задание 1. Word Count
"""""
explode() - превращает массив в отдельные строки.
split() - разбивает строку на слова по пробелам.
lower() и trim() - приводят слова к единому регистру и убирают лишние пробелы, чтобы одинаковые слова считались вместе.
groupBy() группирует одинаковые слова, count() считает количество, orderBy() сортирует по убыванию.
show() показывает несколько строк на экране, collect() загружает все данные на драйвер.
"""
import os
path = os.path.abspath("file.txt")
df = spark.read.text(f"file://{path}")

words = df.select(explode(split(col("value"), "\\s+")).alias("word"))
# без alias:
# words = words.selectExpr("lower(trim(word)) as word")
words = words.select(lower(trim(col("word"))).alias("word")).filter(col("word") != "")
result = words.groupBy("word").count().orderBy(col("count").desc())

result.show()

# Задание 2. Фильтрация и агрегация
"""
filter() оставляет только строки, удовлетворяющие условию.
avg() вычисляет среднее арифметическое.
collect()[0][0] - загружает результат на драйвер и берёт первое значение (единственное число).
Без фильтра среднее будет считаться по всем возрастам (включая 17) -> результат будет другим.
"""
data = [("Alice", 25), ("Bob", 17), ("Charlie", 30)]
df_people = spark.createDataFrame(data, ["name", "age"])
avg_age = df_people.filter(col("age") >= 18).select(avg("age")).collect()[0][0] 
print(f"Средний возраст (18+): {avg_age}")

# Задание 3. Добавить колонку age_category
""""
withColumn() - добавляет новую колонку или заменяет существующую.
when().otherwise() - работает как IF-ELSE.
withColumn() добавляет колонку к существующему DataFrame, select() выбирает только указанные колонки.
Да, можно вызвать withColumn() несколько раз подряд.
"""

print("=== age_category ===")
df_with_cat = df_people.withColumn("age_category", when(col("age") >= 18, "adult").otherwise("minor"))
df_with_cat.show()

# Задание 6. Shuffle
""""
Shuffle - перераспределение данных между партициями (перемещение по сети).
groupBy(), join(), repartition(), sortByKey(), distinct().
Требует передачи данных по сети, записи на диск, что замедляет работу.
В плане выполнения виден Exchange - это и есть shuffle.
"""

df_shuffle = spark.createDataFrame([(1,"a"),(2,"b"),(1,"c")], ["key","val"])
print("=== Shuffle пример ===")
df_shuffle.groupBy("key").count().explain()
""""
Вывод:
Scan - читаем данные
Project - оставляем колонку key
HashAggregate - считаем локально (частичный результат)
Exchange - перемешиваем данные между узлами
HashAggregate - считаем итоговый результат
Операция groupBy("key").count() вызывает shuffle, потому что в плане есть Exchange.
"""

# Задание 8. Broadcast join
"""
Broadcast join - маленькая таблица копируется на все узлы, shuffle большой таблицы не происходит.
Когда одна таблица маленькая - broadcast(users) в join().
Нет shuffle для большой таблицы -> быстрее, меньше сетевого трафика.
"""

from pyspark.sql.functions import broadcast
users = spark.createDataFrame([(1, "Alice"), (2, "Bob")], ["id", "name"])
logs = spark.createDataFrame([(1, "login"), (2, "click"), (1, "logout")], ["user_id", "action"])
print("=== Broadcast join ===")
logs.join(broadcast(users), logs.user_id == users.id).show()

spark.stop()
