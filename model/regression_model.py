import json
import os
import joblib

import numpy as np
import pandas as pd

from xgboost import XGBRegressor


def open_model(name: str) -> XGBRegressor:
    """
    Summary
        The open_model function is a Python function that takes a string parameter name and returns an instance of the XGBRegressor class. It is used to load a pre-trained machine learning model from a file.

    Inputs
        name (string): The name of the model file to be loaded.

    Flow
        1. Check if the name parameter is a string. If not, raise a ValueError with the message "Название должно быть
            строкой!".
        2. Check if the model file with the given name exists. If not, raise a FileNotFoundError with the message
            "Файла с названием {name} не существует!".
        3. Open the model file using joblib.load and assign it to the model variable.
        4. Return the loaded model.

    Outputs
        model (XGBRegressor): The loaded machine learning model.
    """
    if not isinstance(name, str):
        raise ValueError('Название должно быть строкой!')

    if not os.path.exists(os.path.join(name + '.pkl')):
        raise FileNotFoundError(f'Файла с названием {name} не существует!')

    try:
        with open(os.path.join(name + '.pkl'), 'r') as f:
            model = joblib.load(os.path.join(name + '.pkl'))
            return model

    except Exception as e:
        raise Exception(f'Ошибка: {e}')


def open_data(name: str) -> dict:
    """
    Summary
        The open_data function is used to read and return the contents of a JSON file. It takes a string parameter name
        which represents the name of the file to be opened.

        The code above calls the open_data function with the file name 'example'. It then prints the contents of the
        file.

    Inputs
        name (string): The name of the file to be opened.

    Flow
        1. Check if the name parameter is a string. If not, raise a ValueError with the message 'Название должно быть
        строкой!' (The name must be a string!).
        2. Check if a file with the name name + '.json' exists. If not, raise a FileNotFoundError with the message
        'Файла с названием {name} не существует!' (File with name {name} does not exist!).
        3. Try to open the file with the name name + '.pkl' in read mode.
        4. Load the contents of the file as JSON using the json.loads function.
        5. Return the loaded data.

    Outputs
        A dictionary containing the contents of the JSON file.
    """
    if not isinstance(name, str):
        raise ValueError('Название должно быть строкой!')

    if not os.path.exists(os.path.join(name + '.json')):
        raise FileNotFoundError(f'Файла с названием {name} не существует!')

    try:
        with open(os.path.join(name + '.json'), 'r') as f:
            data = json.load(f)
            return data

    except Exception as e:
        raise Exception(f'Ошибка: {e}')


def import_data(data: list, name: str) -> np.array:
    """
    Summary
        The import_data function takes a list of data and a name as inputs and returns a numpy array. It first checks
        if the data is in the correct format and has the correct length. Then, it calls the open_data function to
        retrieve additional information. Next, it checks if the categorical and numerical data in the input list are in
        the correct format. Finally, it creates a new list by replacing missing values in the input list with default
        values from the retrieved information, and returns this new list as a numpy array.

    Inputs
        data (list): A list containing 10 elements representing the data for a car. The elements should be in the
        following order: transmission, name, model, year, engine capacity, horse power, fuel, drive unit, mileage,
        location.
        name (str): The name of the file to be opened.

    Flow
        1. Check if the data parameter is a list. If not, raise a ValueError with the message 'Данные должны быть
            переданы в виде списка!' (The data must be passed as a list!).
        2. Check if the length of the data list is 10. If not, raise an ImportError with the message 'Список должен
            содержать 10 элементов!' (The list must contain 10 elements!).
        3. Call the open_data function with the name parameter to retrieve additional information.
        4. Check if the categorical data in the data list are strings. If not, raise a ValueError with the message
            'Категориальные данные должны передаваться в виде строки!' (Categorical data must be passed as a string!).
        5. Check if the numerical data in the data list are strings. If not, raise a ValueError with the message
            'Числовые данные должны передаваться в виде строки!' (Numerical data must be passed as a string!).
        6. Create a new list corr_data by replacing missing values in the data list with default values from the
            retrieved information.
        7. Convert the corr_data list to a numpy array and return it.

    Outputs
        A numpy array containing the data for a car, with missing values replaced by default values.
    """
    if not isinstance(data, list):
        raise ValueError('Данные должны быть переданы в виде списка!')

    if len(data) != 10:
        raise ImportError('Список должен содержать 10 элементов!')

    try:
        info = open_data(name)['data']
    except Exception as e:
        raise Exception(f'Ошибка: {e}')

    name, model, year, engine_capacity, horse_power, fuel, transmission, drive_unit, mileage, location = data

    category = [transmission, name, model, fuel, drive_unit, location]
    numbers = [year, engine_capacity, horse_power, mileage]
    for c in category:
        if not isinstance(c, str):
            raise ValueError('Категориальные данные должны перередаваться в виде строки!')

    for n in numbers:
        if not isinstance(n, str):
            raise ValueError('Числовые данные должны перередаваться в виде в виде строки!')

    corr_data = []
    for k, v in zip(category, info):
        if k in v.keys():
            corr_data.append(v[k])
        else:
            corr_data.append('1')

    transmission, name, model, fuel, drive_unit, location = corr_data
    full = [name, model, year, engine_capacity, horse_power, fuel, transmission, drive_unit, mileage, location]
    return np.array(full)


