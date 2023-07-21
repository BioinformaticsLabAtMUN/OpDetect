from sklearn.model_selection import KFold, train_test_split, StratifiedKFold
from scipy import signal
import pandas as pd
import numpy as np
import sys
import os
import pickle

REP_NUMBER=6
MIN_LENGTH=150

# resample the coverages to MIN_LENGTH
def resample(row):
    for rep in range(REP_NUMBER):
        # find the length of each part
        l_g1_o = len(row[f'gene_1_{rep}'])
        l_ig_o = len(row[f'intergenic_{rep}'])
        l_g2_o = len(row[f'gene_2_{rep}'])
        
        # find the length of the longest part based on MIN_LENGTH
        l_g1 = max(int((l_g1_o / (l_g1_o + l_ig_o + l_g2_o)) * MIN_LENGTH),1)
        l_g2 = max(int((l_g2_o / (l_g1_o + l_ig_o + l_g2_o)) * MIN_LENGTH),1)
        l_ig = int(MIN_LENGTH - l_g1 - l_g2)

        # resample each part
        row[f'gene_1_{rep}'] = signal.resample(row[f'gene_1_{rep}'], l_g1)
        row[f'intergenic_{rep}'] = signal.resample(row[f'intergenic_{rep}'], l_ig)
        row[f'gene_2_{rep}'] = signal.resample(row[f'gene_2_{rep}'], l_g2)

    return row

# smooth the coverages
def smooth(row):
    for rep in range(REP_NUMBER):
        row[f'gene_1_{rep}'] = signal.savgol_filter(row[f'gene_1_{rep}'], 4, 3, mode='nearest')
        row[f'intergenic_{rep}'] = signal.savgol_filter(row[f'intergenic_{rep}'], 4, 3, mode='nearest')
        row[f'gene_2_{rep}'] = signal.savgol_filter(row[f'gene_2_{rep}'], 4, 3, mode='nearest')
    return row

# scale the coverages to 0-255 it could be negatice number
def scale(row):
    for rep in range(REP_NUMBER):
        row[f'gene_1_{rep}'] = (row[f'gene_1_{rep}'] - np.min(row[f'gene_1_{rep}'])) / (np.max(row[f'gene_1_{rep}']) - np.min(row[f'gene_1_{rep}']) + 1) * 255
        row[f'intergenic_{rep}'] = (row[f'intergenic_{rep}'] - np.min(row[f'intergenic_{rep}'])) / (np.max(row[f'intergenic_{rep}']) - np.min(row[f'intergenic_{rep}'])+1) * 255
        row[f'gene_2_{rep}'] = (row[f'gene_2_{rep}'] - np.min(row[f'gene_2_{rep}'])) / (np.max(row[f'gene_2_{rep}']) - np.min(row[f'gene_2_{rep}'])+1) * 255
    return row

# make the coverages for g1, ig, g2 same length
def same_length(row):
    for rep in range(REP_NUMBER):
        l_g1 = len(row[f'gene_1_{rep}'])
        l_ig = len(row[f'intergenic_{rep}'])
        l_g2 = len(row[f'gene_2_{rep}'])
        l_t = l_g1 + l_ig + l_g2
        
        row[f'gene_1_{rep}'] = np.concatenate([row[f'gene_1_{rep}'], np.zeros(l_ig), np.zeros(l_g2)])
        row[f'intergenic_{rep}'] = np.concatenate([np.zeros(l_g1), row[f'intergenic_{rep}'], np.zeros(l_g2)])
        row[f'gene_2_{rep}'] = np.concatenate([np.zeros(l_g1), np.zeros(l_ig), row[f'gene_2_{rep}']])
    return row

def combine(row):
    combined = []
    for rep in range(REP_NUMBER):
        combined.append(np.array([row[f'gene_1_{rep}'], row[f'intergenic_{rep}'], row[f'gene_2_{rep}']]))

    combined = np.array(combined).transpose(2,0,1)
    return combined

if __name__ == '__main__':

    # input files
    directory = sys.argv[1]
    input_path = directory + '/' + sys.argv[2]

    file_name = sys.argv[3]
    output_path = directory + '/' + file_name + '.npz'
    test_path = directory + '/' + file_name + '_test.npz'
    vis_path = directory + '/' + file_name + '_vis.pkl'

    TEST = False
    if len(sys.argv) == 5:
        TEST = True

    # read data
    data = pd.read_pickle(input_path)

    # resample the coverages to MIN_LENGTH
    data = data.apply(resample, axis=1)

    # smooth the coverages
    # data = data.apply(smooth, axis=1)

    # scale the coverages to 0-255
    data = data.apply(scale, axis=1)

    # make the coverages for g1, ig, g2 same length
    data = data.apply(same_length, axis=1)

    # save data in a pkl file
    # data.to_pickle(vis_path)

    # combine the coverages
    data['combined'] = data.apply(lambda row: combine(row), axis=1)

    # just keep the combined coverage and label and name_1, name_2
    data = data[['name_1', 'name_2', 'combined', 'label']]

    if not TEST:

        # Remove the data with label 2 from the training data
        # use data with label 0 and 1 for training
        data = data[data.label != 2].reset_index(drop=True)
 
        # stratified split
        skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
        folds_index = np.array(list(skf.split(data, data.label)), dtype=object)

        # save the data in np.savez_compressed
        np.savez_compressed(output_path, data=data, folds_index=folds_index)

        print('data.shape', data.shape)

    else:
        # save the data in np.savez_compressed
        np.savez_compressed(output_path, data=data)

        # save gene_pairs in a csv file
        txid = sys.argv[3].split('_')[-1].split('.')[0]
        gene_pairs = data[['name_1', 'name_2', 'label']]
        gene_pairs.to_csv(directory + '/' + txid + '/gene_pairs.csv', index=False)

        # remove the data with label 2 for testing
        data = data[data.label != 2].reset_index(drop=True)

        # save the data in np.savez_compressed
        np.savez_compressed(test_path, data=data)