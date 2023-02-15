import sqlite3
import csv
import pathlib
path = pathlib.Path('test.py').parent.resolve()
#Verbindung mit der DB
conn = sqlite3.connect("sensor-data.db")
c = conn.cursor()

with open(f'{path}\sensor-data\\2022-02-09_dht22_sensor_3660.csv')as f:
    reader = csv.reader(f, delimiter=';')
    next(reader)  
    for row in reader:
        sensor_type = row[1]
        if sensor_type == 'DHT22':
            #schreibe Daten in Table

            conn.commit()
        elif sensor_type == 'SDS011':
            #schreibe Daten in Table
            
            conn.commit()
        else:
            print('error') 
conn.close()        


