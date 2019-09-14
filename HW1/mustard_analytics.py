#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import csv
import seaborn as sns
import operator
from datetime import date


# CICS 397A Homework 1
#  
# Fill in the bodies of the missing functions as specified by the comments.
#


# The main() function below will be executed when your program is run.  
# Note that Python does not require a main() function, but it is 
# considered good style (as is including the __name__ == '__main__'
# conditional below, what does that do?)
#
def main(file_name):
    rows = read_data(file_name)
    total_cost(rows)
    least_common_locs(rows)
    most_common_locs(rows)
    state_totals(rows)
    unique_dates(rows)
    month_avg(rows)
    highest_thirty(rows)
    plot_monthly(rows)
    plot_mpg(rows)
    plot_betweens(rows)


# Exercise 0. (10 points)
#  
# Read in the csv file and return a list of tuples representing the data, transforming each 
# field as follows:
#      date: class date (see datetime module)
#      mileage: integer
#      location: string 
#      gallons: float
#      cost: float 
#    
# Do not return a tuple for the header row.  While you can process the rawtext using string 
# functions, to receive full credit you must use Python's built in csv module.  
#    
def read_data(file_name='mustard_data.csv'):
    with open(file_name) as f:
        input = f.readlines()
        rows = []
        i = 1
        while i < len(input):
            newStr = ['{}'.format(x) for x in list(csv.reader([input[i]], delimiter=',', quotechar='"'))[0]]
            j = 0
            t_arr = []
            while j < len(newStr):
                if (j == 0):
                    timearr = newStr[j].split('/')
                    if len(timearr) == 3:
                        year = int(timearr[2])
                        month = int(timearr[0])
                        day = int(timearr[1])
                        t0 = date(year, month, day)
                    else:
                        t0 = date.min
                    t_arr.append(t0)
                if (j == 1):
                    if (len(newStr[j]) == 0):
                        t_arr.append(int(0))
                    else:
                        fishy = int(newStr[j])
                        t_arr.append(fishy)
                if (j == 2):
                    t_arr.append(newStr[j])
                if (j == 3):
                    if (len(newStr[j]) == 0):
                        t_arr.append(float(0))
                    else:
                        t_arr.append(float(newStr[j]))
                if (j == 4):
                    if (len(newStr[j]) == 0):
                        num = float(0)
                        t_arr.append(num)
                    else:
                        num = float(newStr[j][1:])
                        t_arr.append(float(num))
                j += 1
            rows.append(tuple(t_arr))
            i += 1
    f.close()
    return rows


# Exercise 1. (5 points)
#
# Print out the total amount of money spent on gas.  Depressing.
# 
def total_cost(rows):
    print("\nExercise 1:")
    tcost = 0
    for x in rows:
        tcost += x[-1]
    print("$%.2f" % tcost)
    return (tcost)


# Exercise 2. (5 points)
#
# Print out the number of refueling locations that were visited exactly once.
# 
def least_common_locs(rows):
    print("\nExercise 2:")
    location = []
    #
    # fill in function body here
    #
    for x in rows:
        if (x[2] not in location):
            location.append(x[2])
        elif (x[2] in location):
            location.remove(x[2])
    print(location)
    return location


# Exercise 3. (8 points)
#
# Print out the 10 most common refueling locations, along with the number of times they
# appear in the data, in descending order.  Each output line should look like:
#     Honolulu, HI 42
# 
# Hint: store the locations and counts in a dictionary, then convert the dictionary into a list of
# tuples that can be sorted using Python's sorted() or sort() functions (the "Key Functions" 
# section of https://docs.python.org/3.6/howto/sorting.html might be helpful).
#
def most_common_locs(rows):
    print("\nExercise 3:")
    pathways = {}
    for x in rows:
        place = x[2]
        visits = pathways.get(place)
        if (visits == None):
            pathways[place] = 1
        else:
            pathways.update({place: visits + 1})
    TheList = sorted(list(pathways.items()), key=operator.itemgetter(1), reverse=True)[:10]
    for x in TheList:
        print(x)
    #
    # fill in function body here
    #


