from pymongo import MongoClient
import csv
import requests


def add_data():
    client = MongoClient('mongodb://172.18.0.1:30000')

    db = client['test']

    collection = db['clima']

    with open('worldcities-2.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            lat = float(row['lat'])
            long = float(row['lng'])

            url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&forecast_days=7&daily=temperature_2m_max,temperature_2m_min&timezone=PST'

            response = requests.get(url)
            data = response.json()

            forecast = data['daily']

            date = forecast['time'][1] # Data for tomorrow
            temp_max = forecast['temperature_2m_max'][1] # Data for tomorrow]
            temp_min = forecast['temperature_2m_max'][1] # Data for tomorrow

            temp = (float(temp_max) + float(temp_min)) / 2

            city = row['city']


            document = {
                'date': date,
                'city': city,
                'latitude': lat,
                'longitude': long,
                'temp_max': temp_max,
                'temp_min': temp_min,
                'temp': temp
            }

            collection.insert_one(document)
    client.close()

add_data()