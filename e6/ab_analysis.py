# Exercise 6
# Author: Md Rownak Abtahee Diganta 
# Student ID: 301539632

import sys
import pandas as pd
from scipy.stats import chi2_contingency # from site given in the instructions
from scipy.stats import mannwhitneyu     # from site given in the instructions


OUTPUT_TEMPLATE = (
    '"Did more/less users use the search feature?" p-value:  {more_users_p:.3g}\n'
    '"Did users search more/less?" p-value:  {more_searches_p:.3g} \n'
    '"Did more/less instructors use the search feature?" p-value:  {more_instr_p:.3g}\n'
    '"Did instructors search more/less?" p-value:  {more_instr_searches_p:.3g}'
)


def main():
    searchdata_file = sys.argv[1]
    json_file = pd.read_json(searchdata_file,orient = 'records', lines = True)
    #print(json_file)
    
    # Instruction:  Users with an odd-numbered uid were shown a new-and-improved search box. Others were shown the original design.
    # separating the odd and even numbered uids' users
    
    odd_users = json_file[json_file['uid']%2 != 0]
    #print(odd_users)
    even_users = json_file[json_file['uid']%2 == 0]
    #print(even_users)
    
    # getting rid of NaN values 
    
    odd_users = odd_users.dropna()
    even_users= even_users.dropna()
    
    # Dividing into categories and making contingency table 
    odd_users_atleast_once = odd_users[odd_users['search_count'] != 0]
    odd_users_never        = odd_users[odd_users['search_count'] == 0]
    even_users_atleast_once= even_users[even_users['search_count'] != 0]
    even_users_never = even_users[even_users['search_count'] == 0]
    
    contigency_table = [[len(odd_users_atleast_once),len(odd_users_never)],[len(even_users_atleast_once),len(even_users_never)]]
    # print(contigency_table)
    
    # Did more users use the search feature? (More precisely: did a different fraction of users have search count > 0?)
    chi2 = chi2_contingency(contigency_table) # following the slides 
    more_users_pvalue = chi2.pvalue # in the slide this is the manner used to get pvalue of chi2 
    
    # Did users search more often? (More precisely: is the number of searches per user different?)
    more_searches_pvalue = mannwhitneyu(odd_users['search_count'],even_users['search_count']).pvalue 
    
    # Repeat the above analysis looking only at instructors.
    odd_instructors = odd_users[odd_users['is_instructor'] == True]
    even_instructors = even_users[even_users['is_instructor'] == True]
    
    # Dividing into categories and making contingency table 
    odd_instructors_atleast_once = odd_instructors[odd_instructors['search_count'] != 0]
    odd_instructors_never        = odd_instructors[odd_instructors['search_count'] == 0]
    even_instructors_atleast_once= even_instructors[even_instructors['search_count'] != 0]
    even_instructors_never = even_instructors[even_instructors['search_count'] == 0]
    
    contigency_table_instructors = [[len(odd_instructors_atleast_once),len(odd_instructors_never)],[len(even_instructors_atleast_once),len(even_instructors_never)]]
    # Did more users use the search feature? (More precisely: did a different fraction of users have search count > 0?)
    chi2_instructors = chi2_contingency(contigency_table_instructors) # following the slides 
    more_instructors_pvalue = chi2_instructors.pvalue # in the slide this is the manner used to get pvalue of chi2 
    
    # Did users search more often? (More precisely: is the number of searches per user different?)
    more_searches_pvalue_instructors = mannwhitneyu(odd_instructors['search_count'],even_instructors['search_count']).pvalue 
   
    
    # ...

    # Output
    print(OUTPUT_TEMPLATE.format(
        more_users_p= more_users_pvalue, 
        more_searches_p= more_searches_pvalue,
        more_instr_p= more_instructors_pvalue ,
        more_instr_searches_p= more_searches_pvalue_instructors,
    ))


if __name__ == '__main__':
    main()