# Exercise 4. (8 points)
#
# Print out the total number of visits for each state (as designated by the two-letter
# abbreviation at the end of the location string, one per line, in alphabetical order:
#     CA 42
#     HI 19 
#
def state_totals(rows):
    print("\nExercise 4:")
    pathways = {}
    for x in rows:
        place = x[2]
        if (",") in place:
            state = place[-2:]
        elif (place == ''):
            continue
        elif (place != ''):
            state = place
        visits = pathways.get(state)
        if (visits == None):
            pathways[state] = 1
        else:
            pathways.update({state: visits + 1})
    TheList = sorted(list(pathways.items()), key=operator.itemgetter(0))
    for x in TheList:
        print(x)
    return TheList
    #
    # fill in function body here
    #


# Exercise 5. (8 points)
#
# Print out the total number unique dates in the calendar year that refueling took place
# (this number should be less than 366!).
#
def unique_dates(rows):
    print("\nExercise 5:")
    repeats = []
    udays = []
    for x in rows:
        month = x[0].month
        day = x[0].day
        if [month, day] not in repeats:
            repeats.append([month, day])
            udays.append([month, day])
            continue
        elif [month, day] in udays:
            udays.remove([month, day])
    print(len(udays))
    return (len(udays))
    #
    # fill in function body here
    #


# Exercise 6. (10 points)
#
# Print out the average price per gallon for each month of the year, in calendar order, like so:
#     January $3.12
#     February $2.89
#     ...
# 
# For full credit, use the functions in Python's datetime module to manipulate the date objects.
#
def month_avg(rows):
    print("\nExercise 6:")
    all = {}
    for x in rows:
        month_name = x[0].month
        price = x[-1]
        if all.get(month_name) == None:
            if price == '':
                all[month_name] = [0]
                continue
            all[month_name] = [price]
        else:
            if price == '':
                all.get(month_name).append(0)
                continue
            else:
                all.get(month_name).append(price)
    ans = []
    for key in sorted(all.keys()):
        print("%s  $%.2f" % (date(1900, key, 1).strftime('%B'), sum(all.get(key)) / len(all.get(key))))
        ans.append((date(1900, key, 1).strftime('%B'), sum(all.get(key)) / len(all.get(key))))
    return ans
    #
    # fill in function body here
    #


# Exercise 7. (10 points)
#
# Print out the start and end dates for top three periods with the most miles driven in thirty
# days or less.  The periods should not overlap (you should select them in a greedy manner; that
# is, find the highest mileage period first, and then select from outside that window).  Print
# the start and end dates, followed by the total mileage like so (note the date format):
#     1995-02-14 1995-03-16 502 miles
#     1991-12-21 1992-01-16 456 miles
#     1997-06-01 1997-06-28 384 miles
#
# Again, you should use the date wrangling functions found in Python's datetime module.
#
def highest_thirty(rows):
    print("\nExercise 7:")
    i = 0
    ans = []
    while i < len(rows):
        startdate = rows[i][0]
        if (startdate == date.min):
            i += 1
            continue
        j = i
        miles = 0
        while j < len(rows):
            if (rows[j][0] == date.min):
                j += 1
                miles += rows[j][1]
                continue
            if (rows[j][0] - startdate).days <= 30:
                enddate = rows[j][0]
                miles += rows[j][1]
            elif ((rows[j][0] - startdate).days > 30):
                break
            j += 1
        ans.append((startdate, enddate, miles))
        i += 1
    ans.sort(key=lambda tup: tup[2], reverse=True)
    output = [ans[0]]
    var = 1
    print(output[-1][0], output[-1][1], str(output[-1][2]) + " miles")
    while len(output) < 3:
        startdate123 = (ans[var])[0]
        last_end = output[-1][1]
        if (startdate123 >= last_end):
            output.append(tuple(ans[var]))
            print(output[-1][0], output[-1][1], str(output[-1][2]) + " miles")
        var += 1
    return output
    #
    # fill in function body here
    #


