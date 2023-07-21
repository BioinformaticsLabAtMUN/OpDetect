import os
import numpy as np
import pandas as pd
from scipy.stats import friedmanchisquare, rankdata, norm, chi2
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
from Orange.evaluation import compute_CD, graph_ranks


# module load python
# source ../4_data_process/env/bin/activate

# Directory containing the model outputs (replace with your actual directory)
dir = "outputs"
models = ['om', 'rh', 'of', 'os', 'final_train', 'final']
model_names = ['Operon Mapper', 'Rockhopper', 'Operon Finder', 'OperonSEQer','Our Model', 'Our Model NE']
dataset_names = ['txid224308','txid196627','txid511145','txid85962','txid297246','txid169963','txid272634','txid298386']#,'txid6239'] #['txid176299','txid224326','txid224911','txid208964', 'txid214092',]

# Read the CSV files path = f'{dir}/{model}_{txid}.csv'

# Read the outputs into a numpy array, outputs.shape[0] is # Number of classifiers, outputs.shape[1] is # Number of datasets
outputs = []
for i, model in enumerate(models):
    group = []
    for j, txid in enumerate(dataset_names):
        path = f'{dir}/{model}_{txid}.csv'
        try:
            pred = pd.read_csv(path)
            pred = pred[pred.true != 2]
            pred = pred[pred.pred != 2]
            y_true = pred.true
            y_pred = pred.pred
            # calc auroc
            fpr, tpr, _ = roc_curve(y_true, y_pred)
            roc_auc = auc(fpr, tpr)
            group.append(roc_auc)
        except:
            if model == 'final_train':
                model = 'final'
                path = f'{dir}/{model}_{txid}.csv'
                pred = pd.read_csv(path)
                pred = pred[pred.true != 2]
                pred = pred[pred.pred != 2]
                y_true = pred.true
                y_pred = pred.pred
                # calc auroc
                fpr, tpr, _ = roc_curve(y_true, y_pred)
                roc_auc = auc(fpr, tpr)
                group.append(roc_auc)
            else:
                group.append(0)
                print(f'No prediction file for {model} on {txid}.')
    outputs.append(group)
        
outputs = np.array(outputs)

# Perform Friedman test to check for significant differences
f_stat, f_pval = friedmanchisquare(*outputs)
print(f'Friedman test statistic: {f_stat}')
# 8 digits after the decimal point
print(f'p-value: {f_pval:.8f}')

# Set the critical difference value based on the number of classifiers and datasets
num_classifiers = outputs.shape[0]
num_datasets = outputs.shape[1]
k = num_classifiers
N = num_datasets

# obtain ranks
ranks = rankdata(outputs, axis=0)
ranks = num_classifiers - ranks.astype(int) + 1 # highest to lowest
mean_ranks = np.mean(ranks, axis=1)

#generate a critical difference diagram with Nemenyi post-hoc, default alpha=0.05
cd = compute_CD(mean_ranks, num_datasets) #tested on 7 datasets
print(f'Critical difference: {cd:.3f}')
graph_ranks(mean_ranks, model_names, cd=cd, width=6, reverse=True, textspace=1.5)
plt.savefig('critical_difference.png', dpi=300)

# The dot represents the mean rank and bars represent standard error. Lower ranks indicate better performance, horizontal

fig, ax = plt.subplots(figsize=(6, 3))
# different color
colors = ['tab:green', 'tab:red', 'tab:brown', 'tab:purple', 'tab:orange', 'tab:blue']
for i in range(num_classifiers):
    # horizontal plots
    # xerr represents sandart error
    std = np.std(outputs[i]*100)
    mean_roc = np.mean(outputs[i]*100)
    print(f'{model_names[i]}: {mean_roc:.2f} ± {std:.2f}')
    ax.errorbar(mean_roc, i, xerr=std, fmt='o', color=colors[i], capsize=5, label=model_names[i], markersize=3, elinewidth=0.5)


ax.set_yticks(np.arange(num_classifiers))
ax.set_yticklabels(model_names)
ax.set_xlabel('Mean AUROC')
# ax.set_title('Mean AUROC of classifiers')

# make the figure narrower to fit the legend
fig.tight_layout()

plt.savefig('mean_auroc.png', dpi=300)