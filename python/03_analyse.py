#! python3

# coding: utf-8

# Date: 2021-02-17
# Author: GS
# Title: EV3 Character Recognition Experiment - Analyse
# Description: 
#   Perform EDA on training data and generate associated plot   
# Version 
#   [1.0] 2021-02-17 Initial

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
import os


def plot_dataset(filename, label=None):
    '''Load dataset and generate plots of all or individual target labels'''
    
    # Load dataset
    df_dataset = pd.read_csv(f'./clean_data/{filename}')
    labels = df_dataset['target'].unique()    
    
    if label is None:
        # Generate mean/median plots for all target labels in the dataset[*]
        rows = len(labels)
        plot_number = 0
        fig, axes = plt.subplots(nrows=rows, ncols=1, sharex=True, sharey=True, figsize = (15, 24))
        for l in labels:
            df = df_dataset[df_dataset['target'] == l]
            df = df.drop(labels='target', axis=1)
            df.transpose()
            df.mean().astype(int).plot(ax=axes[plot_number], label = f'mean #{l}')
            df.median().astype(int).plot(ax=axes[plot_number], label = f'median #{l}')
            axes[plot_number].legend(loc='upper right')
            if plot_number == 0:
                axes[plot_number].set_title(f'Angle vs Reflectivity (mean & median) for each target in the dataset')
            axes[plot_number].set_xlabel('Angle of rotation (degrees)')            
            #plt.xlabel('Angle of rotation (degrees)')
            if plot_number == 4:
                axes[plot_number].set_ylabel('Reflectivity (%)')
            #plt.ylabel('Reflectivity (%)')
            plt.subplots_adjust(wspace=0, hspace=0.4)
            plot_number += 1  
    elif label in labels:
        # Generate plots for a specific target label in the dataset
        fig, axes = plt.subplots(nrows=1, ncols=2, sharex=False, sharey=False, figsize = (15, 6))
        df = df_dataset[df_dataset['target'] == int(label)]
        X = df.drop(labels='target', axis=1)
        
        # Plot all rows of the specified target
        X.transpose().plot(ax=axes[0], legend=False)
        axes[0].legend(title="Rotation#", fontsize='small', fancybox=False)
        axes[0].set_title(f'Angle vs Reflectivity for each rotation of #{label}')
        axes[0].set_xlabel('Angle of rotation (degrees)')
        axes[0].set_ylabel(f'Reflectivity of #{label} (%)')

        # Plot mean and median feature values for the specified target
        X.mean().astype(int).plot(label = 'mean')
        X.median().astype(int).plot(label = 'median')
        axes[1].legend()
        axes[1].set_title(f'Angle vs Reflectivity (mean & median) of #{label}')
        axes[1].set_xlabel('Angle of rotation (degrees)')
        axes[1].set_ylabel(f'Reflectivity of #{label} (%)')
    else:
        print(f'The chosen label, {label}, is not a label in this dataset')   
        
    plt.show()

if __name__ == "__main__":

    # Surpress matplotlib warnings[*] 
    warnings.filterwarnings('ignore')

    directory = os.system('pwd')
    print(f'Working folder = {directory}')

    # Load dataset and extract feature set
    filename='training_dataset.csv'
    df_dataset = pd.read_csv(f'./clean_data/{filename}')

    # Extract target labels from dataset
    labels = df_dataset['target'].unique()

    # Extract features from dataset    
    X = df_dataset.drop(labels='target', axis=1)

    # Get the dimensions of the dataset
    print(f'Rows = {X.shape[0]}, Columns = {X.shape[1]}')

    print(f'Target labels in dataset = {labels}')

    # Get the total number of fows of each target label
    df_target_count = df_dataset.loc[:,['0', 'target']].groupby('target').count()
    df_target_count.columns = ['total']
    df_target_count

    # Dataset
    df_dataset.head()

    # Feature set
    X.head()

    X.info()

    # Generate plots for a specific target label
    plot_dataset(filename='training_dataset.csv', label=4)

    # Generate plots for all target labels
    plot_dataset(filename='training_dataset.csv')






