import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

#Find the current directory and read off all files
current_directory = os.getcwd()
entries = os.listdir(current_directory)
files = [f for f in entries if os.path.isfile(os.path.join(current_directory, f))]
#print(files)

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

mean_counts_1 = [] #For first column if reading more than 1 set of data

def mean(x):
    N = len(x)
    total = 0

    for i in x:
        total += i

    mean1 = total / N

    return mean1


for file in files_csv:
    df = pd.read_csv(file)
    time = df[' time ']
    count = df[' count0 ']

    if len(count) > 1 and len(time) > 1:

        
        dt = time[len(time)-1] - time[0]
        dcount = count[len(count)-1] - count[0]
        
        freq = dcount / dt * 1000

        mean_counts_1.append(freq)
    
    else:
        pass


plt.scatter(voltages, mean_counts_1, marker='o', s=3, label = 'data1')
plt.plot(voltages, mean_counts_1)
plt.yscale('log')
plt.xlabel('Voltage/mV')
plt.ylabel('log(Frequency / Hz)')
plt.title('Dark Count Rate vs Threshold Voltage')
plt.savefig('Dark Count 1')
plt.show()

