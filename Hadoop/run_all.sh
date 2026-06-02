#!/bin/bash
# Данные в HDFS загружены.

LOG_FILE="run_all_$(date +%Y%m%d_%H%M%S).log"
echo "Логирование в $LOG_FILE"
exec > >(tee -a "$LOG_FILE") 2>&1

set -e  # Остановка при любой ошибке.

# Создаём alias для hadoop streaming (если не определён).
if ! alias hstream 2>/dev/null; then
    alias hstream="hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar"
fi
shopt -s expand_aliases  # Разрешить использование alias в скрипте.

echo "=== Проверка Hadoop ==="
if ! jps | grep -q "NameNode"; then
    echo "Hadoop не запущен. Запускаем..."
    start-dfs.sh
    start-yarn.sh
    sleep 10
fi

# Задание 1: WordCount.
echo "========== 1. WordCount =========="
hdfs dfs -rm -r /user/enovo/wc/output 2>/dev/null || true
hstream -files wc_mapper.py,wc_reducer.py \
    -input /user/enovo/wc/input -output /user/enovo/wc/output \
    -mapper "python3 wc_mapper.py" -reducer "python3 wc_reducer.py"
echo "Результат:"
hdfs dfs -cat /user/enovo/wc/output/part-00000

# Задание 2: Инвертированный индекс.
echo "========== 2. Инвертированный индекс =========="
hdfs dfs -rm -r /user/enovo/invidx/output 2>/dev/null || true
hstream -files invidx_mapper.py,invidx_reducer.py \
    -input /user/enovo/invidx/input -output /user/enovo/invidx/output \
    -mapper "python3 invidx_mapper.py" -reducer "python3 invidx_reducer.py"
hdfs dfs -cat /user/enovo/invidx/output/part-00000

# Задание 3: Среднее по ключу.
echo "========== 3. Среднее по ключу =========="
hdfs dfs -rm -r /user/enovo/avg/output 2>/dev/null || true
hstream -files avg_mapper.py,avg_reducer.py \
    -input /user/enovo/avg/input -output /user/enovo/avg/output \
    -mapper "python3 avg_mapper.py" -reducer "python3 avg_reducer.py"
hdfs dfs -cat /user/enovo/avg/output/part-00000

# Задание 4: Top-N (3 самых частых слова).
echo "========== 4. Top-N =========="
hdfs dfs -rm -r /user/enovo/topn/output 2>/dev/null || true
hstream -files topn_mapper.py,topn_reducer.py \
    -input /user/enovo/wc/output -output /user/enovo/topn/output \
    -mapper "python3 topn_mapper.py" -reducer "python3 topn_reducer.py" \
    -numReduceTasks 1
hdfs dfs -cat /user/enovo/topn/output/part-00000

# Задание 5: Secondary sort.
echo "========== 5. Secondary sort =========="
hdfs dfs -rm -r /user/enovo/secondary/output 2>/dev/null || true
hstream -files secondary_mapper.py,secondary_reducer.py \
    -input /user/enovo/secondary/input -output /user/enovo/secondary/output \
    -mapper "python3 secondary_mapper.py" -reducer "python3 secondary_reducer.py"
hdfs dfs -cat /user/enovo/secondary/output/part-00000

# Задание 6: Combiner (WordCount с комбайнером).
echo "========== 6. Combiner =========="
hdfs dfs -rm -r /user/enovo/wc_combiner/output 2>/dev/null || true
hstream -files wc_mapper.py,wc_reducer.py,wc_combiner.py \
    -input /user/enovo/wc/input -output /user/enovo/wc_combiner/output \
    -mapper "python3 wc_mapper.py" -combiner "python3 wc_combiner.py" -reducer "python3 wc_reducer.py"
echo "Результат:"
hdfs dfs -cat /user/enovo/wc_combiner/output/part-00000

# Задание 7: Join.
echo "========== 7. Join =========="
hdfs dfs -rm -r /user/enovo/join/output 2>/dev/null || true
hstream -files join_mapper.py,join_reducer.py \
    -input /user/enovo/join/input -output /user/enovo/join/output \
    -mapper "python3 join_mapper.py" -reducer "python3 join_reducer.py"
hdfs dfs -cat /user/enovo/join/output/part-00000

# Задание 9: Pipeline (WordCount -> Top-N).
echo "========== 9. Pipeline =========="
hdfs dfs -rm -r /user/enovo/wc_temp /user/enovo/top_pipeline 2>/dev/null || true
hstream -files wc_mapper.py,wc_reducer.py \
    -input /user/enovo/wc/input -output /user/enovo/wc_temp \
    -mapper "python3 wc_mapper.py" -reducer "python3 wc_reducer.py"
hstream -files topn_mapper.py,topn_reducer.py \
    -input /user/enovo/wc_temp -output /user/enovo/top_pipeline \
    -mapper "python3 topn_mapper.py" -reducer "python3 topn_reducer.py" \
    -numReduceTasks 1
echo "Результат pipeline:"
hdfs dfs -cat /user/enovo/top_pipeline/part-00000

echo "========================================="
echo "Все задания выполнены."
echo "========================================="