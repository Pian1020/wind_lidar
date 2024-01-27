import os
import pandas as pd
from pylab import *

# defines the file directory that contains the HPL files
root = os.getcwd()
file_dir = root + "/ProcessedData"

# creates an empty list to store the DataFrames
df_list = []

# loop that iterates over all the files in the directory
for file in os.listdir(file_dir):
    # checks if the current file ends with the ".hpl"
    if file.endswith(".hpl"):
        # Extracts the date and time information from the filename
        date = file.split("_")[-2] 
        time = file.split("_")[-1].split(".")[0]
        # opens the current file and reads all the lines
        with open(os.path.join(file_dir, file), "r") as f:
            # removes the first line
            lines = f.readlines()
            lines = lines[1:]
            
            # splits each line into three elements
            data = [line.split() for line in lines]
            
            # creates a DataFrame from the three elements
            df = pd.DataFrame(data, columns=["height", "wind_direction", "wind_speed"])
            # adds the datetime to the list
            df["date"]=date
            df["time"]=time
            # adds the DataFrame to the list
            df_list.append(df)

# 將df_list轉換為DataFrame
df_multi = pd.concat(df_list)

# print DataFrame
print(df_multi)

df_multi['height'] = df_multi['height'].astype(int)
df_multi['wind_direction'] = df_multi['wind_direction'].astype(float)
df_multi['wind_speed'] = df_multi['wind_speed'].astype(float)
df_multi['date'] = df_multi['date'].astype(int)
df_multi['time'] = df_multi['time'].astype(int)
