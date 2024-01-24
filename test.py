import os
import pandas as pd
from pylab import *
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

def createDataset(path):
    # creates an dictionary to hold data <string, list>
    dataset = []
    time_stamps = []

    # loop that iterates over all the files in the directory
    for file in os.listdir(path):
        # checks if the current file ends with the ".hpl"
        if file.endswith(".hpl"):
            # Extracts the date and time information from the filename
            date_time_str = file.split("_")[-2] + "_" + file.split("_")[-1].split(".")[0]
            time_stamps.append(date_time_str)
            # opens the current file and reads all the lines
            with open(os.path.join(path, file), "r") as f:
                # removes the first line
                lines = f.readlines()
                lines = lines[1:]
                
                # splits each line into three elements
                data = np.array([line.split() for line in lines])
                dataset.append(data)
    return np.array(dataset), time_stamps

def dataSetToFloat(dataset):
    for iter in range(len(dataset)):
        for it in range(len(dataset[iter])):
            for i in range(len(dataset[iter][it])):
                dataset[iter][it][i] = float(dataset[iter][it][i])
    return dataset

def make_color_map(start_color, end_color, num_steps):
    r = np.linspace(start_color[0], end_color[0], num_steps)
    g = np.linspace(start_color[1], end_color[1], num_steps)
    b = np.linspace(start_color[2], end_color[2], num_steps)
    return np.column_stack((r, g, b))

def draw(dataset, count, time_stamps):
    cmap1 = make_color_map([1, 1, 1], [0.92, 0.92, 0.92], 5)
    cmap2 = make_color_map([0.92, 0.92, 0.92], [0.460, 0.829, 1], 20)
    cmap3 = make_color_map([0.460, 0.829, 1], [0.316, 1, 0.316], 20)
    cmap4 = make_color_map([0.316, 1, 0.316], [1, 1, 0], 20)
    cmap5 = make_color_map([1, 1, 0], [1, 0, 0], 20)

    # Concatenate the colormaps
    c_map = np.vstack((np.ones((3, 3)), cmap1, cmap2, cmap3, cmap4, cmap5, np.zeros((3, 3))))
    custom_cmap = LinearSegmentedColormap.from_list('custom_cmap', c_map, N=256)
    # 將起始和結束位置固定為白色和黑色
    # c_map.set_under('white')
    # c_map.set_over('black')
    plt.figure(figsize=(12, 6))
    
    # 設定橫軸
    plt.xlabel("datetime")
    Z = []
    for iter in dataset:
        Z.append(iter.T[2].astype(float)[:116])
    X = np.arange(1, count+1, 1)
    Y = iter.T[0].astype(float)[:116]
    xx, yy = np.meshgrid(X, Y)
    # 設定縱軸
    plt.ylabel("height")
    Z = np.array(Z)
    print(Z)

    # 繪製風速資料
    # for i in range(count):
    plt.pcolormesh(xx, yy, Z.T, cmap=custom_cmap)
    #plt.gca().set_aspect('equal')  # Ensure equal aspect ratio for clarity

    # 設定colorbar
    cbar = plt.colorbar(label='Wind Speed')
    plt.clim(0, 15)

    # 顯示圖表
    plt.show()

    plt.savefig('wind.png')

if __name__ == "__main__":

    # defines the file directory that contains the HPL files
    root = os.getcwd()
    file_path = root + "/ProcessedData"

    # Read file from the disk
    dataset, time_stamps = createDataset(file_path)
    print(dataset.shape)

    # Modify the all elements in the dictionary into numbers from string
    dataset = dataSetToFloat(dataset)
    
    number_of_data = len(os.listdir(file_path))

    draw(dataset, number_of_data, time_stamps)
    