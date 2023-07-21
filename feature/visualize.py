from sklearn.model_selection import KFold, train_test_split, StratifiedKFold
from scipy import signal
import pandas as pd
import numpy as np
import sys
import functools as ft
import os
import matplotlib.pyplot as plt

REP_NUMBER=6
ROW=2
COL=3
MIN_LENGTH=150

def combine(row):
    combined = []
    for rep in range(REP_NUMBER):
        combined.append(np.array([row[f'gene_1_{rep}'], row[f'intergenic_{rep}'], row[f'gene_2_{rep}']]))

    combined = np.array(combined).transpose(2,0,1)
    return combined

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
        g1 = row[f'gene_1_{rep}']
        ig = row[f'intergenic_{rep}']
        g2 = row[f'gene_2_{rep}']


        ax[r][c].plot(g1, colors[0])
        ax[r][c].plot(ig, colors[1])
        ax[r][c].plot(g2, colors[2])

        # set the title of each plot
        ax[r][c].set_title('Sample ' + str(rep + 1))

        # set the x and y limits
        # ax[r][c].set_xlim([0.001, 255])
        # ax[r][c].set_ylim([0.01, 255])

        # set the x and y labels
        ax[r][c].set_xlabel('Position')
        ax[r][c].set_ylabel('Read count')

    fig.suptitle('gene pairs=('+row.name_1 + ' , ' + row.name_2 + ')  label=' + str(row.label))
    fig.savefig(folder + '/' + row.name_1 + '-' + row.name_2 + '-label=' + str(row.label) + '.png')
    plt.close(fig)
    print("done")

# func to visualize the combined data for each gene pair size=(150,6,3)
def visulaize_combined_data(row, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
        
    fig, ax = plt.subplots(1, figsize=(9, 4))
    ax.imshow(row['combined'].transpose(1,0,2), extent=[0, 150, 0, 60])
    ax.set_title('gene pairs=('+row.name_1 + ' , ' + row.name_2 + ')  label=' + str(row.label))
    ax.set_xlabel('Position')
    ax.set_ylabel('Samples')
    # set y label 1-6 for Samples, write in the middle of each Sample
    ax.set_yticks(np.arange(5, 65, 5))
    ax.set_yticklabels([6 , 5.5, 5 , 4.5, 4 , 3.5, 3 , 2.5, 2 , 1.5, 1 , 0.5])
    # for i, tick in enumerate(ax.yaxis.get_major_ticks()):
    #     if i % 2 == 1:
    #         tick.set_visible(False)
    # for over y labels and set the color of each label
    for i,label in enumerate(ax.yaxis.get_ticklabels()):
        if i % 2 == 1:
            label.set_visible(False)
        else:
            #remove tick lines
            label.set_visible(True)
            ax.yaxis.get_ticklines()[i*2].set_visible(False)
    
    ax.set_xticks(np.arange(0, 175, 25))
    ax.set_xticklabels(np.arange(0, 175, 25))


    plt.savefig(folder + '/' + row.name_1 + '-' + row.name_2 + '-label=' + str(row.label) + '-combined.png')
    plt.close()

if __name__ == '__main__':
    
    # input files
    directory = sys.argv[1]
    input_path = directory + '/' + sys.argv[2]

    # read data
    data = pd.read_pickle(input_path)
    folder = str(directory + '/plots')


    data.apply(lambda row: visulaize_data(row, folder), axis=1)

    data['combined'] = data.apply(lambda row: combine(row), axis=1)
    data.apply(lambda row: visulaize_combined_data(row, folder), axis=1)