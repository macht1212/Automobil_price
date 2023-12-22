import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as ply

from data_prep.data_prep import open_file, drop_data, replace, fillna_, price, name_sep

st.header('Анализ объявлений о продаже автомобилей с сайта drom.ru ')
st.text('Идея и реализация: Александр Назимов')

st.markdown('''Данные были получены из открытых источников, а именно с сайта drom.ru при помощи написанного самолично парсера с использованием библиотек requests и beautifulsoup4. Данные сохранялись в файл с расширением .csv и названием, включающим в себя дату парсинга. Парсились данные легковых автомобилей.''')

st.markdown("""### Описание датасета

Датасет состоит из 10 признаков:  
1. **name** - Марка и модель автомобиля
2. **year** - Год выпуска автомобиля
3. **engine_capacity** - Объем двигателя (л)
4. **horse_power** - Мощность двигателя (л. с.)
5. **fuel** - Тип топлива
6. **transmission** - Каробка передач
7. **drive_unit** - Привод
8. **mileage** - Пробег (км)
9. **location** - Место продажи
10. **price** - Стоимость автомобиля  

В последствии при подготовке данных для модели регрессии признак name был разделен на два: name (Марка автомобиля) и model (Модель автомобиля)
""")

data = open_file('cars_2023-12-19')

data = drop_data(data)
data = replace(data)
data = fillna_(data)
data = price(data)
data = name_sep(data)


st.markdown('### Датасет')
st.dataframe(data)


name_bar = ply.bar(data.name.value_counts().head(15))
st.plotly_chart(name_bar)



