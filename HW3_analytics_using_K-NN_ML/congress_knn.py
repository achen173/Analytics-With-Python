import sys
import csv
import random


TEST_SET_SIZE = 100
VERBOSE = True  # change this to eliminate debug output


def read_data(train_file, predict_col_name):
    """Read in the congressional voting data.

        Arguments:
            train_file -- path to the csv data
            predict_col_name -- the name of the column that will be considered the class label

        Returns:
            name__votes -- dictionary that maps rep name to a list of votes
            name__class -- dictionary that maps rep name to a class label
    """
    name__votes = {}
    name__class = {}
    with open(train_file, encoding="utf8") as infile:
        reader = csv.reader(infile)
        col_names = next(reader)  # header row
        class_col_idx = col_names.index(predict_col_name)
        for row in reader:  # Name, State, District, Party, Vote1, Vote2, ...
            name = row[0]
            class_val = row[class_col_idx]
            row.pop(class_col_idx)
            name__votes[name] = row[4:]
            name__class[name] = class_val
    if VERBOSE:
        print("read", len(name__votes), "rows")
    return name__votes, name__class


def predict_votes(train_vote_lists, test_vote_lists, class_vals, k):
    """Predict the class value (vote) for a set of representatives.

        Arguments:
            train_vote_lists -- dictionary mapping rep name to vote list for the training data
            test_vote_lists -- dictionary mapping rep name to vote list for the test instances
            class_vals -- dictionary mapping rep name to class value
            k -- the number of nearest neighbors to consider

        Returns:
            accuracy of the predictions
    """
    correct_count = 0
    for test_name, test_votes in test_vote_lists.items():
        if VERBOSE:
            print("predicting vote for ", test_name)
        predict_class = predict(train_vote_lists, test_votes, class_vals, k)
        if VERBOSE:
            print("predicted value:", predict_class, "------  actual value:", class_vals[test_name])
            if(predict_class != class_vals[test_name]):
                print("problem ")
        if predict_class == class_vals[test_name]:
            correct_count += 1
    accuracy = correct_count / len(test_vote_lists)
    if VERBOSE:
        print("correct {}/{} = {:.2f}".format(correct_count, len(test_vote_lists), accuracy))
    return accuracy


def predict(train_dict, test_row, class_dict, k):
    """Predict the class value of a single instance.

        Arguments:
            train_dict -- dictionary mapping a key value (rep name) to attribute values (votes)   {Rep: (Votes...........)}
            test_row -- a list of attribute values (votes) for a single test instance             
            class_dict -- dictionary mapping keys (rep name) to class value                       {Rep1: Vote, Rep2: Vote2, ....}
            k -- the number of nearest neighbors to consider
        Returns:
            predicted class
    """
    #
    # Fill in the function body
    #
    return class_dict.get(knn(train_dict, test_row, k)[0])


def knn(train_dict, test_row, k):
    """Generate a list of neighbor instances for a given example.

        Arguments:
            train_dict -- dictionary mapping a key value (rep name string) to attribute values (votes)
            test_row -- a list of attribute values (votes) for a single test instance
            k -- the number of nearest neighbors to consider

        Returns:
            a list containing the key value strings (rep names) of the k nearest neighbors
    """
    distances = list()
    for rowName in train_dict:    # iterate through keys
        dist = distance(test_row, train_dict.get(rowName))
        distances.append((rowName, dist))
        # if(rowName == 'James “Jim” McGovern'):
        #     print("\n\nI messed up\n\n", rowName)
    distances.sort(key=lambda tup: tup[1])
    neighbors = list()
    for i in range(k):
         neighbors.append(distances[i][0])
    return neighbors  # Fix this!


def distance(row1, row2):
    """Calculate the distance between two lists of attributes.

        Arguments:
            row1 -- list of attribute values
            row1 -- list of attribute values

        Returns:
            distance in attribute space between row1 and row2
    """
    i= 0
    j = len(row1)
    while i < len(row1):
        if(row1[i] == row2[i]):
            j = j - 1
        i += 1
    return j  # Fix this!


###################################

if __name__ == '__main__':

    # grab some parameters from the command line, and show help if they're not all there
    if len(sys.argv) <= 3:
        sys.exit("USAGE: " + sys.argv[0] + " path/to/congress_data.csv predict_col_name k")
    train_file_path = sys.argv[1]
    predict_col = sys.argv[2]
    k = int(sys.argv[3])
    # train_file_path = 'congress_data.csv'
    # predict_col = 'Vote119'
    # k = 150

    # read in the data file
    votes, class_vals = read_data(train_file_path, predict_col)

    # randomly split the data into training and test sets, putting into dictionaries keyed by name
    all_names = list(votes.keys())
    random.shuffle(all_names)
    train_names = all_names[:-TEST_SET_SIZE]
    test_names = all_names[-TEST_SET_SIZE:]
    train_vote_lists = {name: votes[name] for name in train_names}
    test_vote_lists = {name: votes[name] for name in test_names}

    # run the classifier and print the accuracy
    acc = predict_votes(train_vote_lists, test_vote_lists, class_vals, k)
    print(acc)
