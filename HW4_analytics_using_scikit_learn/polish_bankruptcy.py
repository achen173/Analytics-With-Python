#!/usr/bin/python
import sys
import numpy as np
import pandas as pd
from sklearn import impute
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.model_selection import KFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn import datasets, linear_model
# from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_score
# Each of the steps defined in the main() function calls one or more of the functions stubbed out
# below.  Fill in the function bodies below, paying attention to how they are called and what kinds
# of values are returned.  Wherever possible, you should use tools from the scikit-learn codebase
# to accomplish each task; note that you'll have to include relevant import statements.
#
def main(file_name):
    #
    # 0. Read in the data.  Store the attributes in a pandas DataFrame called x, and class values
    #    (last column) in a Series object called y.

    x, y = read_data(file_name)

    #
    # 1. Handle missing values in the data using an sklearn SimpleImputer.  The transformed
    #    data should be stored in a numpy array x_imp.
    x_imp = impute_data(x)

    #
    # 2. Split the imputed data into training and test sets, where 75% of the data is used for
    # training
    x_train, x_test, y_train, y_test = train_test_split(x_imp, y)

    # 3. Print out the class distributions for both training and test
    train_pos_count, train_neg_count = get_class_distrib(y_train)
    test_pos_count, test_neg_count = get_class_distrib(y_test)
    print("training class distrib: {:.2f}, {:.2f}".format(train_pos_count/len(y_train),
                                                          train_neg_count/len(y_train)))
    print("test class distrib: {:.2f}, {:.2f}".format(test_pos_count/len(y_test),
                                                      test_neg_count/len(y_test)))

    #
    # 4. Learn a decision tree model and get its accuracy on both the training and test data
    tree_clf = learn_tree(x_train, y_train)
    acc_train = test_model(tree_clf, x_train, y_train)
    acc_test = test_model(tree_clf, x_test, y_test)
    print("decision tree training acc: {:.4f}, test acc: {:.4f}".format(acc_train, acc_test))

    #
    # 5. Print out the names of the top five most important features in the tree from 4.  You can
    #    access them through the feature_importances_ data member of the classifier object.
    for feat, score in top_features(tree_clf, x.columns, 5):
        print("{} ({:.4f})".format(feat, score))

    #
    # 6. Repeat exercise 4, this time using a scikit-learn k-NN classifier that uses
    #    a Euclidean distance metric.  Print the test set accuracy obtained from using several
    #    values of k.  What is the best value of k?
    k_vals = [1, 3, 5, 7, 9, 19, 39, 79, 159, 319]
    for k in k_vals:
        knn_clf = learn_knn(x_train, y_train, k)
        acc_test = test_model(knn_clf, x_test, y_test)
        print("k-nn {} test acc: {:.4f}".format(k, acc_test))

    #
    # 7. Repeat exercise 6, but this time scale the data first using the scikit-learn
    #    StandardScaler to preprocess the data.  Use the make_pipeline function() to create a
    #    pipeline.
    for k in k_vals:
        knn_clf_std = learn_knn_standard(x_train, y_train, k)
        acc_test = test_model(knn_clf_std, x_test, y_test)
        print("k-nn {} (standardized) test acc: {:.4f}".format(k, acc_test))

    #
    # 8. Now repeat the classification process from exercise 4, using 10-fold cross-validation
    #    instead of the single training/test split.
    acc_test = crossval_tree(x_imp, y, 10)
    print("decision tree {}-fold cross-validation acc: {:.4f}".format(10, acc_test))


#
# Fill in the function bodies for each of the functions below.  The purpose of each is described
# in the main() function above.  The types of the return values can be found in the comments
# below.  Note that each has been initialized to None to enable incremental development of the code.
#

def read_data(file_name):
    #  Read in the data.  Store the attributes in a pandas DataFrame called x, and class values
    #  (last column) in a Series object called y.
    x = pd.read_csv(file_name)
    newX = x.drop(['class'], axis=1)
    y = x.iloc[:,-1]
    return newX, y  # x is a DataFrame, y is a Series


def impute_data(x):
    # 1. Handle missing values in the data using an sklearn SimpleImputer.  The transformed
    #    data should be stored in a numpy array x_imp.
    x_imp = impute.SimpleImputer(missing_values=np.nan, strategy='constant', fill_value=0)
    ans = x_imp.fit_transform(x)
    return ans  # x is a numpy.array


def get_class_distrib(class_labels):
    neg, pos = class_labels.value_counts() # 0 -> neg, 1->pos
    return pos, neg  # pos and neg are integer counts

def learn_tree(x, y):
    # 4. Learn a decision tree model and get its accuracy on both the training and test data
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(x, y)
    return clf  # clf is a tree classifier object


def test_model(clf, x, y):
    myans = clf.predict(x)
    theiry = y.to_numpy()
    if len(myans) == len(theiry):
        acc = np.sum(myans == theiry)
    else:
        print("Invalid Comparision")
    return acc/len(myans)  # acc is a float


def top_features(clf, col_names, num):
    mylist = [];
    for x,y in zip(col_names, clf.feature_importances_):
        mylist.append((x,y))
    sortedlist = sorted(mylist, key=lambda x: x[1])
    return sortedlist[len(sortedlist)-num:]  # feat_scores is a list of (feature name, float) tuples


def learn_knn(x, y, k):
    clf = KNeighborsClassifier(n_neighbors=k)
    clf.fit(x, y)
    return clf  # clf is a knn classifier object


def learn_knn_standard(x, y, k):
    stdScaler = StandardScaler()
    clf = KNeighborsClassifier(n_neighbors=k)
    model = Pipeline([('sel', stdScaler), ('clf', clf)])
    pipeline = model.fit(x, y)
    return pipeline  # clf is a pipeline object

    # train_pos_count, train_neg_count = get_class_distrib(y_train)
    # test_pos_count, test_neg_count = get_class_distrib(y_test)
    # print("training class distrib: {:.2f}, {:.2f}".format(train_pos_count/len(y_train),
    #                                                       train_neg_count/len(y_train)))
    # print("test class distrib: {:.2f}, {:.2f}".format(test_pos_count/len(y_test),
    #                                                   test_neg_count/len(y_test)))
    #
    # #
    # # 4. Learn a decision tree model and get its accuracy on both the training and test data
    # tree_clf = learn_tree(x_train, y_train)
    # acc_train = test_model(tree_clf, x_train, y_train)
    # acc_test = test_model(tree_clf, x_test, y_test)
    # print("decision tree training acc: {:.4f}, test acc: {:.4f}".format(acc_train, acc_test))

def crossval_tree(x, y, folds):
    # 8. Now repeat the classification process from exercise 4, using 10-fold cross-validation
    #    instead of the single training/test split.
    # 4. Learn a decision tree model and get its accuracy on both the training and test data
    # tree_clf = learn_tree(x_train, y_train)
    # acc_train = test_model(tree_clf, x_train, y_train)
    # acc_test = test_model(tree_clf, x_test, y_test)
    # print("decision tree training acc: {:.4f}, test acc: {:.4f}".format(acc_train, acc_test))

    # kf = KFold(n_splits=folds)  # Define the split - into 2 folds
    # for train, test in kf.split(y):
    #     print("TRAIN:", train, "TEST:", test)
    # test = 0
    lasso = linear_model.Lasso()
    y_pred = cross_val_score(lasso, x, y, cv=folds)
    acc = [x for x in y_pred if x >0]
    return len(acc)/len(y_pred) # acc is a float


#########################

if __name__ == '__main__':
    # data_file_name = sys.argv[1]
    data_file_name = 'polish_bankruptcy_data.csv'
    main(data_file_name)







