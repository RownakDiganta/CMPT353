# Exercise 2
# Author: Md Rownak Abtahee Diganta 
# Student ID: 301539632 

import sys 
import pandas as pd 
import matplotlib.pyplot as plt

# To get the command line arguments (as strings), using the built-in sys module as per the instruction (Given)
filename1 = sys.argv[1]
filename2 = sys.argv[2]
# print(filename2)

# Reading file into a dataframe (Given in the instruction)
data_frame_1 = pd.read_csv(filename1, sep=' ', header=None, index_col=1, names= ['lang', 'page', 'views', 'bytes'])
data_frame_2 = pd.read_csv(filename2, sep=' ', header=None, index_col=1, names= ['lang', 'page', 'views', 'bytes'])
# print(data_frame_1.head(5))

# Plot 1: Distribution of Views
# Given hint: using only the first input file, sort the data by the number of views (decreasing). 
#[Hint: sort_values.] If you give plt.plot a single data set, it will be plotted against a 0 to n-1 range, which will be what we want.

sorted_data_frame_1 = data_frame_1.sort_values(by = ['views'], ascending= False)
x_coordinate = sorted_data_frame_1['views'].values # Given hint: pass the underlying NumPy array (data['views'].values) # otherwise index use korbe
plt.figure(figsize=(10, 5))                        # changing the size to something sensible
plt.subplot(1, 2, 1)                               # subplots in 1 row, 2 columns, select the first
plt.title("Popularity Distribution")
plt.xlabel('Rank')
plt.ylabel('Views')
plt.plot(x_coordinate)
#plt.show()

# plot 2:  Hourly Views
# Given hint : you'll need to get the two series into the same DataFrame
# Creating a new dataframe by concatenating the previous dataframes. In this case we will only take views column from the both dataframes 
data_frame_3 = pd.concat([data_frame_1['views'].rename('Hour_1_views'),data_frame_2['views'].rename('Hour_2_views')],axis = 1) # concatenating vertically # important
                                                                                                                             # changing the column names

#print(data_frame_3)

plt.subplot(1, 2, 2)                               # subplots in 1 row, 2 columns, select the first
plt.title("Hourly Correlation")
plt.xlabel('Hour 1 views')
plt.ylabel('Hour 2 views')
plt.xscale('log')
plt.yscale('log')
plt.plot(data_frame_3['Hour_1_views'],data_frame_3['Hour_2_views'],'o',color = '#0000FF',ms = 3) # setting color and marker size to match the sample 
#plt.show()
plt.savefig('wikipedia.png')



