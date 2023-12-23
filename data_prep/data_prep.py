import os
import pandas as pd
import numpy as np
import json


def open_file(name: str) -> pd.DataFrame:
    return pd.read_csv(os.path.join(name + '.csv'))


def category(data: pd.DataFrame) -> tuple:
    return tuple(data.select_dtypes('object').columns)


def number(data: pd.DataFrame) -> tuple:
    return tuple(data.select_dtypes('number').columns)


def _flat_generator(list_):
    for elem in list_:
        for el in elem:
            yield el


def _indexes(data: list) -> set:
    return {x for x in _flat_generator(data)}


def drop_data(data: pd.DataFrame) -> pd.DataFrame:
    to_drop = [
        list(data[data.fuel == 'автомат'].index),
        list(data[data.fuel == 'механика'].index),
        list(data[data.transmission == '4WD'].index),
        list(data[data.transmission == 'передний'].index)
    ]
    ind = _indexes(to_drop)
    for i in ind:
        data.drop(i, axis=0, inplace=True)

    data.drop(data[data.drive_unit == '108 058 км'].index, axis=0, inplace=True)

    return data


def replace(data: pd.DataFrame) -> pd.DataFrame:
    data.transmission.replace({'механика': 'МКПП',
                               'автомат': 'АКПП',
                               'робот': 'РКП',
                               'вариатор': 'CVT'
                               }, inplace=True)
    return data


def fillna_(data: pd.DataFrame) -> pd.DataFrame:
    return data.fillna(0)


def price(data: pd.DataFrame) -> pd.DataFrame:
    price_ = []
    for d in data.price:
        price_.append(d.replace('\xa0', '').replace('₽', ''))
    data.reset_index(drop=True, inplace=True)
    data.price = pd.Series(price_)

    return data


def name_sep(data: pd.DataFrame) -> pd.DataFrame:
    data.price = data.price.astype('int')

    data.price = data.price / 1_000
    data.mileage = data.mileage / 1_000

    brand = []
    model = []
    for i in range(len(data.name)):
        title = data.name[i].split(" ")
        brand.append(title[0])
        model.append(' '.join(title[1:]))

    data.name = pd.Series(brand)
    data['model'] = pd.Series(model)
    data = data[['name', 'model', 'year', 'engine_capacity', 'horse_power', 'fuel',
                 'transmission', 'drive_unit', 'mileage', 'location', 'price']]

    return data


def select_category_data(data: pd.DataFrame) -> tuple:
    return tuple(data[c] for c in category(data))
