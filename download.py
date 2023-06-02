import urllib.request
import datetime
import glob
import sqlite3
import SQL

BASE = "https://archive.sensor.community"
# conn3 = sqlite3.connect("sensor-data.db")
# c3 = conn3.cursor()

def download(url):
    """
    Download and return data from the given URL.
    >>> data = download('https://de.wikipedia.org')
    >>> type(data)
    <class 'bytes'>
    """
    # Alternatives are described here: 
    # https://www.blog.pythonlibrary.org/2020/06/18/how-to-download-a-file-with-python-video/
    data = urllib.request.urlopen(url).read()
    return data

def save(data, filename):
    'Save data into the given filename.'
    with open(filename, 'wt') as f:
        f.write(data)

def download_days(number_of_days):
    'Download and save data for a given number of days.'
    one_day = datetime.timedelta(days=1)
    import os

    if not os.path.exists('sensor-data'):
        os.makedirs('sensor-data')

    for i in range(1, number_of_days + 1): # no data for today
        current_date = datetime.date.today() - i * one_day
        temp = f'{current_date}'
        now = datetime.date.today()
        nowstr = f'{now}' 
        if temp[0:4] == nowstr[0:4]:
            base_url = f'{BASE}/{current_date}/{current_date}'
        else:
            base_url = f'{BASE}/'+ temp[0:4] + f'/{current_date}/{current_date}'


        for sensor in ['sds011_sensor_3659', 'dht22_sensor_3660']:
            url = f'{base_url}_{sensor}.csv'
            print('download', url)
            try:
                data = str(download(url), encoding='UTF-8')
            except Exception:
                print('Unable to download')
                continue
            
            save(data, f'sensor-data/{current_date}_{sensor}.csv')

def getdays(c,conn): 
    one_day = datetime.timedelta(days=1)
    current_date = datetime.date.today()
    days = 0

    #Es wird überprüft ob die DB gefüllt ist------------------------------------------------------
    c.execute("SELECT COUNT ( DISTINCT (substr(timestamp, 0, 11))) FROM DHT22", {})  
    conn.commit()
    record = c.fetchone()
    #Wenn die Datenbank leer ist sollen die Daten für das letzte Jahr heruntergeladen werden
    if record[0] == 0:
        return 365
    #---------------------------------------------------------------------------------------------

    #Es wird das Letzte Datum aus dem Table DHT22 selected----------------------------------------
    c.execute("SELECT timestamp FROM DHT22 ORDER BY timestamp DESC LIMIT 1", {}) 
    conn.commit()
    record = c.fetchone()
    #datetimstr ist der ganze timestamp
    datetimestr = record[0]
    #lastdate ist nur das Datum ohne die Uhrzeit
    lastdate = datetime.date(int(datetimestr[0:4]), int(datetimestr[5:7]), int(datetimestr[8:10]))
    #---------------------------------------------------------------------------------------------

    #Es wird berechnet wie viele Tage seit dem letzten Datum in der DB vergangen sind
    while lastdate < current_date - one_day:
        days +=1
        current_date = datetime.date.today() - days * one_day
    #---------------------------------------------------------------------------------------------

    #file = len(glob.glob(f'sensor-data\\{current_date}*.csv'))
    #while len(glob.glob(f'sensor-data\\{current_date}*.csv')) <1 and days <= 365:
        #days +=1
        #current_date = datetime.date.today() - days * one_day
    
    #Es wird der letzte Tag gelöscht damit kein halber Tag in der DB steht------------------------
    # date = f"{lastdate}"
    # c.execute("DELETE FROM DHT22 WHERE timestamp LIKE :date", {'date':date + '%'}) 
    # conn.commit()
    # c.execute("DELETE FROM SDS011 WHERE timestamp > :date", {'date':date + '%'}) 
    # conn.commit()
    #---------------------------------------------------------------------------------------------

    return days

#Es wird überpeüft, ob der ausgewähle Tag i GUI in der Datenbank ist, wenn nicht wird er heruntergeladen
def checkdate(date,c,conn):
    c.execute("SELECT COUNT(timestamp) FROM DHT22 WHERE TIMESTAMP LIKE :KEY", {'KEY': date + '%'})  
    conn.commit()
    record = c.fetchone()
    now = datetime.date.today()
    nowstr = f'{now}' 
    if date == nowstr[0:4]:
        base_url = f'{BASE}/{date}/{date}'
    else:
        base_url = f'{BASE}/'+ date[0:4] + f'/{date}/{date}'
    if record[0] == 0:
        url = f'{base_url}_sds011_sensor_3659.csv'
        data = str(download(url), encoding='UTF-8')
        save(data, f'sensor-data/{date}_sds011_sensor_3659.csv')
        url = f'{base_url}_dht22_sensor_3660.csv'
        data = str(download(url), encoding='UTF-8')
        save(data, f'sensor-data/{date}_dht22_sensor_3660.csv')
        SQL.importtoDB(c, conn, data)
#-------------------------------------------------------------------------------

# if __name__ == '__main__':
#    download_days(365)
#     c3.execute("DELETE FROM DHT22 WHERE ref >= 0", {}) 
#     conn3.commit()
#     c3.execute("DELETE FROM SDS011 WHERE ref >=0", {}) 
#     conn3.commit()
import subprocess
import sys

def install_packages(requirements_file):
    with open(requirements_file) as f:
        requirements = f.read().splitlines()
    for package in requirements:
        try:
            __import__(package)
            print(f"{package} ist schon installiert.")
        except ImportError:
            print(f"Installiere {package}...")
            cmd = [sys.executable, "-m", "pip", "install", package]
            try:
                subprocess.check_call(cmd)
            except subprocess.CalledProcessError as e:
                print(f"Fehler beim installieren von {package}: {str(e)}")



