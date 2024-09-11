# Exercise 1
# Author: Md Rownak Abtahee Diganta 
# Student ID: 301539632 

import pandas as pd 

#Getting arrays out of the data file. Given in the question.

totals = pd.read_csv('totals.csv').set_index(keys=['name'])
#print(totals)
counts = pd.read_csv('counts.csv').set_index(keys=['name'])
#print(counts)

# Question 1 : Which city had the lowest total precipitation over the year?
# Given hint : sum across the rows (axis 1);use argmin to determine which row has the lowest value. 
#              Print the row number. 
# This was done previously in numpy. Now changing it to pandas. 
# similar function like argmin in pandas is idxmin

City_total_yearly = totals.sum(axis = 1)                        # from the total array summing horizontally 
lowest_precipitation_index = City_total_yearly.idxmin(axis = 0) # idxmin gets the index of the lowest value in an array 
print('City with lowest total precipitation:')
print(lowest_precipitation_index)

# Question 2: Determine the average precipitation in these locations for each month.
# Given hint: That will be the total precipitation for each month (axis 0), 
#             divided by the total observations for that months. Print the resulting array.
# This was done previously in numpy. Now changing it to pandas. 

Monthly_totals = totals.sum(axis = 0)                  # from the total array summing vertically
Monthly_observation = counts.sum(axis = 0)              # from the count array summing vertically
Monthly_average_precipitation = (Monthly_totals/Monthly_observation)
print('Average precipitation in each month:')
print(Monthly_average_precipitation)

# Question 3: Give the average precipitation (daily precipitation averaged over the month) for each city by printing the array.
# Thinking : we need City_total_yearly which is already done in the part of question 1. We need to find City_counts_yearly
# This was done previously in numpy. Now changing it to pandas. 

City_counts_yearly = counts.sum(axis = 1)                  # from the total array summing vertically
City_average_precipitation = (City_total_yearly/City_counts_yearly)
print('Average precipitation in each city:')
print(City_average_precipitation)


