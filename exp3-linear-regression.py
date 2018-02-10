from random import seed
from random import randrange
from csv import reader
from math import sqrt
import argparse


# Load a CSV file


def load_csv(filename):
    dataset = list()
    with open(filename, 'r') as file:
        csv_reader = reader(file)
        for row in csv_reader:
            if not row:
                continue
            dataset.append(row)
    return dataset

# Convert string column to float


def str_column_to_float(dataset, column):
    for row in dataset:
        row[column] = float(row[column].strip())

# Split a dataset into a train and test set


def train_test_split(dataset, split):
    train = list()
    train_size = split * len(dataset)
    dataset_copy = list(dataset)
    while len(train) < train_size:
        index = randrange(len(dataset_copy))
        train.append(dataset_copy.pop(index))
    return train, dataset_copy

# Calculate root mean squared error


def rmse_metric(actual, predicted):
    sum_error = 0.0
    for i in range(len(actual)):
        prediction_error = predicted[i] - actual[i]
        sum_error += (prediction_error ** 2)
    mean_error = sum_error / float(len(actual))
    return sqrt(mean_error)

# Evaluate an algorithm using a train/test split


def evaluate_algorithm(dataset, algorithm, split, *args):
    train, test = train_test_split(dataset, split)
#    counter = 0
#    while counter <= 10:
#       print("Actual: %.2f \n")
    test_set = list()
    for row in test:
        row_copy = list(row)
        row_copy[-1] = None
        test_set.append(row_copy)
    predicted = algorithm(train, test_set, *args)
    actual = [row[-1] for row in test]
    print("Actual \t Predicted")
    for i in range(10):
        print("%.2f \t %.2f" % (actual[i], predicted[i]))
    rmse = rmse_metric(actual, predicted)
    return rmse

# Calculate the mean value of a list of numbers


def mean(values):
    return sum(values) / float(len(values))

# Calculate covariance between x and y


def covariance(x, mean_x, y, mean_y):
    covar = 0.0
    for i in range(len(x)):
        covar += (x[i] - mean_x) * (y[i] - mean_y)
    return covar

# Calculate the variance of a list of numbers


def variance(values, mean):
    return sum([(x - mean)**2 for x in values])

# Calculate coefficients


def coefficients(dataset):
    x = [row[0] for row in dataset]
    y = [row[1] for row in dataset]
    x_mean, y_mean = mean(x), mean(y)
    b1 = covariance(x, x_mean, y, y_mean) / variance(x, x_mean)
    b0 = y_mean - b1 * x_mean
    return [b0, b1]

# Simple linear regression algorithm


def simple_linear_regression(train, test):
    predictions = list()
    b0, b1 = coefficients(train)
    print('Coefficients after training: %.3f, %.3f' % (b0, b1))
#    counter = 0
    for row in test:
        yhat = b0 + b1 * row[0]
        predictions.append(yhat)
#        counter += 1
#        if counter <= 10:
#            print("%.2f \n" % (yhat))
    return predictions

# Simple linear regression on insurance dataset


seed(1)

# load and prepare data
parser = argparse.ArgumentParser(description='Linear Regression Example \
    for ML Lab DJSCE')
parser.add_argument('--filename', type=str,
                    help='Provide path to dataset')
parser.add_argument('--ttsplit', type=float,
                    help='Provide Train-Test Split Ratio')
args = parser.parse_args()
filename = args.filename
dataset = load_csv(filename)
for i in range(len(dataset[0])):
    str_column_to_float(dataset, i)
# evaluate algorithm
split = args.ttsplit
if split >= 1.0:
    print("Split must be between 0 and 1")
print("Train-Test Split : %.2f" % (split))
rmse = evaluate_algorithm(dataset, simple_linear_regression, split)
print('RMSE: %.3f' % (rmse))
