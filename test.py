
# read files
import os
import pandas as pd
from pylab import *

# defines the file directory that contains the HPL files
root = os.getcwd()
file_dir = root + "\ProcessedData"

# creates an empty list to store the DataFrames
df_list = []

# loop that iterates over all the files in the directory
for file in os.listdir(file_dir):
    # checks if the current file ends with the ".hpl"
    if file.endswith(".hpl"):
        # Extracts the date and time information from the filename
        date_time_str = file.split("_")[-2] + "_" + file.split("_")[-1].split(".")[0]
        
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
            df["datetime"]=date_time_str
            # adds the DataFrame to the list
            df_list.append(df)

# 將df_list轉換為DataFrame
df_multi = pd.concat(df_list)

# print DataFrame
print(df_multi)

df_multi['height'] = df_multi['height'].astype(int)
df_multi['wind_direction'] = df_multi['wind_direction'].astype(float)
df_multi['wind_speed'] = df_multi['wind_speed'].astype(float)
df_multi['datetime'] = df_multi['datetime'].astype(str)


df_2000=df_multi.loc[df_multi["height"] <= 2000]

height_list=[]
height_list=df_multi['height'].values.tolist()
count = len(os.listdir(file_dir))

# Create the empty list to store wind_speed lists
H = []
WS = []
DT = []

# Iterate through each unique datetime in the DataFrame
a=0
for datetime_value in df_2000['datetime'].unique():
    # Select wind_speed values for the current datetime
    wind_speed_list = df_2000[df_2000['datetime'] == datetime_value]['wind_speed'].tolist()
    # Add the extracted wind_speed list to the WS list
    WS.append(wind_speed_list)
    DT.append(datetime_value)
    if a == 0:
        H = df_2000[df_2000['datetime'] == datetime_value]['height'].tolist()
    a=1

# Rotate WS 90 degrees counterclockwise
WS_rotated = np.array(WS).T  # Transpose and reverse lists


# %%

import matplotlib.pyplot as plt


# 製作jet色彩映射
cmap = plt.cm.jet

# 將起始和結束位置固定為白色和黑色
cmap.set_under('white')
cmap.set_over('black')


plt.figure(figsize=(12, 6))

# 設定橫軸
plt.xlabel("datetime")

# 設定縱軸
plt.ylabel("height")

# 繪製風速資料
for i in range(count):
    plt.pcolormesh(WS_rotated, cmap=cmap)
#plt.gca().set_aspect('equal')  # Ensure equal aspect ratio for clarity

# 設定colorbar
cbar = plt.colorbar(label='Wind Speed')
plt.clim(0, 15)

#plt.yticks(H)

# 顯示圖表
plt.show()


# %%