import sqlite3
import csv
import os
import pathlib

path = pathlib.Path('test.py').parent.resolve()

def listCSV():
    path = pathlib.Path('test.py').parent.resolve()
    dir_path = f'{path}\sensor-data\\'
    res = []
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            res.append(path)
    return res

def importtoDB(c,conn,label):
    list = listCSV()
    for i in list: 
        with open(f'{path}\sensor-data\\' + i)as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)
            print(i)  
            for row in reader:
                sensor_type = row[1]
                if sensor_type == 'DHT22':
                    #schreibe Daten in Table
                    c.execute("INSERT INTO DHT22 (sensor_id, sensor_type, timestamp, loc_id, lon, lat, feuchtigkeit, temp) VALUES (:sid, :stype, :time, :loc, :lon, :lat, :feucht, :temp)",
                            {'sid': row[0], 'stype':row[1], 'time':row[5], 'loc':row[2], 'lat':row[3], 'lon':row[4], 'feucht':row[6], 'temp':row[7]}) 
                    conn.commit()
                elif sensor_type == 'SDS011':
                    #schreibe Daten in Table
                    c.execute("INSERT INTO SDS011 (sensor_id,sensor_type,timestamp,loc_id,lon,lat,P1,P2) VALUES(:a, :b, :c, :d, :e, :f, :g, :h)",
                            {'a':row[0], 'b': row[1], 'c': row[5], 'd': row[2], 'e': row[3], 'f': row[4], 'g':row[6], 'h': row[9]})
                    conn.commit()
                else:
                    print('error') 
            try:
                f.close()
                os.remove('sensor-data\\' + i)
                label.setText(f"Daten für {i[:10]} aktualisiert") 
            except Exception as e: 
                print(e)
                
def SELECT(DATUM,WERT,Liste):
    conn = sqlite3.connect("sensor-data.db")
    c = conn.cursor()
    if WERT == "feuchtigkeit" or WERT == "temp":
        c.execute("SELECT timestamp, {} FROM DHT22 WHERE timestamp LIKE ?".format(WERT), (DATUM + '%',))
    elif WERT == "P1" or WERT == "P2":
        c.execute("SELECT substr(timestamp,12,10), {} FROM SDS011 WHERE timestamp LIKE ?".format(WERT), (DATUM + '%',))
    else:
        print("Ungültiger WERT")

    rows = c.fetchall()
    timestamp_liste = [row[0] for row in rows]
    wert_liste = [row[1] for row in rows]

    conn.close()
    if Liste == 'DATUM':
        return timestamp_liste
    elif Liste == 'WERT':
        return wert_liste
    else:
        print('ERROR: Keine Liste ausgewählt')    