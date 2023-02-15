import sqlite3
import pandas as pd

data = pd.read_csv (r'C:\Users\lachteresch\Desktop\FeinstaubProjekt\sensor-data\2022-02-09_dht22_sensor_3660.csv')   
df = pd.DataFrame(data)

print(df)
