import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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
    df_multi['height'] = df_multi['height']+15
    df_multi['wind_direction'] = df_multi['wind_direction'].astype(float)
    df_multi['wind_speed'] = df_multi['wind_speed'].astype(float)

    #print(df_multi)

    return df_multi

def readtxt(path):
    # Create an empty list to store the DataFrames
    df_list = []

    # Loop that iterates over all the files in the directory
    for file in os.listdir(path):
        # Check if the current file ends with the ".txt" extension
        if file.endswith(".txt"):
            # Extract the date and time information from the filename
            timestamp = file.split("_")[0] + file.split("_")[1]
            format = "%Y%m%d%H%M"
            timestamp = datetime.strptime(timestamp, format)
            
            # Adjust minutes based on whether it's odd or even
            if timestamp.minute % 2 == 0:  # Even minutes
                timestamp = timestamp.replace(second=0)
            else:  # Odd minutes
                timestamp += timedelta(minutes=1)
                timestamp = timestamp.replace(second=0)

            # Open the current file and read all the lines
            with open(os.path.join(path, file), "r") as f:
                # Read the file into a DataFrame
                df = pd.read_csv(f, delim_whitespace=True, skiprows=1)
                
                # Remove commas from all columns
                df.columns = df.columns.str.replace(',', '')
                df = df.applymap(lambda x: x.replace(',', '') if isinstance(x, str) else x)
                
                # Select only the necessary columns
                df = df[['asl', 'ws', 'wd']]
                
                # Rename columns to match the expected names
                df.columns = ['height', 'wind_speed', 'wind_direction']
                
                # Add the datetime to the DataFrame
                df["datetime"] = timestamp
                # Add the DataFrame to the list
                df_list.append(df)
    
    # Convert the list of DataFrames to a single DataFrame
    df_multi = pd.concat(df_list)
    
    # Convert DataFrame columns to appropriate data types
    df_multi['height'] = df_multi['height'].astype(float)
    df_multi['wind_direction'] = df_multi['wind_direction'].astype(float)
    df_multi['wind_speed'] = df_multi['wind_speed'].astype(float)

    return df_multi

def timeAdjust(dataset, start, end):
    selected_data = dataset[(dataset['datetime'] >= start) & (dataset['datetime'] <= end)]
    return selected_data

def heightAdjust(dataset, start, end):
    selected_data = dataset[(dataset['height'] >= start) & (dataset['height'] <= end)]
    return selected_data

def draw(df, df2, start_time, end_time, start_height, end_height):
    fig, ax1 = plt.subplots(figsize=(12, 8))

    # 矢量圖設置
    ax1.set_xlabel("Wind Speed (m/s)")
    ax1.set_ylabel("Height (m, asl)")
    ax1.grid(True, which='both', linestyle='--', linewidth=0.5)

    # 風速折線圖設置
    ax2 = ax1.twiny()
    wind_speed_data = df.groupby('height')['wind_speed'].mean().reset_index()
    wind_speed_data2 = df2.groupby('height')['wind_speed'].mean().reset_index()
    ax1.plot(wind_speed_data['wind_speed'], wind_speed_data['height'], color='blue', marker='', linestyle='-')
    ax2.plot(wind_speed_data2['wind_speed'], wind_speed_data2['height'], color='red', marker='', linestyle='-')
    
    ax1.set_xlim(0,12)
    ax2.set_xlim(0,12)

    
    # 在折線圖上繪製矢量圖的箭頭
    for i in range(len(wind_speed_data)):
        height = wind_speed_data['height'].iloc[i]
        wind_speed = wind_speed_data['wind_speed'].iloc[i]
        datetime_height_data = df[df['height'] == height]
        if not datetime_height_data.empty:
            u = datetime_height_data['wind_speed'].mean() * np.sin(np.radians(datetime_height_data['wind_direction'].mean()))
            v = datetime_height_data['wind_speed'].mean() * np.cos(np.radians(datetime_height_data['wind_direction'].mean()))
            ax1.quiver(wind_speed, height, u, v, color='b', scale=120, width=0.003)
    for i in range(len(wind_speed_data2)):
        height = wind_speed_data2['height'].iloc[i]
        wind_speed = wind_speed_data2['wind_speed'].iloc[i]
        datetime_height_data = df2[df2['height'] == height]
        if not datetime_height_data.empty:
            u = datetime_height_data['wind_speed'].mean() * np.sin(np.radians(datetime_height_data['wind_direction'].mean()))
            v = datetime_height_data['wind_speed'].mean() * np.cos(np.radians(datetime_height_data['wind_direction'].mean()))
            ax2.quiver(wind_speed, height, u, v, color='r', scale=120, width=0.003)

    title = f'Wind Comparison between Yanchao-UAV and Kaoshiung-Wind-LIDAR at 24/02/29 00:00'
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
    dataset2 =readtxt(file_path)
    
    # Costumize dataset
    format = "%Y/%m/%d %H:%M:%S"
    start_time = datetime.strptime(start_time, format)
    end_time = datetime.strptime(end_time, format)
    adjusted_dataset = timeAdjust(dataset, start_time, end_time)
    adjusted_dataset = heightAdjust(adjusted_dataset, start_height, end_height) 
    adjusted_dataset2 = timeAdjust(dataset2, start_time, end_time)
    adjusted_dataset2 = heightAdjust(adjusted_dataset2, start_height, end_height)
    
    draw(adjusted_dataset,adjusted_dataset2, start_time, end_time, start_height, end_height)
