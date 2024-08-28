from sklearn.model_selection import StratifiedKFold
from scipy import signal
import pandas as pd
import numpy as np
import sys
import os
import matplotlib.pyplot as plt

REP_NUMBER=6
MIN_LENGTH=150

# resample the coverages to MIN_LENGTH
def resample(row):
    for rep in range(REP_NUMBER):
        # find the length of each part
        l_g1_o = len(row[f'gene_1_{rep}'])
        l_ig_o = len(row[f'intergenic_{rep}'])
        l_g2_o = len(row[f'gene_2_{rep}'])
        l_t_o = l_g1_o + l_ig_o + l_g2_o
        
        # find the length of the each part based on MIN_LENGTH, use 2 as min to avoid casting [a] to a.
        l_g1 = max(int((l_g1_o / l_t_o) * MIN_LENGTH), 2)
        l_g2 = max(int((l_g2_o / l_t_o) * MIN_LENGTH), 2)
        l_ig = max(int(MIN_LENGTH - l_g1 - l_g2), 2)
        l_t = l_g1 + l_ig + l_g2

        if not l_t == MIN_LENGTH:
            diff = l_t - MIN_LENGTH
            if l_g1 == max(l_g1, l_ig, l_g2):
                l_g1 -= diff
            elif l_g2 == max(l_g1, l_ig, l_g2):
                l_g2 -= diff
            else:
                l_ig -= diff

        # resample each part
        row[f'gene_1_{rep}'] = signal.resample(row[f'gene_1_{rep}'], l_g1)
        row[f'intergenic_{rep}'] = signal.resample(row[f'intergenic_{rep}'], l_ig)
        row[f'gene_2_{rep}'] = signal.resample(row[f'gene_2_{rep}'], l_g2)

    return row

def smooth(row):
    for rep in range(REP_NUMBER):
        for gene in ['gene_1', 'intergenic', 'gene_2']:
            row[f'{gene}_{rep}'] = signal.savgol_filter(row[f'{gene}_{rep}'], 4, 3, mode='nearest')
    return row

# scale the coverages to 0-1 (stable scale between g1-ig-g2)
def scale(row):
    for rep in range(REP_NUMBER):
        MAX = np.max([np.max(row[f'gene_1_{rep}']), np.max(row[f'gene_2_{rep}']), np.max(row[f'intergenic_{rep}'])])
        MIN = np.min([np.min(row[f'gene_1_{rep}']), np.min(row[f'gene_2_{rep}']), np.min(row[f'intergenic_{rep}'])])
        
        for gene in ['gene_1', 'intergenic', 'gene_2']:
            if MAX - MIN != 0:
                row[f'{gene}_{rep}'] = (row[f'{gene}_{rep}'] - MIN) / (MAX - MIN)
            else:
                row[f'{gene}_{rep}'] = row[f'{gene}_{rep}'] - MIN
                # print(len(row[f'{gene}_{rep}']), row['name_1'], row['name_2'], row['label'])
                pass
    return row

# make the coverages for g1, ig, g2 same length
def same_length(row):
    for rep in range(REP_NUMBER):
        l_g1 = len(row[f'gene_1_{rep}'])
        l_ig = len(row[f'intergenic_{rep}'])
        l_g2 = len(row[f'gene_2_{rep}'])

        row[f'gene_1_{rep}'] = np.concatenate([row[f'gene_1_{rep}'], np.zeros(l_ig), np.zeros(l_g2)])
        row[f'intergenic_{rep}'] = np.concatenate([np.zeros(l_g1), row[f'intergenic_{rep}'], np.zeros(l_g2)])
        row[f'gene_2_{rep}'] = np.concatenate([np.zeros(l_g1), np.zeros(l_ig), row[f'gene_2_{rep}']])
    return row

COL=3
ROW=2

