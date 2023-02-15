import sqlite3
import pandas as pd
import csv
import pathlib
path = pathlib.Path('test.py').parent.resolve()

with open(f'{path}\sensor-data\\2022-02-09_dht22_sensor_3660.csv')as f:
    reader = csv.reader(f, delimiter=';')
    next(reader)  
    for row in reader:
        sensor_type = row[1]
        print(sensor_type)
