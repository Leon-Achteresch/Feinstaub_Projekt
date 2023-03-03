import sqlite3
from datetime import datetime


#Verbindung mit der DB


#WERTE wird aus der Datenbank als ARRAY zurückgegeben(Für die Y Koord)
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