def visulaize_data(row, folder):
    # create a folder to save the plots
    if not os.path.exists(folder):
        os.makedirs(folder)

    # X has 3 sequences for each gene pair, plot them in one figure and save it by name of genes 
    # features_columns = ['name_1', 'name_2', 'sequence', 'label']
    # third col in each row is the sequence that has 3 different lists

    colors = ['r', 'g', 'b']
    fig, ax = plt.subplots(ROW,COL, figsize=(15, 10))
    for rep in range(REP_NUMBER):
        r, c = rep // COL, rep % COL

        # plot the gene_1 coverage, intergenic coverage and gene_2 coverage in 3 different colors
        g1 = row[f'gene_1_{rep}']*100
        ig = row[f'intergenic_{rep}']*100
        g2 = row[f'gene_2_{rep}']*100


        ax[r][c].plot(g1, colors[0])
        ax[r][c].plot(ig, colors[1])
        ax[r][c].plot(g2, colors[2])

        # set the title of each plot
        ax[r][c].set_title('Sample ' + str(rep + 1))

        # set the x and y labels
        ax[r][c].set_xlabel('Position')
        ax[r][c].set_ylabel("Scaled Read count %")

    fig.suptitle('gene pairs=('+row.name_1 + ' , ' + row.name_2 + ')  label=' + str(row.label))
    fig.savefig(folder + '/' + row.name_1 + '-' + row.name_2 + '-label=' + str(row.label) + '.png')
    plt.close(fig)

def combine(row):
    combined = []
    for rep in range(REP_NUMBER):
        combined.append(np.array([row[f'gene_1_{rep}'], row[f'intergenic_{rep}'], row[f'gene_2_{rep}']]))

    combined = np.array(combined).transpose(2,0,1)
    return combined

def visulaize_combined_data(row, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
        
    fig, ax = plt.subplots(1, figsize=(5, 5))
    ax.imshow((row['combined']* 255).astype(np.uint8), extent=[0, REP_NUMBER*300, 0, MIN_LENGTH])
    ax.set_title('gene pairs=('+row.name_1 + ' , ' + row.name_2 + ')  label=' + str(row.label))
    ax.set_ylabel('Position')
    ax.set_xlabel('Samples')
    # set x label 1-6 for Samples, write in the middle of each Sample
    ax.set_xticks(np.arange(150, REP_NUMBER*300+150, 300))
    ax.set_xticklabels((np.arange(1,REP_NUMBER+1)))

    plt.savefig(folder + '/' + row.name_1 + '-' + row.name_2 + '-label=' + str(row.label) + '-combined.png')
    plt.close()

if __name__ == '__main__':

    # input files
    data_dir = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]

    input_path = data_dir + '/' + input_file
    output_path = data_dir + '/' + output_file

    fig_dir = data_dir + '/' + 'figures'
    if not os.path.exists(fig_dir):
        os.makedirs(fig_dir)

    VIS = False
    TEST = False
    if len(sys.argv) > 4:
        if sys.argv[4] == "TEST":
            TEST = True
        elif sys.argv[4] == "VIS":
            VIS = True 

    # read data
    data = pd.read_pickle(input_path)

    # resample the coverages to MIN_LENGTH
    data = data.apply(resample, axis=1)
    print('resample done')

    # scale the coverages to 0-1 (stable scale between g1-ig-g2)
    data = data.apply(scale, axis=1)
    print('scale done')

    # Smooth the signal
    data = data.apply(smooth, axis=1)
    print('smooth done')

    # make the coverages for g1, ig, g2 same length (Zero padding)
    data = data.apply(same_length, axis=1)
    print('same_length done')

    # make individual sample plot
    if VIS:
        data.apply(lambda row: visulaize_data(row, fig_dir+'/individual'), axis=1)
        # print('individual plot done')

    # combine the coverages
    data['combined'] = data.apply(lambda row: combine(row), axis=1)
    print('combine done')

    # final visualization of data
    if VIS:
        data.apply(lambda row: visulaize_combined_data(row, fig_dir+'/combined'), axis=1)
        # print('combined plot done')

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
        label_path = sys.argv[5]

        # save gene_pairs in a csv file
        txid = sys.argv[3].split('_')[-1].split('.')[0]
        gene_pairs = data[['name_1', 'name_2', 'label']]
        gene_pairs.to_csv(label_path, index=False)

        # remove the data with label 2 for testing
        data = data[data.label != 2].reset_index(drop=True)

        # save the data in np.savez_compressed
        np.savez_compressed(output_path, data=data)