def prepare_df(data: np.array, name: str) -> pd.DataFrame:
    """
    Summary
    The prepare_df function takes a list of data and a name as inputs and returns a pandas DataFrame. It first calls the
    import_data function to retrieve a numpy array of the data. Then, it creates a transposed DataFrame from the numpy
    array and renames the columns. Next, it converts specific columns to the appropriate data types. Finally, it returns
    the prepared DataFrame.

    Inputs
        data (np.array): A array containing 10 elements representing the data for a car. The elements should be in the
            following order: transmission, name, model, year, engine capacity, horse power, fuel, drive unit, mileage,
            location.
        name (str): The name of the file to be opened.

    Flow
        1. Call the import_data function with the data and name parameters to retrieve a numpy array of the data.
        2. Create a transposed DataFrame te from the numpy array.
        3. Rename the columns of te to match the desired column names.
        4. Define two lists int_64 and float_32 to specify the columns that need to be converted to the appropriate data
            types.
        5. Iterate over the columns in int_64 and float_32 and convert them to np.int64 and np.float32 respectively.
        6. Return the prepared DataFrame te.

    Outputs
        A pandas DataFrame containing the prepared data for a car.

    """
    df = import_data(data=data, name=name)
    te = pd.DataFrame(df).T
    te.rename(columns={
        0: 'name',
        1: 'model',
        2: 'year',
        3: 'engine_capacity',
        4: 'horse_power',
        5: 'fuel',
        6: 'transmission',
        7: 'drive_unit',
        8: 'mileage',
        9: 'location'
    }, inplace=True)
    int_64 = ['name', 'model', 'year', 'fuel', 'transmission', 'drive_unit', 'location']
    float_32 = ['engine_capacity', 'horse_power', 'mileage']
    for i in int_64:
        te[i] = te[i].astype(np.int64)
    for i in float_32:
        te[i] = te[i].astype(np.float32)

    return te


def predict(data: np.array, name: str, model_name: str) -> np.array:
    """
    Summary
        The predict function takes in an array of data, a name, and a model name as inputs. It first prepares the data
        by calling the prepare_df function, which converts the data into a pandas DataFrame with the appropriate column
        names and data types. Then, it loads the pre-trained machine learning model by calling the open_model function.
        Finally, it uses the loaded model to make predictions on the prepared data and returns the predicted values as
        a numpy array.

    Inputs
        data (np.array): An array containing 10 elements representing the data for a car. The elements should be in the
            following order: transmission, name, model, year, engine capacity, horse power, fuel, drive unit, mileage,
            location.
        name (str): The name of the file to be opened.
        model_name (str): The name of the pre-trained machine learning model file to be loaded.

    Flow
        Call the prepare_df function with the data and name parameters to prepare the data as a pandas DataFrame.
        Call the open_model function with the model_name parameter to load the pre-trained machine learning model.
        Use the loaded model to make predictions on the prepared data.
        Return the predicted values as a numpy array.

    Outputs
        np.array: An array containing the predicted values for the given data.
    """
    df = prepare_df(data, name)
    model = open_model(model_name)
    return model.predict(df)