# Exercise 8. (12 points)
#
# Use matplotlib to create a bar chart that indicates the total number of miles driven in each
# month (your chart should have twelve bars).  Export your plot to a pdf called
# "mustard_months.pdf".  Label each bar with the full name of the month.
#
def plot_monthly(rows):
    print("\nExercise 8:")
    all = {}
    for x in rows:
        month_name = x[0].month
        mileage = x[1]
        if all.get(month_name) == None:
            if mileage == '':
                all[month_name] = [0]
                continue
            all[month_name] = [mileage]
        else:
            if mileage == '':
                all.get(month_name).append(0)
                continue
            else:
                all.get(month_name).append(mileage)
    ans = []
    label_month = []
    amount = []
    for key in sorted(all.keys()):
        label_month.append((date(1900, key, 1).strftime('%B')))
        amount.append(sum(all.get(key)) / 1000000)
        ans.append((date(1900, key, 1).strftime('%B'), sum(all.get(key))))
    y_pos = np.arange(len(label_month))
    plt.bar(y_pos, amount, align='center', alpha=0.5)
    plt.xticks(y_pos, label_month)
    plt.xticks(rotation=90)
    plt.ylabel('MILEAGE (MILLION)')
    plt.xlabel('MONTHS')
    plt.title('MILEAGE PER MONTH')
    plt.tight_layout()
    plt.savefig('mustard_months.pdf')
    plt.close()
    return ans
    #
    # fill in function body here
    #


# Exercise 9. (12 points)
#
# Use matplotlib to create a line plot of the miles per gallon achieved (y-axis) over time
# (x-axis).  Export your plot to a pdf called "mustard_mpg_time.pdf".  Make sure you label
# the axes in your plot.
#
# Hint: you'll need to use the gallons and the mileage delta between successive entries to
# calculate miles per gallon.
#
def plot_mpg(rows):
    print("\nExercise 9:")
    dates = []
    values = []
    for x in rows:
        if (x[0] != date.min and x[1] != 0 and x[3] != 0):
            if (x[1] / x[3]) > 20000:
                print(x)
            dates.append(x[0])
            values.append(x[1] / x[3])
    plt.plot(dates, values)
    plt.ylabel('AVERAGE MILES PER GALLON (MPG)')
    plt.xlabel('TIME')
    plt.title('CHANGE OF MPG OVER TIME')
    plt.tight_layout()
    plt.savefig("mustard_mpg_time.pdf")
    plt.close()
    #
    # fill in function body here
    #


# Exercise 10. (12 points)
#
# Use the seaborn library (must be installed manually if you're not using Anaconda) to
# create a density plot of the number of days between refueling entries over the period
# captured in the data.  Export your plot to a pdf called "mustard_in_between_days.pdf".
# (Hat tip to Robert Smith.)
#
def plot_betweens(rows):
    print("\nExercise 10:")
    arr_days = []
    i = 1
    while i < len(rows):
        if rows[i][0] == date.min:
            arr_days.append((rows[i + 1][0] - rows[i - 1][0]).days)
            i += 2
            continue
        arr_days.append((rows[i][0] - rows[i - 1][0]).days)
        i += 1
    sns.set();
    sns.distplot(arr_days)
    plt.title('DENSITY PLOT OF THE NUMBER OF DAYS BETWEEN REFUELING ENTRIES')
    plt.tight_layout()
    plt.savefig('mustard_in_between_days.pdf')
    plt.close()
    # print(arr_days)
    #
    # fill in function body here
    #


#########################

if __name__ == '__main__':
    data_file_name = sys.argv[1]
    main(data_file_name)
    #plot_betweens(read_data())
    #plot_monthly(read_data())
    #plot_mpg(read_data())
