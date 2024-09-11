# Exercise 3
# Author: Md Rownak Abtahee Diganta 
# Student ID: 301539632 

import sys 
import pandas as pd 
import matplotlib.pyplot as plt
from statsmodels.nonparametric.smoothers_lowess import lowess # From the slides
from pykalman import KalmanFilter                             # From slides 
import numpy as np

# To get the command line arguments (as strings), using the built-in sys module as per the instruction (Given)
filename1 = sys.argv[1]

# Reading file into cpu_data (in the first hint there is a variable called cpu_data. Probably, it is the data frame)
# Also parsing timestamp data while reading the file.
# Also changing data types of columns and removing NaN values 

cpu_data = pd.read_csv(filename1, parse_dates = ['timestamp'])      # Parsing timestamp to datetime format 
cpu_data['temperature'] = cpu_data['temperature'].astype('float')   # Converting temperature to float type
cpu_data = cpu_data.dropna()                                        # Dropping all the NaN value in the data frame

# Checking the values 
#print(cpu_data['temperature'])
#print(cpu_data['timestamp'])

# LOESS Smoothing
loess_smoothed = lowess(endog = cpu_data['temperature'], exog= cpu_data['timestamp'], frac= 0.029) # From the given site

# Kalman Smoothing
# Taken from hint 
kalman_data = cpu_data[['temperature', 'cpu_percent', 'sys_load_1', 'fan_rpm']]
initial_state = kalman_data.iloc[0]
observation_covariance = np.diag([0.8, 0.8, 0.8, 0.8]) ** 2 # TODO: shouldn't be zero
transition_covariance = np.diag([0.045, 0.045, 0.045, 0.045]) ** 2 # TODO: shouldn't be zero
transition = [[0.94,0.5,0.2,-0.001], [0.1,0.4,2.1,0], [0,0,0.94,0], [0,0,0,1]] # TODO: shouldn't (all) be zero

# From slide
kf = KalmanFilter(    
    initial_state_mean=initial_state,
    initial_state_covariance=observation_covariance,
    observation_covariance=observation_covariance,
    transition_covariance=transition_covariance,
    transition_matrices=transition)

# Taken from hint
kalman_smoothed, _ = kf.smooth(kalman_data)


# Plotting 
plt.figure(figsize=(12, 4))                                               # From the given hint 
plt.plot(cpu_data['timestamp'], cpu_data['temperature'], 'b.', alpha=0.5) # From the given hint
plt.plot(cpu_data['timestamp'], loess_smoothed[:, 1], 'r-')               # From the given hint 
plt.plot(cpu_data['timestamp'], kalman_smoothed[:, 0], 'g-')              # From the given hint 

# Taken from Exercise 1 (As per the hint)
# Add a legend to your plot so we (and you) can distinguish the data points, LOESS-smoothed line, and Kalman-smoothed line (Instruction)
plt.legend(['data points', 'LOESS-smoothed line','Kalman-smoothed line'])
plt.xlabel('timestamp')
plt.ylabel('temperature')
# Adding diagram 
plt.title('CPU Temperature Noise Reduction')                              # ref: https://www.geeksforgeeks.org/matplotlib-pyplot-title-in-python/
#plt.show() # maybe easier for testing
plt.savefig('cpu.svg') # saving the plot (Given in the instruction) 
