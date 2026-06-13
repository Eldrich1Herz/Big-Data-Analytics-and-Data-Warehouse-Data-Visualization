#!/bin/bash
INPUT=/user/enovo/wc/input
WC_OUT=/user/enovo/wc_temp
TOP_OUT=/user/enovo/top_pipeline
hdfs dfs -rm -r $WC_OUT $TOP_OUT 2>/dev/null
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -files wc_mapper.py,wc_reducer.py \
  -input $INPUT -output $WC_OUT \
  -mapper "python3 wc_mapper.py" -reducer "python3 wc_reducer.py"
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -files topn_mapper.py,topn_reducer.py \
  -input $WC_OUT -output $TOP_OUT \
  -mapper "python3 topn_mapper.py" -reducer "python3 topn_reducer.py" \
  -numReduceTasks 1
hdfs dfs -cat $TOP_OUT/part-00000
