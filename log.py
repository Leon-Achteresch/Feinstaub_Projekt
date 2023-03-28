import os
from datetime import datetime

def writelog(message, item):
    if not os.path.isfile("log.txt"):
        with open("log.txt", "w") as file:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"Log file created on {current_time}\n")
            file.write("-------\n")
    
    with open("log.txt", "a") as file:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(current_time + "   |||      " + str(message) + "\n")
        file.write(current_time + "   |||      " + str(item) + "\n")
        file.write("-------\n")
