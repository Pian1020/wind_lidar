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

def draw(dataset, start_time, end_time, start_height, end_height):

    # Create color map
    cmap1 = make_color_map([1, 1, 1], [0.92, 0.92, 0.92], 5)
    cmap2 = make_color_map([0.92, 0.92, 0.92], [0.460, 0.829, 1], 20)
    cmap3 = make_color_map([0.460, 0.829, 1], [0.316, 1, 0.316], 20)
    cmap4 = make_color_map([0.316, 1, 0.316], [1, 1, 0], 20)
    cmap5 = make_color_map([1, 1, 0], [1, 0, 0], 20)
    # colors = [(1, 1, 1), (0.92, 0.92, 0.92), (0.460, 0.829, 1), (0.316, 1, 0.316), (1, 1, 0), (1, 0, 0)]
    # custom_cmap = LinearSegmentedColormap.from_list('custom_cmap', colors)

    # Concatenate the colormaps
    c_map = np.vstack(( cmap1, cmap2, cmap3, cmap4, cmap5 ))
    custom_cmap = LinearSegmentedColormap.from_list('custom_cmap', c_map, N=256)
    custom_cmap.set_over('black')
    custom_cmap.set_under('white')
    
    plt.figure(figsize=(12, 6))

    # Create time stamps show on the graph
    time_diff = (end_time - start_time) / 24
    evenly_spaced_datetimes = []
    evenly_spaced_datetimes.append(start_time)
    for i in range(1, 25):
        evenly_spaced_datetimes.append(start_time + i * time_diff)
    evenly_spaced_datetimes.append(end_time)
    plt.xlabel("LocalTime (hh)", fontsize=12)

    # Create height stamps to show on the graph
    step_size = (end_height - start_height) / 5
    evenly_spaced_numbers = []
    evenly_spaced_numbers.append(start_height)
    for i in range(1, 5):
        evenly_spaced_numbers.append(start_height + i * step_size)
    evenly_spaced_numbers.append(end_height)
    plt.ylabel("Height a.g.l (m)", fontsize=12)

    # Draw wind speed data
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
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H %m/%d'))
    # Function to format x-axis tick labels
    def format_xticks(x):
        if x.hour == 0:
            return x.strftime('%H\n%m/%d')
        else:
            return x.strftime('%H')

    # Set x-axis tick labels
    plt.xticks(evenly_spaced_datetimes, [format_xticks(x) for x in evenly_spaced_datetimes], rotation=0)
    plt.yticks(evenly_spaced_numbers)
    # Set colorbar
    cbar = plt.colorbar(ticks=np.arange(0, 13, 1),label='Wind Speed (m s⁻¹)')
    cbar.ax.tick_params(labelsize=12)
    plt.clim(0, 12)
    
    # Specify step value to select data at intervals of time
    step_hours = 19  # Select every N data
    selected_datetimes = adjusted_dataset['datetime'].unique()[9::step_hours]

    # Specify step value to select data at intervals of height
    step_heights = 8  # Select every N data
    selected_heights = adjusted_dataset['height'].unique()[5::step_heights]

    for datetime_val in selected_datetimes:
        for height_val in selected_heights:
            # Filter data where wind speed is less than or equal to 12
            mask = (adjusted_dataset['wind_speed'] <= 12) & (adjusted_dataset['datetime'] == datetime_val) & (adjusted_dataset['height'] == height_val)
            datetime_height_data = adjusted_dataset[mask]
    
            # If data matching the condition is found, draw the vector field
            if not datetime_height_data.empty:
                # Calculate u and v for the given datetime and height
                u = datetime_height_data['wind_speed'] * np.sin(np.radians(datetime_height_data['wind_direction']))
                v = datetime_height_data['wind_speed'] * np.cos(np.radians(datetime_height_data['wind_direction']))
        
                # Draw the vector field for wind direction and wind speed
                plt.quiver(datetime_height_data['datetime'], datetime_height_data['height'], -u, -v, color='purple', scale=120, width=0.003)

    # Title
    start_date_str = start_time.strftime('%d')
    end_date_minus_1 = (end_time - timedelta(days=1)).strftime('%d')
    if end_date_minus_1 <= start_date_str :
        title = f'UV-Wind profile of Halo Lidar at Kaohsiung during {start_date_str}'
    else:
        title = f'UV-Wind profile of Halo Lidar at Kaohsiung during Feb {start_date_str}-{end_date_minus_1}, 2024'
    plt.title(title, fontsize=16)
    
    # Show the plot
    plt.show()

    # plt.savefig('wind.png')

if __name__ == "__main__":

    """ start_time = input()
    end_time = input()
    start_height = int(input())
    end_height = int(input()) """
    start_time = "2024/02/14 00:00:00"
    end_time = "2024/02/17 00:00:00"
    start_height = 100
    end_height = 2000

    # defines the file directory that contains the HPL files
    root = os.getcwd()
    file_path = root + "/iop1"

    # Read file from the disk
    dataset = createDataset(file_path)
    
    # Costumize dataset
    format = "%Y/%m/%d %H:%M:%S"
    start_time = datetime.strptime(start_time, format)
    end_time = datetime.strptime(end_time, format)
    adjusted_dataset = timeAdjust(dataset, start_time, end_time)
    adjusted_dataset = heightAdjust(adjusted_dataset, start_height, end_height) 

    draw(adjusted_dataset, start_time, end_time, start_height, end_height)
