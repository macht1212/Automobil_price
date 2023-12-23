import datetime

import pandas as pd
import streamlit as st

from data_prep.data_prep import select_category_data, open_file, drop_data, replace, fillna_, price, name_sep
from model.regression_model import predict, open_data


def model_part():
    st.header('')
    st.header("""Модель регрессии""")

    st.markdown("""### Подготовка датасета""")
    st.markdown("""1. Обработка выбросов
2. Перевод категориальных значений в числовые (Count Encoder или Label Encoder)
3. Разделение данных на тренировочную и тестовую выборки (sklearn: train_test_split). Размер тестовой выборки составил 20%.  
4. Выбор модели регрессии (RandomForestRegressor из библиотеки sklearn или XGBRegressor из библиотеки xgboost)
5. Обучение и тестирование модели  
6. Сохранение предобученной модели""")

    st.markdown("""Наилучший результат показала модель регрессии XGBRegressor с модифицировнными категориальными признаками через Count Encoder:  
* Accuracy тренировочной выборки: 0.99078
* Accuracy тестовой выборки: 0.94262""")
    st.markdown("""# Использование модели""")

    data = open_file('cars_2023-12-19')

    data = drop_data(data)
    data = replace(data)
    data = fillna_(data)
    data = price(data)
    data = name_sep(data)

    name, model, fuel, transmission, drive_unit, location = select_category_data(data)

    name_to_model = st.selectbox('Марка', name.unique())

    selector = open_data('selector')

    selector['Прочие'].append('Другой')

    model_to_model = st.selectbox('Модель', selector[name_to_model])

    year_to_model = st.text_input('Год выпуска', key=1, placeholder='0',
                                  help='Введите год выпуска автомобиля (целое число)')

    engine_capacity_to_model = st.text_input('Объем двигателя', key=2, placeholder='0.0',
                                             help='Введите объем двигателя в литрах (число с плавающей точкой)')

    horse_power_to_model = st.text_input('Мощность двигателя', key=3, placeholder='0',
                                         help='Введите мощность двигателя в лошадинных силах (целое число)')

    mileage_to_model = st.text_input('Пробег', key=4, placeholder='0.0',
                                     help='Введите пробег автомобиля в тыс. км. (число с плавающей точкой)')

    fuel_to_model_to_model = st.selectbox('Тип топлива', fuel.unique())

    transmission_to_model = st.selectbox('Коробка передач', transmission.unique())

    drive_unit_to_model = st.selectbox('Привод', drive_unit.unique())

    location_to_model = st.selectbox('Город', location.unique())

    data_to_model = [
        name_to_model,
        model_to_model,
        year_to_model,
        engine_capacity_to_model,
        horse_power_to_model,
        fuel_to_model_to_model,
        transmission_to_model,
        drive_unit_to_model,
        mileage_to_model,
        location_to_model
    ]

    if st.button('Рассчитать:'):
        try:
            counted_price = int(round(predict(data_to_model, "data", "car_model")[0] * 1000, 0))
            st.header(f'Ориентировочная стоимость составит: {counted_price:,d} руб.')
        except:
            st.header('Вы не ввели корректные данные, при затруднении смотрите подсказки.')
