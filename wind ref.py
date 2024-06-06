import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.colors import LinearSegmentedColormap
from pylab import *
from datetime import datetime, timedelta

def createDataset(path):
    # Create an empty list to store the DataFrames
    df_list = []

    # Loop that iterates over all the files in the directory
    for file in os.listdir(path):
        # Check if the current file ends with the ".hpl" extension
        if file.endswith(".hpl"):
            # Extract the date and time information from the filename
            timestamp = file.split("_")[-2] + file.split("_")[-1].split(".")[0]
            format = "%Y%m%d%H%M%S"
            timestamp = datetime.strptime(timestamp, format)
            
            # Adjust minutes based on whether it's odd or even
            if timestamp.minute % 2 == 0:  # Even minutes
                timestamp = timestamp.replace(second=0)
            else:  # Odd minutes
                timestamp += timedelta(minutes=1)
                timestamp = timestamp.replace(second=0)

            # Open the current file and read all the lines
            with open(os.path.join(path, file), "r") as f:
                # Remove the first line
                lines = f.readlines()
                lines = lines[1:]
                
                # Split each line into three elements
                data = [line.split() for line in lines]
                
                # Create a DataFrame from the three elements
                df = pd.DataFrame(data, columns=["height", "wind_direction", "wind_speed"])
                # Add the datetime to the DataFrame
                df["datetime"] = timestamp
                # Add the DataFrame to the list
                df_list.append(df)
    
    # Convert the list of DataFrames to a single DataFrame
    df_multi = pd.concat(df_list)

    # Convert DataFrame columns to appropriate data types
    df_multi['height'] = df_multi['height'].astype(int)
    df_multi['wind_direction'] = df_multi['wind_direction'].astype(float)
    df_multi['wind_speed'] = df_multi['wind_speed'].astype(float)

    #print(df_multi)

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

def draw(df, start_time, end_time, start_height, end_height):
    fig, ax1 = plt.subplots(figsize=(12, 8))

    # 矢量圖設置
    ax1.set_xlabel("Date time")
    ax1.set_ylabel("Height")
    ax1.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax1.xaxis.set_major_locator(mdates.HourLocator(interval=6))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d %H:%M"))

    heights = df['height'].unique()
    datetimes = pd.date_range(start_time, end_time, freq='1T')

    for height in heights:
        datetime_height_data = df[df['height'] == height]
        if not datetime_height_data.empty:
            u = datetime_height_data['wind_speed'] * np.sin(np.radians(datetime_height_data['wind_direction']))
            v = datetime_height_data['wind_speed'] * np.cos(np.radians(datetime_height_data['wind_direction']))
            ax1.quiver(datetime_height_data['datetime'], datetime_height_data['height'], u, v, color='purple', scale=120, width=0.003)

    # 風速折線圖設置
    ax2 = ax1.twiny()
    ax2.set_xlabel("Wind Speed")

    wind_speed_data = df.groupby('height')['wind_speed'].mean().reset_index()
    ax2.plot(wind_speed_data['wind_speed'], wind_speed_data['height'], color='blue', marker='', linestyle='-')

    # 在折線圖上繪製矢量圖的箭頭
    for i in range(len(wind_speed_data)):
        height = wind_speed_data['height'].iloc[i]
        wind_speed = wind_speed_data['wind_speed'].iloc[i]
        datetime_height_data = df[df['height'] == height]
        if not datetime_height_data.empty:
            u = datetime_height_data['wind_speed'].mean() * np.sin(np.radians(datetime_height_data['wind_direction'].mean()))
            v = datetime_height_data['wind_speed'].mean() * np.cos(np.radians(datetime_height_data['wind_direction'].mean()))
            ax2.quiver(wind_speed, height, u, v, color='red', scale=120, width=0.003)

    start_date_str = start_time.strftime('%d')
    end_date_minus_1 = (end_time - timedelta(days=1)).strftime('%d')
    if end_date_minus_1 <= start_date_str:
        title = f'UV-Wind profile of Halo Lidar at Kaohsiung during {start_date_str}'
    else:
        title = f'UV-Wind profile of Halo Lidar at Kaohsiung during Feb {start_date_str}-{end_date_minus_1}, 2024'
    plt.title(title, fontsize=16)

    fig.tight_layout()
    plt.show()



if __name__ == "__main__":

    """ start_time = input()
    end_time = input()
    start_height = int(input())
    end_height = int(input()) """
    start_time = "2024/02/29 00:00:00"
    end_time = "2024/02/29 00:00:00"
    start_height = 50
    end_height = 2000

    # defines the file directory that contains the HPL files
    root = os.getcwd()
    file_path = root + "/testfile"

    # Read file from the disk
    dataset = createDataset(file_path)
    
    # Costumize dataset
    format = "%Y/%m/%d %H:%M:%S"
    start_time = datetime.strptime(start_time, format)
    end_time = datetime.strptime(end_time, format)
    adjusted_dataset = timeAdjust(dataset, start_time, end_time)
    adjusted_dataset = heightAdjust(adjusted_dataset, start_height, end_height) 

    draw(adjusted_dataset, start_time, end_time, start_height, end_height)
