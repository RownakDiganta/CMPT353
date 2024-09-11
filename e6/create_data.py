# Exercise 6
# Author: Md Rownak Abtahee Diganta 
# Student ID: 301539632

import time
from implementations import all_implementations
import pandas as pd 
import numpy as np

def main():
    # We are concerned with the seven sorting implementations given in the all_implementations array: qs1, qs2, qs3, qs4, qs5, merge1, partition_sort.
    all_implementations_array = ['qs1','qs2','qs3','qs4','qs5','merge1','partition_sort']
    # Creating data frame to store data and later convert it to data.csv 
    data = pd.DataFrame(columns= all_implementations_array)

    # ...
    # Creating/ initializing lists to store value in it 
    qs1 = []
    qs2 = []
    qs3 = []
    qs4 = []
    qs5 = []
    merge1 = []
    partition_sort = []


    list_array = [qs1,qs2,qs3,qs4,qs5,merge1,partition_sort]

    for i in range(200):
        random_array = np.random.randint(0,2000,200)
        z = 0
        for sort in all_implementations:
            st = time.time()
            res = sort(random_array)
            en = time.time()
            list_array[z].append(en - st)
            z = z+1

    # storing values from lists to their respective columns in the data frame 
    data['qs1'] = qs1
    data['qs2'] = qs2
    data['qs3'] = qs3
    data['qs4'] = qs4
    data['qs5'] = qs5
    data['merge1'] = merge1
    data['partition_sort'] = partition_sort

    data.to_csv('data.csv',index = False)

if __name__ == '__main__':
    main()