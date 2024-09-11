# Exercise 6
# Author: Md Rownak Abtahee Diganta 
# Student ID: 301539632

import pandas as pd 
import numpy as np
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import matplotlib.pyplot as plt

def main():
    
    # You will need a statistical test that can be used to determine if the means of multiple samples are different, and then decide which ones
    data_frame = pd.read_csv('data.csv')
    data_mean = data_frame.mean()
    print('Sorting implementations and respective mean of their speed:\n')
    print(data_mean)
    print('\n')
    
    # Give a ranking of the sorting implementations by speed,
    # Ref: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rank.htmls (Gained knowledge from here)
    ranked_data_mean = data_mean.rank(axis =0, ascending= True)
    sorted_rank = ranked_data_mean.sort_values(ascending= True)
    print('Sorting implementations and their respective rank(Ascending):\n')
    print(sorted_rank)
    
    # including which ones could not be distinguished. (i.e. which pairs could our experiment not conclude had different running times?)
    # In your analysis, you can almost certainly apply the lesson from the “It's Probably Okay” section in lecture:
    # if you have more than about 40 data points and they are reasonably-normal-looking, then you can use a parametric test
    # I have more than 40 data points. Hence, I can use ANOVA and Turkey's HSD test 
    
    # First let's do ANOVA 
    # Taking inspiration from slides
    anova = stats.f_oneway(data_frame['qs1'], data_frame['qs2'], data_frame['qs3'], data_frame['qs4'], data_frame['qs5'], data_frame['merge1'], data_frame['partition_sort'])
    print('\n',anova,'\n')
    print('ANOVA p-value: ',anova.pvalue,'\n') # This is <0.05 . Hence, the null hypothesis should be rejected 
    
    # Turkey's HSD test 
    # Taking inspiration from slides
    sort_implementation_data = pd.DataFrame({'qs1':data_frame['qs1'],'qs2': data_frame['qs2'],'qs3': data_frame['qs3'], 'qs4':data_frame['qs4'], 'qs5':data_frame['qs5'],'merge1': data_frame['merge1'], 'partition_sort':data_frame['partition_sort']})
    sort_implementation_melt = pd.melt(sort_implementation_data)
    posthoc = pairwise_tukeyhsd(
    sort_implementation_melt['value'], sort_implementation_melt['variable'],
    alpha=0.05)
    print(posthoc)
    
    # Was in the slide for visualization. It helps to have a good idea about the data as visualization helps.
    #fig = posthoc.plot_simultaneous()
    #plt.show()
    
if __name__ == '__main__':
    main()