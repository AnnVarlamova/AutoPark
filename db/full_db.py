import pandas as pd
import sqlite3  # Или import psycopg2 для PostgreSQL

# Подключение к базе данных
conn = sqlite3.connect('car_fleet.db')

# Список файлов и таблиц
files_and_tables = {
    'car_test.csv': 'car_info',
    'rides_info.csv': 'rides_info',
    'driver_info.csv': 'driver_info',
    'fix_info.csv': 'fix_info'
}


# Функция для обработки формата "YYYY-MM-DD"
def process_dates_ymd(df, date_columns):
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], format="%Y-%m-%d", errors='coerce')
    return df


# Функция для обработки формата "YYYY-MM-DD HH:MM"
def process_dates_ymd_hm(df, date_columns):
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], format="%Y-%m-%d %H:%M", errors='coerce')
    return df


# Загрузка данных из файлов
for file, table in files_and_tables.items():
    df = pd.read_csv(file)

    # Проверяем, если ли в таблице колонки с датами
    if table == 'rides_info':
        df = process_dates_ymd(df, ['ride_date'])  # Обрабатываем ride_date
    elif table == 'driver_info':
        df = process_dates_ymd(df, ['first_ride_date'])  # Обрабатываем first_ride_date
    elif table == 'fix_info':
        df = process_dates_ymd_hm(df, ['fix_date'])  # Обрабатываем fix_date

    # Сохраняем данные в базу
    df.to_sql(table, conn, if_exists='replace', index=False)
    print(f"Данные из {file} успешно загружены в таблицу {table}")

# Закрываем подключение
conn.close()
