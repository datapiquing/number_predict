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
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
import pickle

def preprocess_training_dataset(filename):
    """Load training dataset and extract feature set and target labels"""

    df_dataset = pd.read_csv(f'./clean_data/{filename}')

    # Extract the feature data as X
    X = df_dataset.drop(labels='target', axis=1)

    # Extract the target label column as y
    y = df_dataset['target']

    return X, y


def train_knn_model(X, y, model_filename):
    """Split the dataset, fit the model to the training data and save the model"""

    # Split the data into training (70%) and test (30%), set the random generator seed and mix the rows
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=21, stratify=y)

    # Initialise the classifier, passing in the expected number of unique targets
    knn = KNeighborsClassifier(n_neighbors=10)

    # Fit the model to the training data
    knn.fit(X_train, y_train)

    # ## Save the ML Model
    # Serialise and save the model to disk
    pickle.dump(knn, open(f'./ml_model/{model_filename}', 'wb'))

    return X_train, X_test, y_train, y_test, knn


def predict_results_and_calculate_accuracys(X_test, knn_model):
    """Predict the target labels of the test data and calculate their accuracy"""    

    # Predict the target value of each test data row
    y_pred = knn_model.predict(X_test)

    # Calculate the accuracy of the model on the test data
    accuracy = knn_model.score(X_test, y_test)

    return y_pred, accuracy


def plot_model_complexity_curve(X_train, X_test, y_train, y_test, knn_model, neighbours):
    """Plot the accuracy of the model for different values of kNN neighbors"""

    # Setup arrays to store train and test accuracies
    n = np.arange(1,neighbours)
    train_accuracy = np.empty(len(n))
    test_accuracy = np.empty(len(n))

    # Loop over different values of k
    for i, k in enumerate(n):
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
    plt.plot(n, test_accuracy, label = 'Testing Accuracy')
    plt.plot(n, train_accuracy, label = 'Training Accuracy')
    plt.legend()
    plt.xlabel('Number of Neighbors')
    plt.ylabel('Accuracy')
    plt.show()


if __name__ == "__main__":

    dataset_filename = 'training_dataset.csv'
    X, y = preprocess_training_dataset(dataset_filename)

    model_filename = 'number_reflectivity_knn_model'
    X_train, X_test, y_train, y_test, kNN_model = train_knn_model(X, y, model_filename)

    y_pred, accuracy = predict_results_and_calculate_accuracys(X_test, kNN_model)

    print(f"Test set predictions: {y_pred}")

    print(f"Accuracy of predictions: {accuracy}")

    kNN_neighbors = 12
    plot_model_complexity_curve(X_train, X_test, y_train, y_test, kNN_model, kNN_neighbors)

    print(confusion_matrix(y_test, y_pred))

    # ## Classification Report
    print(classification_report(y_test, y_pred))


# From the top left of the matrix (for numbers 0 to 9), the vertical rows represent actual values and the horizontal 
# columns represent predicted values. There are no instances were the actual and predicted values are different.
# Hence, the diagional represents a count of all rows where the actual and predicted values are the same. 
# Therefore, in this case, the predicted results are 100% accurate






