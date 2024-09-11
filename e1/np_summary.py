# Exercise 1
# Author: Md Rownak Abtahee Diganta 
# Student ID: 301539632 

import numpy as np

# Getting numpy arrays out of the data file. Given in the question.
data = np.load('monthdata.npz')
totals = data['totals']
counts = data['counts']

# Question 1 : Which city had the lowest total precipitation over the year?
# Given hint : sum across the rows (axis 1);use argmin to determine which row has the lowest value. 
#              Print the row number. 


City_total_yearly = totals.sum(axis = 1)                  # from the total array summing horizontally 
lowest_precipitation_index = np.argmin(City_total_yearly) # argmin gets the index of the lowest value in an array 
print('Row with lowest total precipitation:')
print(lowest_precipitation_index)

# Question 2: Determine the average precipitation in these locations for each month.
# Given hint: That will be the total precipitation for each month (axis 0), 
#             divided by the total observations for that months. Print the resulting array.

Monthly_totals = totals.sum(axis = 0)                  # from the total array summing vertically
Monthly_observation = counts.sum(axis = 0)              # from the counts array summing vertically
Monthly_average_precipitation = (Monthly_totals/Monthly_observation)
print('Average precipitation in each month:')
print(Monthly_average_precipitation)

# Question 3: Give the average precipitation (daily precipitation averaged over the month) for each city by printing the array.
# Thinking : we need City_total_yearly which is already done in the part of question 1. We need to find City_counts_yearly

City_counts_yearly = counts.sum(axis = 1)                  # from the total array summing vertically
City_average_precipitation = (City_total_yearly/City_counts_yearly)
print('Average precipitation in each city:')
print(City_average_precipitation)

# Question 4: Calculate the total precipitation for each quarter in each city (i.e. the totals for each station across three-month groups).
# Given hint: You can assume the number of columns will be divisible by 3. 
#             use the reshape function to reshape to a 4n by 3 array, sum, and reshape back to n by 4.

number_of_rows = totals.shape[0] # We can also use counts array as they are same size.To be safe using totals
# number_of_col  = totals.shape[1]

reshaped_totals_1 = totals.reshape((4*number_of_rows,3)) # reshaping as per the given hint 
total_horizontally_1 = reshaped_totals_1.sum(axis = 1)   # Summing horizontally 

reshaped_totals_2 = total_horizontally_1.reshape(number_of_rows,4) # reshaping again as per the given hint 

print('Quarterly precipitation totals:')
print(reshaped_totals_2)
