#!/usr/bin/python
import sys
import pandas as pd
import calendar
#import datetime as dt
  
# CICS 397A Homework 2 Part II
#  
# Fill in the bodies of the missing functions as specified by the comments.  For this assigment,
# you should use the pandas module to do all the data manipulation and aggegation rather than
# looping through the data yourself.  (It is okay to loop through your DataFrame in order to print
# the results in the correct format, however.)
#


# The main() function below will be executed when your program is run.  
# Note that Python does not require a main() function, but it is 
# considered good style (as is enclosing the __name__ == '__main__'
# conditional below, what does that do?)
#
def main(file_name):
    df = read_data(file_name)
    total_cost(df)
    least_common_locs(df)
    most_common_locs(df)
    state_totals(df)
    unique_dates(df)
    month_avg(df)


# Exercise 0. (10 points)
#  
# Read in the csv file into a pandas DataFrame using the read_csv() function.
#      date: class date
#      mileage: integer
#      location: string 
#      gallons: float
#      cost: float 
#
def read_data(file_name):

    #
    # fill in function body here
    #
    df = pd.read_csv(file_name)
    df['date'] = pd.to_datetime(df['date'].fillna(0))
    df['mileage'] = df['mileage'].fillna(0).astype(int)
    df['location'] = df['location'].fillna(0).astype(str)
    df['gallons'] = df['gallons'].fillna(0).astype(float)
    df['cost'] = df['cost'].replace('[\$,]', '', regex=True).fillna(0).astype(float)
    return df

# Exercise 1. (15 points)
#
# Print out the total amount of money spent on gas.  Still depressing.
# 
def total_cost(df):
    print("\nExercise 1:")
    #print(df['cost'].sum())
    print('${:,.2f}'.format(df['cost'].sum()))
    #
    # fill in function body here
    #
    #return df['cost'].sum()

# Exercise 2. (15 points)
#
# Print out the number of refueling locations that were visited exactly once.
# 
def least_common_locs(df):
    print("\nExercise 2:")
    print(len(df['location'].value_counts()[df['location'].value_counts() == 1].index))
    #
    # fill in function body here
    #


# Exercise 3. (15 points)
#
# Print out the 10 most common refueling locations, along with the number of times they
# appear in the data, in descending order.  Each output line should look like:
#     Honolulu, HI 42
# 
def most_common_locs(df):
    print("\nExercise 3:")
    print(df['location'].value_counts()[:10].to_string(header=None))
    #
    # fill in function body here
    #


# Exercise 4. (15 points)
#
# Print out the total number of visits for each state (as designated by the two-letter
# abbreviation at the end of the location string, one per line, in alphabetical order:
#     CA 42
#     HI 19 
#
def state_totals(df):
    print("\nExercise 4:")
    df['text_new1'] = [(x.split(","))[-1].strip(" ") for x in df['location']]
    df['text_new1'] = df['text_new1'][df['text_new1'] != '0']
    print(df['text_new1'].value_counts().to_string(header=None))


# Exercise 5. (15 points)
#
# Print out the total number unique dates in the calendar year that refueling took place
# (this number should be less than 366!).
#
def unique_dates(df):
    print("\nExercise 5:")
    df['text_new1'] = [(x.month,x.day) for x in df['date']]
    print(df['text_new1'].value_counts()[df['text_new1'].value_counts() == 1].sum())



# Exercise 6. (15 points)
#
# Print out the average price per gallon for each month of the year, in calendar order, like so:
#     January $3.12
#     February $2.89
#     ...
#
def month_avg(df):
    print("\nExercise 6:")
    if (df['date'].count() != df['cost'].count()):
        print("InCorrect Comparison")
    for k in range(1, 13):
        list2 = []
        for (x,y) in zip(df['date'], df['cost']):
            if x.month == k:
                list2.append(y)
        dfObj = pd.DataFrame(list2)
        print('{} ${:,.2f}'.format(calendar.month_name[k], dfObj[0].mean()))

#########################

if __name__ == '__main__':
    data_file_name = 'mustard_data.csv'
    #data_file_name = sys.argv[1]
    main(data_file_name)




