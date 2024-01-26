import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

#Find the current directory and read off all files
current_directory = os.getcwd()
entries = os.listdir(current_directory)
files = [f for f in entries if os.path.isfile(os.path.join(current_directory, f))]
print(files)

files_sanitised = []
files_csv = []

#Find all .csv files and append to list. Also strip the A.csv from each.
for file in files:
    if '.csv' in file:
        df = pd.read_csv(file)
        count = df[' count0 ']
        if len(count) > 1:
            files_csv.append(file)
            file_stripped = ''.join(letter for letter in file if letter.isdigit())
            files_sanitised.append(file_stripped)
    
    
voltages = []

#Add the numerical value from the sanitised list to the voltages array
for i in files_sanitised:
    voltages.append(float(i))

voltages.sort()

mean_counts = []
mean_counts_upper = []
mean_counts_lower = []
count_err = []

def mean(x):
    N = len(x)
    total = 0

    for i in x:
        total += i

    mean1 = total / N

    return mean1

def variance(x):
    N = len(x)
    total_x = 0
    total_xsquare = 0

    for i in x:
        total_x += i
        total_xsquare += i**2

    x_bar = total_x / N
    x_bar_square = total_xsquare / N

    var = x_bar_square - x_bar**2

    return abs(var)

for file in files_csv:
    df = pd.read_csv(file)
    time = df[' time ']
    count = df[' count0 ']

    if len(count) > 1:

        intervals = len(time) - 1
        
        dt = []
        dcount = []
        freq = []

        for i in range (0, intervals):
            dt_i = time[i+1] - time[i]
            dt.append(dt_i)
        
        for j in range(0,intervals):
            count_i = count[i+1] - count[i]
            dcount.append(count_i)

        for k in range(0, intervals):
            freq_i = dcount[k] / dt[k]
            freq_i *= 1000 #Convert from per millisecond to second
            freq.append(freq_i)

        count_avg = mean(freq)
        mean_counts.append(count_avg)
    
    else:
        pass


log_counts = np.log(mean_counts)
plt.scatter(voltages, log_counts, marker='o', label='data', s=3)
plt.xlabel('Voltage/mV')
plt.ylabel('log(Frequency / Hz)')
plt.title('Dark Count Rate vs Threshold Voltage')
plt.legend()
plt.savefig('Dark Count 1')
plt.show()

