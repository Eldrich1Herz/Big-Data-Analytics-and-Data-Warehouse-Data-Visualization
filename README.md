# Big Data Analytics and Data Warehouse: Data Visualization

Проект по анализу больших данных, созданию хранилища данных (Data Warehouse) и визуализации. Реализован с использованием стека технологий Big Data.

## Технологии

| Категория | Технологии |
|-----------|------------|
| **Big Data** | Hadoop, HDFS, PySpark |
| **Stream Processing** | Apache Kafka |
| **Database** | PostgreSQL |
| **NLP** | Word2Vec |
| **Visualization** | Streamlit |
| **Environment** | WSL (Ubuntu), Python |

## Структура проекта

```
├── АБДИХД/                     # Анализ Больших данных и хранилища данных 
│   ├── Apache Kafka-/          # Работа с Apache Kafka (НЕ ЗАВЕРШЕНО)
│   ├── Hadoop+/                # Hadoop и HDFS
│   ├── Pipelines-/             # Data Pipelines (НЕ ЗАВЕРШЕНО)
│   ├── PySpark+/               # PySpark обработка данных
│   └── Word2Vec+/              # NLP и векторизация текста
│
└── ВАНАДАН/                    # Раздел студента Визуализация аналитических данных и анализ данных
    ├── 23.05. Python/          # Визуализация с помощью стандартных python-библиотек
    └── 30.05. Streamlit/       # Визуализация данных через фреймворк
```

## Разделы

### АБДИХД

| Модуль | Описание |
|--------|----------|
| **Apache Kafka** | Настройка и работа с потоками данных в реальном времени |
| **Hadoop** | Распределенная обработка данных, HDFS файловая система |
| **Pipelines** | Построение ETL/ELT пайплайнов |
| **PySpark** | Обработка больших данных с использованием Spark |
| **Word2Vec** | Векторизация текстовых данных, NLP задачи |

### ВАНАДАН

| Модуль | Описание |
|--------|----------|
| **Python** | Разработка на Python для работы с данными |
| **Streamlit** | Создание интерактивных дашбордов и визуализация |

## Установка

### Требования
- Python 3.8+
- WSL (Ubuntu) или Linux окружение
- Hadoop (для модулей Big Data)
- Apache Kafka
- PostgreSQL

### Установка зависимостей

```bash
# Установка основных зависимостей Python
pip install pyspark kafka-python streamlit pandas numpy matplotlib

# Для работы с PostgreSQL
pip install psycopg2 sqlalchemy
```

## Использование

### Запуск PySpark
```bash
pyspark
```

### Запуск Kafka
```bash
# Запуск Zookeeper
bin/zookeeper-server-start.sh config/zookeeper.properties

# Запуск Kafka broker
bin/kafka-server-start.sh config/server.properties
```

### Запуск Streamlit дашборда
```bash
streamlit run app.py
```

## Ссылки

- [Apache Hadoop](https://hadoop.apache.org/)
- [Apache Kafka](https://kafka.apache.org/)
- [PySpark Documentation](https://spark.apache.org/docs/latest/api/python/)
- [Streamlit](https://streamlit.io/)
- [Word2Vec](https://radimrehurek.com/gensim/models/word2vec.html)
