#! python3

# coding: utf-8

# Date: 2021-02-17
# Author: GS
# Title: EV3 Character Recognition Experiment - Train
# Description: 
#   Train, save and analyse the supervised kNN model created using the dataset   
# Version 
#   [1.0] 2021-02-17 Initial

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df_dataset = pd.read_csv('./clean_data/training_dataset.csv')
df_dataset.head()

df_dataset.shape

# Extract the feature (column) names of the data
feature_names = df_dataset.columns.drop('target')
feature_names

# Extract the feature data as X
X = df_dataset.drop(labels='target', axis=1)
X

# Extract a list of all posible targets (i.e. numbers 0 to 9)
target_names = df_dataset['target'].unique() #list(range(0,10))
target_names

# Extract the target label column as y
y = df_dataset['target']
y

# ## Train the model
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import pickle

# Split the data into training (70%) and test (30%), set the random generator seed and mix the rows
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=21, stratify=y)

# Initialise the classifier, passing in the expected number of unique targets
knn = KNeighborsClassifier(n_neighbors=10)

# Fit the model to the training data
knn.fit(X_train, y_train)

# ## Save the ML Model
# Serialise and save the model to disk
pickle.dump(knn, open('./ml_model/number_reflectivity_knn_model', 'wb'))

# Predict the target value of each test data row
y_pred = knn.predict(X_test)

print(f"Test set predictions: {y_pred}")

# Calculate the accuracy of the model on the test data
knn.score(X_test, y_test)

# ## Model Complexity Curve
# Setup arrays to store train and test accuracies
neighbors = np.arange(1,12)
train_accuracy = np.empty(len(neighbors))
test_accuracy = np.empty(len(neighbors))

# Loop over different values of k
for i, k in enumerate(neighbors):
    # Setup a k-NN Classifier with k neighbors: knn
    knn = KNeighborsClassifier(k)
    
    # Fit the classifier to the training data
    knn.fit(X_train, y_train)
    
    # Compute accuracy on the training set
    train_accuracy[i] = knn.score(X_train, y_train)
    
    # Compute accuracy on the testing set
    test_accuracy[i] = knn.score(X_test, y_test)


# Generate plot
plt.title('k-NN: Varying Number of Neighbors')
plt.plot(neighbors, test_accuracy, label = 'Testing Accuracy')
plt.plot(neighbors, train_accuracy, label = 'Training Accuracy')
plt.legend()
plt.xlabel('Number of Neighbors')
plt.ylabel('Accuracy')
plt.show()


# Test and training accuracy are both 100% indicating the data is relatively simple and the 
# reflectivity signatures of each number well defined with little overlap

# ## Confusion Matrix
from sklearn.metrics import classification_report, confusion_matrix

# From the top left of the matrix (for numbers 0 to 9), the vertical rows represent actual values and the horizontal 
# columns represent predicted values. There are no instances were the actual and predicted values are different.
# Hence, the diagional represents a count of all rows where the actual and predicted values are the same. 
# Therefore, in this case, the predicted results are 100% accurate

print(confusion_matrix(y_test, y_pred))

# ## Classification Report
print(classification_report(y_test, y_pred))






