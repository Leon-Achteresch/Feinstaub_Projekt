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
            c.execute("INSERT INTO DHT22 (sensor_id, sensor_type, timestamp, loc_id, lon, lat, feuchtigkeit, temp) VALUES (:sid, :stype, :time, :loc, :lon, :lat, :feucht, :temp)",
                      {'sid': row[0], 'stype':row[1], 'time':row[5], 'loc':row[2], 'lat':row[3], 'lon':row[4], 'feucht':row[6], 'temp':row[7]}) 
            conn.commit()
        elif sensor_type == 'SDS011':
            #schreibe Daten in Table
            c.execute("INSERT INTO SDS011 (sensor_id,sensor_type,timestamp,loc_id,lon,lat,P1,P2) VALUES(:a, :b, c, :d, :e, :f, :g, :h)",
                      {'a':row[0], 'b': row[1], 'c': row[5], 'd': row[2], 'e': row[3], 'f': row[4], 'g':row[6], 'h': row[9]})
            conn.commit()
        else:
            print('error') 
conn.close()        


