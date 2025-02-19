import requests
import sqlite3

from config import API

API_CONFIG = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': 'USDEUR',
    'apikey': API,
    'datatype': 'json',
    'outputsize': 'full'
}

API_CONFIG_STR = '&'.join([f'{k}={v}' for k, v in API_CONFIG.items()])


url = f'https://www.alphavantage.co/query?{API_CONFIG_STR}'
r = requests.get(url)
data = r.json()


connection = sqlite3.connect('USD_EUR_data.db')
cursor = connection.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS Rates (
id INTEGER PRIMARY KEY,
date TEXT NOT NULL,
open_value REAL NOT NULL
)
''')

for k, v in data['Time Series (Daily)'].items():
    date_val = k
    open_val = v['1. open']
    cursor.execute(
        'INSERT INTO Rates (date, open_value) VALUES (?, ?)',
        (date_val, open_val)
        )

connection.commit()
connection.close()
