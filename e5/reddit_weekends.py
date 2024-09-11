# Exercise 5
# Author: Md Rownak Abtahee Diganta 
# Student ID: 301539632 

import sys
import pandas as pd 
from datetime import date # From the given website of the instruction
from scipy import stats
# import matplotlib.pyplot as plt
import numpy as np 

OUTPUT_TEMPLATE = (
    "Initial T-test p-value: {initial_ttest_p:.3g}\n"
    "Original data normality p-values: {initial_weekday_normality_p:.3g} {initial_weekend_normality_p:.3g}\n"
    "Original data equal-variance p-value: {initial_levene_p:.3g}\n"
    "Transformed data normality p-values: {transformed_weekday_normality_p:.3g} {transformed_weekend_normality_p:.3g}\n"
    "Transformed data equal-variance p-value: {transformed_levene_p:.3g}\n"
    "Weekly data normality p-values: {weekly_weekday_normality_p:.3g} {weekly_weekend_normality_p:.3g}\n"
    "Weekly data equal-variance p-value: {weekly_levene_p:.3g}\n"
    "Weekly T-test p-value: {weekly_ttest_p:.3g}\n"
    "Mann-Whitney U-test p-value: {utest_p:.3g}"
)


def main():
    reddit_counts = sys.argv[1]

    # ...
    counts = pd.read_json(sys.argv[1], lines=True)
    # Instruction: look only at values (1) in 2012 and 2013, and (2) in the /r/canada subreddit.
    # ref: https://pandas.pydata.org/docs/reference/api/pandas.Series.dt.weekday.html (gained knowledge)
    counts['week_day'] = counts['date'].dt.weekday
    # ref: https://pandas.pydata.org/docs/reference/api/pandas.Series.dt.year.html (gained knowledge)
    counts['year']     = counts['date'].dt.year
    # separating rows having subreddit canada and making a data frame 
    counts_subreddit = counts[counts['subreddit'] == 'canada']
    #print(counts_subreddit)
    # separating rows having year 2012 and 2013 and making a data frame 
    counts_final = counts_subreddit[(counts_subreddit['year']== 2012) | (counts_subreddit['year']== 2013)]
    #print(counts_final)
    # separating weekends and weekdays and making two data frames
    weekends = counts_final[(counts_final['week_day']==5)|(counts_final['week_day']==6)]
    weekdays = counts_final[~((counts_final['week_day']==5)|(counts_final['week_day']==6))]
    #print(weekends)
    #print(weekdays)
    
    # Student's T-Test 
    initial_p = stats.ttest_ind(weekends['comment_count'],weekdays['comment_count']).pvalue
    initial_weekday_n_p = stats.normaltest(weekdays['comment_count']).pvalue
    initial_weekend_n_p = stats.normaltest(weekends['comment_count']).pvalue
    initial_levene = stats.levene(weekends['comment_count'],weekdays['comment_count']).pvalue
    
    # Fix 1: transforming data might save us.
    
    
    # For log p value is way small for equal-variance
    #transformed_weekdays = np.log(weekdays['comment_count'])
    #transformed_weekends = np.log(weekends['comment_count'])
    
    # For exp p values are NaN
    #transformed_weekdays = np.exp(weekdays['comment_count'])
    #transformed_weekends = np.exp(weekends['comment_count'])
    
    # sqrt is giving 0.556 for equal-variance
    transformed_weekdays = np.sqrt(weekdays['comment_count'])
    transformed_weekends = np.sqrt(weekends['comment_count'])
    
    # # For log p value i way too small (7.39e-08)for equal-variance
    #transformed_weekdays = (weekdays['comment_count'])**2
    #transformed_weekends = (weekends['comment_count'])**2
    
    transformed_weekday_n_p = stats.normaltest(transformed_weekdays).pvalue
    transformed_weekend_n_p = stats.normaltest(transformed_weekends).pvalue
    transformed_levene      = stats.levene(transformed_weekends,transformed_weekdays).pvalue
    
# Fix 2: the Central Limit Theorem might save us.
    weekends_i_calendar = weekends['date'].dt.isocalendar()
    weekends_i_calender = weekdays['date'].dt.isocalendar()
    
    # copying the data frame to not mess with the initial data frame we created 
    weekends_c = weekends.copy()
    weekdays_c = weekdays.copy()

    # REF: https://www.w3schools.com/python/pandas/ref_df_assign.asp (Gained knowledge from here)
    
    weekends_c = weekends_c.assign(
        year=weekends['date'].dt.isocalendar().year, # Used isocalendar as instructed
        week=weekends['date'].dt.isocalendar().week  # Used isocalendar as instructed
    )
    weekdays_c = weekdays_c.assign(
        year=weekdays['date'].dt.isocalendar().year, # Used isocalendar as instructed
        week=weekdays['date'].dt.isocalendar().week  # Used isocalendar as instructed
    )

    # Grouping year and week to find the mean 
    weekends_grouped = weekends_c.groupby(by=['year', 'week'])[['comment_count']].mean()
    weekdays_grouped = weekdays_c.groupby(by=['year', 'week'])[['comment_count']].mean()

    # Finding p values 
    weekly_weekday_n_p = stats.normaltest(weekdays_grouped['comment_count']).pvalue
    weekly_weekend_n_p = stats.normaltest(weekends_grouped['comment_count']).pvalue
    weekly_levene = stats.levene(weekends_grouped['comment_count'], weekdays_grouped['comment_count']).pvalue
    weekly_ttest = stats.ttest_ind(weekends_grouped['comment_count'], weekdays_grouped['comment_count']).pvalue
    
    # Fix 3: a non-parametric test might save us.
    # ref: https://www.reneshbedre.com/blog/mann-whitney-u-test.html (Gained knowledge)
    Mann_utest = stats.mannwhitneyu(weekends['comment_count'], weekdays['comment_count'], alternative='two-sided').pvalue
    
    print(OUTPUT_TEMPLATE.format(
        initial_ttest_p= initial_p,
        initial_weekday_normality_p= initial_weekday_n_p,
        initial_weekend_normality_p= initial_weekend_n_p,
        initial_levene_p= initial_levene,
        transformed_weekday_normality_p= transformed_weekday_n_p ,
        transformed_weekend_normality_p= transformed_weekend_n_p ,
        transformed_levene_p= transformed_levene,
        weekly_weekday_normality_p= weekly_weekday_n_p ,
        weekly_weekend_normality_p= weekly_weekend_n_p,
        weekly_levene_p= weekly_levene,
        weekly_ttest_p= weekly_ttest,
        utest_p= Mann_utest,
    ))


if __name__ == '__main__':
    main()
