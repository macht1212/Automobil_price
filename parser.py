import os
import csv
import re
import datetime
import time

import requests

from bs4 import BeautifulSoup


def get_data():
    """
    The get_data function is responsible for scraping data from a website and saving it to a CSV file. It uses the
    requests library to send HTTP requests and retrieve the HTML content of each page. Then, it uses the BeautifulSoup
    library to parse the HTML and extract specific information such as car names, years, engine capacity, horsepower,
    fuel type, transmission, drive unit, mileage, location, and price. Finally, it writes the extracted data to a CSV
    file.

    Inputs
    There are no inputs for the get_data function. It retrieves data from a website by sending HTTP requests.

    Flow
        1. Generate a filename based on the current date and time.
        2. Open a CSV file with the generated filename for writing.
        3. Write the header row to the CSV file.
        4. Iterate over a range of page numbers from 1 to 2000.
        5. Send an HTTP GET request to the website's URL for each page.
        6. Parse the HTML content of the response using BeautifulSoup.
        7. Extract the car names, years, engine capacity, horsepower, fuel type, transmission, drive unit, mileage,
        location and price from the parsed HTML.
        8. Write the extracted data as a row to the CSV file.
        9. Repeat steps 5-8 for each page.
        10. Close the CSV file.

    Outputs
        The get_data function does not return any values. It saves the extracted data to a CSV file.
    """
    file = f'cars_{datetime.datetime.now().strftime("%Y-%m-%d")}'
    path = f'./{file}'
    with open(os.path.join(path + '.csv'), 'w') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(
            ['name', 'year', 'engin_capacity', 'horse_power', 'fuel', 'transmission', 'drive_unit', 'millage',
             'location', 'price'])
        for i in range(1, 2_000):
            time.sleep(3)

            response = requests.get(url=f'https://auto.drom.ru/all/page{i}/').text
            soup = BeautifulSoup(response, features='lxml')
            name_year = soup.find_all('span', {'data-ftid': 'bull_title'})
            info = soup.find_all('div', class_='css-1fe6w6s e162wx9x0')
            prices = soup.find_all('div', class_="css-1dv8s3l eyvqki91")
            locations = soup.find_all('span', {'data-ftid': 'bull_location'})

            for ny, i, p, l in zip(name_year, info, prices, locations):
                name, year = ny.text.split(', ')
                try:
                    engin_hp, fuel, transmission, drive_unit, millage = i.text.split(', ')
                    millage = re.findall(pattern=r'\d+.\d', string=millage.replace(' ', ''))
                    millage = ''.join(millage)
                    try:
                        engin, hp, *tail = re.findall(pattern=r'(\d+.\d)|(\d+)', string=engin_hp)
                        engin = ''.join(engin)
                        hp = ''.join(hp)
                    except:
                        engin = None
                        hp = re.findall(pattern=r'(\d+)', string=engin_hp)
                        hp = ''.join(hp)
                except:
                    try:
                        engin_hp, fuel, transmission, drive_unit, *tail = i.text.split(', ')
                        try:
                            engin, hp, *tail = re.findall(pattern=r'(\d+.\d)|(\d+)', string=engin_hp)
                            engin = ''.join(engin)
                            hp = ''.join(hp)
                            millage = '0'
                        except:
                            engin = None
                            hp = re.findall(pattern=r'(\d+)', string=engin_hp)
                            hp = ''.join(hp)
                    except:
                        pass
                price = p.text
                location = l.text

                writer.writerow([name, year, engin, hp, fuel, transmission, drive_unit, millage, location, price])
