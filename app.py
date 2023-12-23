import streamlit as st

from backend import home_part, data_part, model_part


def main():
    st.header('Анализ объявлений о продаже автомобилей с сайта drom.ru ')
    st.text('Идея и реализация: Александр Назимов')
    st.text('Ссылка на репозиторий GitHub: ')

    st.markdown('''Данные были получены из открытых источников, а именно с сайта drom.ru при помощи написанного самолично 
        парсера с использованием библиотек requests и beautifulsoup4. Данные сохранялись в файл с расширением .csv и 
        названием, включающим в себя дату парсинга. Парсились данные легковых автомобилей.''')

    home_part()
    data_part()
    model_part()


if __name__ == '__main__':
    main()
