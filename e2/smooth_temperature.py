# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 20:45:42 2021

@author: vaibh
"""
import sys
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import statsmodels.api as sm
from pykalman import KalmanFilter 

filename = sys.argv[1]
cpu_data = pd.read_csv(filename)

# Ensure the timestamp is correctly parsed, handling milliseconds as well
cpu_data['timestamp'] = pd.to_datetime(cpu_data['timestamp'], format='%Y-%m-%d %H:%M:%S.%f', errors='coerce')
cpu_data = cpu_data.dropna(subset=['timestamp'])  # Drop rows where timestamp could not be parsed

timestamp = cpu_data['timestamp'].apply(np.datetime64)
temperature = cpu_data['temperature'].astype(float)

# LOWESS smoothing
lowess = sm.nonparametric.lowess
loess_smoothed = lowess(temperature, timestamp, frac=0.035)

# Prepare data for the Kalman Filter
kalman_data = cpu_data[['temperature', 'cpu_percent', 'sys_load_1', 'fan_rpm']].dropna()  # Ensure no missing values

initial_state = kalman_data.iloc[0]
observation_covariance = np.diag([0.75, 0.75, 0.75, 0.75]) ** 2
transition_covariance = np.diag([0.05, 0.05, 0.05, 0.05]) ** 2
transition = [[0.97, 0.5, 0.2, -0.001], 
              [0.1, 0.4, 2.2, 0], 
              [0, 0, 0.95, 0], 
              [0, 0, 0, 1]]

kf = KalmanFilter(initial_state_mean=initial_state,
                  observation_covariance=observation_covariance,
                  transition_covariance=transition_covariance,
                  transition_matrices=transition)

kalman_smoothed, _ = kf.smooth(kalman_data)

# Plotting the results
plt.figure(figsize=(12, 4))
plt.plot(cpu_data['timestamp'], cpu_data['temperature'], 'b.', alpha=0.5)
plt.plot(cpu_data['timestamp'], loess_smoothed[:, 1], 'r-')
plt.plot(cpu_data['timestamp'], kalman_smoothed[:, 0], 'g-')
plt.legend(['Data Points', 'Loess Smoothed', 'Kalman Smoothed'])
plt.title('CPU Temperature')
plt.xlabel('Time')
plt.ylabel('Temperature (°C)')
plt.show()
