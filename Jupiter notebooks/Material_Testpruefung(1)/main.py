# Task 1: Read the data from data.csv

# Hint: This one we already solved for you ;)
import pandas as pd
import numpy as np

df = pd.read_csv("data.csv")

X = df.drop(['target'], axis=1)
y = df['target']

# Task 2: Split data into training and testing.

from sklearn.model_selection import train_test_split

# Hint: this function takes as parameter X, y, and a 'test_size' ;)
X_train, X_test, y_train, y_test = None, None, None, None

# Task 3: Train a model on your data.

# Hint 1: Below are some options for models ;)
# Hint 2: To train a model, use the method 'fit' with some X and some y.
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier

model = None

# Task 4: Measure the quality of your estimator in the test data.

from sklearn.metrics import accuracy_score

# Hint: Here you use your estimator to 'predict' the labels for your
# test data.
y_pred = None

# Hint: Call accuracy_score with the following arguments:
# 1. the true labels.
# 2. the labels you predicted.
acc = 0.

print("Accuracy of classif. tree on test data: {:.3f}".format(acc))

# Task 5: Use your estimator to make predictions for the examples in X_final.csv

X_final = pd.read_csv("X_final.csv")
y_final = None
print(y_final)
