import pandas as pd
import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('car_fleet.db')

# Шаг 1. Загрузка данных из submission.csv и submission_r.csv
submission = pd.read_csv('submission.csv')
submission_r = pd.read_csv('submission_r.csv')

# Шаг 2. Загрузка таблицы car_info из базы
car_info = pd.read_sql('SELECT * FROM car_info', conn)

# Шаг 3. Объединение данных с таблицей car_info
# Добавляем данные из submission
car_info = car_info.merge(submission, on='car_id', how='left')

# Добавляем данные из submission_r
car_info = car_info.merge(submission_r, on='car_id', how='left')

# Шаг 4. Сохранение обновлённой таблицы в базу данных
car_info.to_sql('car_info', conn, if_exists='replace', index=False)
print("Данные успешно добавлены в таблицу car_info")

# Закрытие соединения с базой данных
conn.close()
