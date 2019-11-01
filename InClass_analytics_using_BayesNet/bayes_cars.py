import pandas as pd


# Read the data file into a DataFrame using pd.read_csv()
df_all = pd.read_csv('mtcars.csv', dtype={'vs': str, 'am': str, 'gear': str, 'carb': str})


# Split the data set into training and test sets
df_train = df_all.sample(frac=0.8, random_state=None)  # set random_state to a number to repeat split
df_test = df_all.drop(df_train.index)


# We want to calculate P(cyl | vs, am, gear, carb) for each possible value of cyl.  Using Bayes rule, we have:
#
# P(cyl | vs, am, gear, carb) = P(vs, am, gear, carb | cyl) * P(cyl) / P(vs, am, gear, carb)
#
# Since we're using a "naive" Bayes classifer, we'll make a conditional independence assumption about the
# attributes, allowing us to rewrite the above as:
# [ P(vs | cyl) * P(am | cyl) * P(gear | cyl) * P(carb | cyl) ] * P(cyl) / P(vs, am, gear, carb)
#
# For each test example, we'll need to calculate each of these terms above, and select the value of cyl that
# gives us the highest posterior probability.  Since we care more about the class label (the predicted value
# of cyl than the probability itself, we can ignore the last (denominator) term, since it will be the same
# for all classes.  Now we just need to calculate:
# [ P(vs | cyl) * P(am | cyl) * P(gear | cyl) * P(carb | cyl) ] * P(cyl)
#
# For the above, we need to calculate the probabilty of each attribute (vs, am, gear, carb) value conditioned
# on the class (cyl), as well as the marginal probability of the class).  We do this by counting values in the
# training set.
#

def prob(df, class_name, class_val):
    num = df[df[class_name] == class_val]
    if(len(df[class_name]) == 0):
        print("YOU DIVIDED BY ZERO!!!")
    return len(num) / len(df[class_name])
    """
    Calculate the marginal probability of a class value in a dataframe.

    Arguments:
        df -- DataFrame object containing training data
        class_name -- the name of the column containing the class value
        class_val -- the value for which we're calculating a marginal probability

    Returns:
         P(class_val)
    """


def cond_prob(df, attr_name, attr_val, class_name, class_val):
    den = df[df[class_name] == class_val]
    num = den[den[attr_name] == attr_val]
    return len(num) / len(den)
    """
    Calculate the conditional probability of an attribute value given class in a dataframe.
    
    Arguments:
        df -- DataFrame object containing training data
        attr_name -- the name of the column containing attribute values
        attr_val -- the attribute value for which we're calculating the conditional probability
        class_name -- the name of the column containing the class value
        class_val -- the class value with which we're calculating the conditional probability

    Returns:
         P(attr_val | class_val)
    """

# Iterate over the training set
labels = []
for index, row in df_test.iterrows():

    # Calculate a (non-normalized) probability value for each possible class and keep the highest
    best_p = -1.0
    best_label = None
    for class_value in sorted(df_train['cyl'].unique()):

        p_vs_cyl = cond_prob(df_train, 'vs', row['vs'], 'cyl', class_value)  # P(vs | cyl)
        #
        # Fill in the other terms in the posterior probability calculation and calculate P(class_value | attributes)
        #

        # p = 0.1884  # FIX THIS!
        p = prob(df_train, "cyl", class_value)
        if p > best_p:
            best_p = p
            best_label = class_value

    labels.append(best_label)

df_test['cyl_predicted'] = labels
df_test['correct'] = df_test.apply(lambda r: r['cyl'] == r['cyl_predicted'], axis=1)
print(df_test)

accuracy = len(df_test[df_test['cyl'] == df_test['cyl_predicted']]) / len(df_test)
print("accuracy: {:.4f}".format(accuracy))

