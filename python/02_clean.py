#! python3

# coding: utf-8

# Date: 2021-02-17
# Author: GS
# Title: EV3 Character Recognition Experiment - Clean
# Description: 
#   Clean the raw data files, restructure feature and target labels ready for machine learning
#   and concatenate them into a single file used for training
# Version 
#   [1.0] 2021-02-17 Initial

import numpy as np
import pandas as pd
import subprocess

def create_rotation_dict():
    '''Initialise a dictionary with keys of 0 to 360 at 10 degree intervals, each with value zero'''
    degree_bins = list(range(0,361,10))
    rotation_dict = {}
    for bin in degree_bins:
        rotation_dict[bin] = 0
    return rotation_dict

# A function to place rotation values into buckets of 10 degrees (+ or - 5 degrees either side)
# These will be the feature columns of each sample rotation

def rotation_buckets(degrees):
    '''Calculate which 360 degree bucket (width=10) the rotation belongs'''
    if degrees > 360 and degrees%360 < 5:
        degrees = (degrees - 5)%360
    else:
        degrees = degrees%360
    modulus = degrees%10
    if modulus < 5:
        bucket = degrees - modulus
    else:
        bucket = (degrees - modulus) + 10
    return bucket


def create_clean_dataframe(filename):
    '''Read in raw data file and return clean DataFrame with target column'''

    target_value = int(filename[5:6])
    
    df_raw_data = pd.read_csv(f'./raw_data/{filename}')
    
    # Remove the space that prefixes the 'reflectivity' column name
    df_raw_data.columns = ['angle', 'reflectivity']
    
    # The experiment was 1 run of X x 360 degree rotations
    # Put actual rotation angle into buckets of 10 degrees between 0 and 360 degrees
    # Concatenate each run of X rotations vertically as tuples of (bucket_degrees, reflectivity_percentage)

    results_list = []
    rotation_column = 'angle'
    reflectivity_column = 'reflectivity'
    for index, row in df_raw_data.iterrows():
        prev_bucket_degrees = -1
        actual_degrees = row[rotation_column]
        bucket_degrees = rotation_buckets(actual_degrees)
        relectivity_percentage = row[reflectivity_column]
        #print(actual_degrees, bucket_degrees, relectivity_percentage)
        results_list.append((bucket_degrees, relectivity_percentage))
        
    # Convert the list of result tuples (rotation angle, refelctivity) to a dictionary of dictionaries where
    # the key is the run number and the value is a dictionary of rotation angles (from 0 to 360 degrees at 
    # 10 degree intervals) and their respective reflectivity value

    run = 0
    results = {}
    dict = create_rotation_dict()
    at_360 = False
    for tuple in results_list:
        if tuple[0] < 360 or at_360 == False:
            dict[tuple[0]] = tuple[1]    
            if tuple[0] >= 360:
                results[run] = dict
                run += 1
                dict = create_rotation_dict()

        at_360 = (tuple[0] >= 360) 
        
    # Create a DataFrame from the angle vs reflectivity results

    df_results = pd.DataFrame.from_dict(results)
    
    # Transpose the DataFrame so each rotation sample is a row and each 10 degree angle of rotation 
    # between 0 and 360 degrees is a feature column

    df_results = df_results.transpose()
    
    # Impute and zero values
    # For angles 0 - 10 degrees use the value of 360 degrees

    df_results[0] = np.where(df_results[0] == 0, df_results[360], df_results[0])
    
    # Where a cell value is zero convert to NaN

    df_results[df_results.eq(0)] = np.nan
    
    # Replace NaN values with the column mean

    df_results.fillna(df_results.mean().astype(int), inplace=True)
    df_results = df_results.astype(int)
        
    # Create a target column with the value of the number scanned
    df_results['target'] = target_value
    
    # Export the number DataFrame to a .csv file
    df_results.to_csv(f'./clean_data/{filename}', index=False)
    
    return df_results


def combine_cleaned_dataframes(filename_list):
    ''''''

    df_clean_results = pd.DataFrame()

    for filename in all_filenames:
        df = create_clean_dataframe(filename)
        df_clean_results = pd.concat([df_clean_results, df], ignore_index=True) 

    # Export the number DataFrame to a .csv file
    df_clean_results.to_csv(f'./clean_data/training_dataset.csv', index=False)
    
    return df_clean_results


if __name__ == "__main__":

    # Get a list of all raw data files collected
    filename = 'train'
    all_filenames = subprocess.call(['sh', 'ls raw_data/ | grep -e $filename'])

    dataset = combine_cleaned_dataframes(all_filenames)
    dataset


