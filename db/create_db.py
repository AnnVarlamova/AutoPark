import sqlite3

# Подключение к базе данных (создаст файл, если его нет)
conn = sqlite3.connect('car_fleet.db')
cursor = conn.cursor()

# Создание таблиц
cursor.execute('''CREATE TABLE IF NOT EXISTS car_info (
    car_id INT PRIMARY KEY,
    model TEXT,
    car_type TEXT,
    fuel_type TEXT,
    car_rating FLOAT,
    riders INT,
    year_to_start INT,
    year_to_work INT,
    main_city TEXT,
    target_reg FLOAT,
    target_class INT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS rides_info (
    ride_id INT PRIMARY KEY,
    user_id INT,
    car_id INT,
    ride_date DATE,
    rating FLOAT,
    ride_duration FLOAT,
    distance FLOAT,
    ride_cost FLOAT,
    speed_avg FLOAT,
    speed_max FLOAT,
    stop_times INT,
    refueling BOOLEAN,
    user_ride_quality FLOAT,
    deviation_normal FLOAT,
    FOREIGN KEY (car_id) REFERENCES car_info(car_id),
    FOREIGN KEY (user_id) REFERENCES driver_info(user_id)
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS driver_info (
    user_id INT PRIMARY KEY,
    age INT,
    sex TEXT,
    user_rating FLOAT,
    user_rides INT,
    user_time_accident INT,
    first_ride_date DATE
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS fix_info (
    worker_id INT,
    car_id INT,
    work_type TEXT,
    work_duration FLOAT,
    destroy_degree FLOAT,
    fix_date DATE,
    PRIMARY KEY (worker_id, car_id),
    FOREIGN KEY (car_id) REFERENCES car_info(car_id)
)''')

conn.commit()
conn.close()
