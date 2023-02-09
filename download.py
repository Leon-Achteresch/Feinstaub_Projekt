import urllib.request
import datetime

BASE = "http://archive.luftdaten.info"

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

    for i in range(1, number_of_days + 1): # no data for today
        current_date = datetime.date.today() - i * one_day
        base_url = f'{BASE}/{current_date}/{current_date}'

        for sensor in ['sds011_sensor_3659', 'dht22_sensor_3660']:
            url = f'{base_url}_{sensor}.csv'
            print('download', url)
            try:
                data = str(download(url), encoding='UTF-8')
            except Exception:
                print('Unable to download')
                continue
            
            save(data, f'sensor-data/{current_date}_{sensor}.csv')

if __name__ == '__main__':
    download_days(365)
