import streamlit as st
import sqlite3
import pandas as pd

# Подключение к базе данных
DB_PATH = 'db/car_fleet.db'

@st.cache_data
def load_data(query):
    """Загружает данные из базы данных."""
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(query, conn)

# Загружаем данные
car_info = load_data("SELECT * FROM car_info")
rides_info = load_data("SELECT * FROM rides_info")
driver_info = load_data("SELECT * FROM driver_info")
fix_info = load_data("SELECT * FROM fix_info")

# Настройка интерфейса
st.title("🚗 Дашборд Таксопарка")

# Выбор секции
section = st.sidebar.selectbox(
    "Выберите секцию для анализа",
    ["Общая информация", "Анализ машин", "Анализ водителей"]
)

# Общая информация
if section == "Общая информация":
    st.header("Общая информация")
    st.write("**Всего автомобилей:**", len(car_info))
    st.write("**Всего водителей:**", len(driver_info))
    st.write("**Всего поездок:**", len(rides_info))
    st.write("**Всего ремонтов:**", len(fix_info))

    # График: частота ремонтов по маркам автомобилей
    st.subheader("Частота ремонтов по маркам")
    model_fix_counts = fix_info.merge(car_info, on='car_id')['model'].value_counts()
    st.bar_chart(model_fix_counts)

# Анализ машин
elif section == "Анализ машин":
    st.header("Анализ автомобилей")

    # График: распределение числа поездок по моделям
    st.subheader("Распределение числа поездок по моделям")
    model_riders = car_info.groupby('model')['riders'].sum().sort_values(ascending=False)
    st.bar_chart(model_riders)

    selected_model = st.selectbox("Выберите марку автомобиля", car_info['model'].unique())
    filtered_cars = car_info[car_info['model'] == selected_model]
    st.write(f"Найдено машин марки **{selected_model}**: {len(filtered_cars)}")

    # График: распределение рейтингов машин выбранной марки
    st.subheader("Распределение рейтинга машин")
    st.bar_chart(filtered_cars['car_rating'].value_counts())

    # Просмотр наиболее критических машин
    st.subheader("Ранжирование машин по дням до ремонта")
    sort_order = st.radio("Выберите порядок сортировки", ["Возрастание", "Убывание"])
    sorted_cars = car_info.sort_values(by='target_reg', ascending=(sort_order == "Возрастание"))
    st.dataframe(sorted_cars)

    # Выбор конкретного автомобиля по ID
    car_id = st.selectbox("Выберите ID автомобиля", car_info['car_id'].unique())
    selected_car = car_info[car_info['car_id'] == car_id]
    st.write(f"**Информация о выбранной машине (ID: {car_id})**")
    st.table(selected_car)

# Анализ водителей
elif section == "Анализ водителей":
    st.header("Анализ водителей")
    st.write("Пол: **0 = Мужчина**, **1 = Женщина**")

    # Ранжирование водителей по числу инцидентов
    st.subheader("Ранжирование водителей по числу инцидентов")
    sort_order = st.radio("Выберите порядок сортировки", ["Возрастание", "Убывание"])
    sorted_drivers = driver_info.sort_values(by='user_time_accident', ascending=(sort_order == "Возрастание"))
    st.dataframe(sorted_drivers)

    # График: распределение рейтинга по полу
    st.subheader("Распределение рейтинга по полу")
    gender_ratings = driver_info.groupby('sex')['user_rating'].mean()
    st.bar_chart(gender_ratings)

    # График: распределение рейтинга по возрасту
    st.subheader("Распределение рейтинга по возрасту")
    age_ratings = driver_info.groupby('age')['user_rating'].mean()
    st.line_chart(age_ratings)

    # График: распределение рейтинга по стажу
    if 'first_ride_date' in driver_info.columns:
        driver_info['experience_years'] = pd.to_datetime('2025-01-01') - pd.to_datetime(driver_info['first_ride_date'])
        driver_info['experience_years'] = driver_info['experience_years'].dt.days // 365
        st.subheader("Распределение рейтинга по стажу")
        exp_ratings = driver_info.groupby('experience_years')['user_rating'].mean()
        st.line_chart(exp_ratings)

    # Выбор конкретного водителя по ID
    user_id = st.selectbox("Выберите ID водителя", driver_info['user_id'].unique())
    selected_driver = driver_info[driver_info['user_id'] == user_id]
    st.write(f"**Информация о выбранном водителе (ID: {user_id})**")
    st.table(selected_driver)


# Завершение
st.sidebar.info("Дашборд разработан для оптимизации анализа автопарка 🚖")
