# Exercise 12
# Author: Md Rownak Abtahee Diganta 
# Student ID: 301539632

# This part I took inspiration from exercise 10 reddit_averages.py.

import sys
import string, re
from pyspark.sql import SparkSession, functions, types

spark = SparkSession.builder.appName('word count').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 8) # make sure we have Python 3.8+
assert spark.version >= '3.2' # make sure we have Spark 3.2+

def main(in_directory, out_directory):
    # 1. Read lines from the files with spark.read.text.
    file = spark.read.text(in_directory)
    #file.show()
    
    # 2. Split the lines into words with the regular expression below.
    # Use the split and explode functions. Normalize all of the strings to lower-case (so “word” and “Word” are not counted separately.)
    # Given in the instructions 
    wordbreak = r'[%s\s]+' % (re.escape(string.punctuation),)  # regex that matches spaces and/or punctuation
    
    # ref: https://spark.apache.org/docs/3.1.1/api/python/reference/api/pyspark.sql.functions.split.html (Gained knowledge)
    file_1 = file.select(functions.split(file['value'], wordbreak, -1).alias('value_array'))
    #file_1.show()
    # ref: https://spark.apache.org/docs/3.1.3/api/python/reference/api/pyspark.sql.functions.explode.html (Gained knowledge)
    file_2 = file_1.select(functions.explode(file_1['value_array']).alias('elements'))
    #file_2.show()
    # ref: https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.lower.html (Gained knowledge)
    file_3 = file_2.select(functions.lower("elements").alias('lower_elem'))
    #file_3.show()
    
    # 3. Count the number of times each word occurs.
    file_4 = file_3.groupBy(file_3['lower_elem'])
    # ref: https://www.geeksforgeeks.org/pyspark-groupby-dataframe-with-aggregation-or-count/ (Gained Knowledge)
    file_5 = file_4.count()
    #file_5.show()
    
    # 4.Sort by decreasing count (i.e. frequent words first) and alphabetically if there's a tie.
    file_6 = file_5.sort("count", ascending = False)
    #file_6.show()
    
    # 5. Notice that there are likely empty strings being counted: remove them from the output.
    # (They come from spaces at the start/end of lines in the original input.)
    # ref: https://www.geeksforgeeks.org/removing-blank-strings-from-a-pyspark-dataframe/ (Gained Knowledge)
    
    file_7 = file_6.filter(file_6.lower_elem !='')
    #file_7.show()
    
    # 6. Write results as CSV files with the word in the first column, and count in the second (uncompressed: they aren't big enough to worry about).
    # naming the column with words as word as the instruction said. 
    final_file = file_7.withColumnRenamed("lower_elem","word")
    #final_file.show()
    final_file.write.csv(out_directory)
if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)