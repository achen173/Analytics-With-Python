import sys
from math import log2
import pandas as pd
import numpy as np
import math


def entropy(vals):
    """Calculate the entropy of a list of values"""
    #
    # FILL THIS IN
    #
    e = 0
    for v in set(vals):
        occurance = vals.count(v)
        e -= occurance*math.log(occurance)
    # e = 0.0  # FIX THIS!
    return e


def info_gain(attr_class_tuples):
    """Calculate the information gain from splitting a list of (attribute, class) tuples by attribute value.

    Arguments:
        attr_class_tuples -- a list of (attribute, class) tuples; e.g., [ ('sunny', 'yes'), ('cloudy', 'no'), ... ]

    Returns:
         The quantity of information gain from splitting the tuples into subsets by their attribute values, as
         measured by the change in entropy.
    """
    #
    # FILL THIS IN
    #
    parent_list = []
    [parent_list.append(x[1]) for x in attr_class_tuples]
    parent_entropy = entropy(parent_list)
    entropy_child_result = 0
    result = 0
    against_list = []
    entropy_child = []
    counter_appear = 0
    for x2 in attr_class_tuples:
        if x2[0] not in against_list:
            for test in attr_class_tuples:
                if test[0] == x2[0]:
                    entropy_child.append(test[1])
                    counter_appear += 1
            prob = counter_appear/len(attr_class_tuples)
            entropy_child_result = prob * entropy(entropy_child)
            against_list.append(x2[0])
        result += entropy_child_result
    return parent_entropy-result


def select_best_attr(df, class_col):
    best_attr = None
    best_ig = -sys.maxsize

    for attr_col in df.columns:
        if attr_col == class_col:
            continue

        if pd.api.types.is_numeric_dtype(df[attr_col]):
            s, ig = select_best_split(df, attr_col, class_col)
            attr_col = attr_col + "<={:.2f}".format(s)
        else:
            tuples = list(zip(df[attr_col], df[class_col]))
            ig = info_gain(tuples)
            print("info gain for {} is {:.4f}".format(attr_col, ig))

        if ig > best_ig:
            best_attr = attr_col
            best_ig = ig

    return best_attr, best_ig


def select_best_split(df, attr_col, class_col, num_splits=10):
    best_split = None
    best_ig = -sys.maxsize

    for s in np.linspace(df[attr_col].min(), df[attr_col].max(), num_splits):
        feature_vals = (df[attr_col] <= s)
        tuples = list(zip(feature_vals, df[class_col]))
        ig = info_gain(tuples)
        print("info gain for {} <= {:.2f} is {:.4f}".format(attr_col, s, ig))

        if ig > best_ig:
            best_split = s
            best_ig = ig

    return best_split, best_ig


#############################
if __name__ == '__main__':

    if len(sys.argv) <= 4:
      sys.exit("USAGE: " + sys.argv[0] + " path/to/data.csv id_column_name class_column_name")
    infile_path = sys.argv[1]   # anyone_for_tennis.csv
    id_col_name = sys.argv[2]   # Tennis
    class_col_name = sys.argv[3]    # Yes


    df_all = pd.read_csv(infile_path)
    df_all.drop(columns=id_col_name, inplace=True)

    best_col, ig = select_best_attr(df_all, class_col_name)
    print("best split is {} ({})".format(best_col, ig))





