import os
import pandas as pd
from pylab import *
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from datetime import datetime, timedelta
import matplotlib.dates as mdates

def createDataset(path):
    # creates an empty list to store the DataFrames
    df_list = []

    # loop that iterates over all the files in the directory
    for file in os.listdir(path):
        # checks if the current file ends with the ".hpl"
        if file.endswith(".hpl"):
            # Extracts the date and time information from the filename
            timestamp = file.split("_")[-2] + file.split("_")[-1].split(".")[0]
            format = "%Y%m%d%H%M%S"
            timestamp = datetime.strptime(timestamp, format)
            # opens the current file and reads all the lines
            with open(os.path.join(path, file), "r") as f:
                # removes the first line
                lines = f.readlines()
                lines = lines[1:]
                
                # splits each line into three elements
                data = [line.split() for line in lines]
                
                # creates a DataFrame from the three elements
                df = pd.DataFrame(data, columns=["height", "wind_direction", "wind_speed"])
                # adds the datetime to the list
                df["datetime"] = timestamp
                # adds the DataFrame to the list
                df_list.append(df)

    # 將df_list轉換為DataFrame
    df_multi = pd.concat(df_list)

    # print DataFrame

    df_multi['height'] = df_multi['height'].astype(int)
    df_multi['wind_direction'] = df_multi['wind_direction'].astype(float)
    df_multi['wind_speed'] = df_multi['wind_speed'].astype(float)

    return df_multi

def make_color_map(start_color, end_color, num_steps):
    r = np.linspace(start_color[0], end_color[0], num_steps)
    g = np.linspace(start_color[1], end_color[1], num_steps)
    b = np.linspace(start_color[2], end_color[2], num_steps)
    return np.column_stack((r, g, b))

def timeAdjust(dataset, start, end):
    selected_data = dataset[(dataset['datetime'] >= start) & (dataset['datetime'] <= end)]
    return selected_data

def heightAdjust(dataset, start, end):
    selected_data = dataset[(dataset['height'] >= start) & (dataset['height'] <= end)]
    return selected_data

def draw(dataset, start_time, end_time, start_height, end_height):

    # Create color map
    cmap1 = make_color_map([1, 1, 1], [0.92, 0.92, 0.92], 5)
    cmap2 = make_color_map([0.92, 0.92, 0.92], [0.460, 0.829, 1], 20)
    cmap3 = make_color_map([0.460, 0.829, 1], [0.316, 1, 0.316], 20)
    cmap4 = make_color_map([0.316, 1, 0.316], [1, 1, 0], 20)
    cmap5 = make_color_map([1, 1, 0], [1, 0, 0], 20)

    # Concatenate the colormaps
    c_map = np.vstack((np.ones((3, 3)), cmap1, cmap2, cmap3, cmap4, cmap5, np.zeros((3, 3))))
    custom_cmap = LinearSegmentedColormap.from_list('custom_cmap', c_map, N=256)

    plt.figure(figsize=(12, 6))

    # Create time stamps show on the graph

    time_diff = (end_time - start_time) / 19
    evenly_spaced_datetimes = []
    evenly_spaced_datetimes.append(start_time)
    for i in range(1, 19):
        evenly_spaced_datetimes.append(start_time + i * time_diff)
    evenly_spaced_datetimes.append(end_time)
    plt.xlabel("datetime")

    # Create height stamps to show on the graph
    step_size = (end_height - start_height) / 9
    evenly_spaced_numbers = []
    evenly_spaced_numbers.append(start_height)
    for i in range(1, 9):
        evenly_spaced_numbers.append(start_height + i * step_size)
    evenly_spaced_numbers.append(end_height)
    plt.ylabel("height")

    # 繪製風速資料
    X = np.unique(dataset['datetime'].values)
    Y = np.unique(dataset['height'].values)
    Z = []
    for date in X:
        Z.append(dataset[(dataset['datetime'] == date)]['wind_speed'])
    Z = np.array(Z)
    # Z = dataset['wind_speed'].values
    xx, yy = np.meshgrid(X, Y)
    plt.pcolormesh(xx, yy, Z.T, cmap=custom_cmap)
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.xticks(evenly_spaced_datetimes, rotation=45)
    plt.yticks(evenly_spaced_numbers)
    # 設定colorbar
    cbar = plt.colorbar(label='Wind Speed')
    plt.clim(0, 15)

    # # 顯示圖表
    plt.show()

    # plt.savefig('wind.png')

if __name__ == "__main__":

    start_time = input()
    end_time = input()
    start_height = int(input())
    end_height = int(input())

    # defines the file directory that contains the HPL files
    root = os.getcwd()
    file_path = root + "/ProcessedData"

    # Read file from the disk
    dataset = createDataset(file_path)
    
    # Costumize dataset
    format = "%Y/%m/%d %H:%M:%S"
    start_time = datetime.strptime(start_time, format)
    end_time = datetime.strptime(end_time, format)
    adjusted_dataset = timeAdjust(dataset, start_time, end_time)
    adjusted_dataset = heightAdjust(adjusted_dataset, start_height, end_height) 

    draw(adjusted_dataset, start_time, end_time, start_height, end_height)
    