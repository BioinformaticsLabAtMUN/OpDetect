import pandas as pd
from sklearn.metrics import classification_report
import sys
import numpy as np

txid = sys.argv[1]
pred_path = '../../operons/data_odb/'+txid+'/of_outputs/operons.txt'
preds = pd.read_csv(pred_path, sep='\t', header=None)

label_path = '../../operons/data_odb/'+txid+'/gene_pairs.csv'
labels = pd.read_csv(label_path)
labels.columns = ['name_1', 'name_2', 'true']

genes = labels.copy()

# modify preds
def make_pair(operon_pair_list, genes):
    if len(genes) > 1:
        for gene_1 in genes:
            for gene_2 in genes:
                if not gene_1 == gene_2:
                    operon_pair_list.append([gene_1, gene_2])
                    operon_pair_list.append([gene_2, gene_1])

operon_pair_list=[]
preds.apply(lambda row: make_pair(operon_pair_list, row[0].split(',')), axis=1)

genes['pred'] = genes.apply(lambda row: 1 if [row.name_1.split(',')[0], row.name_2.split(',')[0]] in operon_pair_list else 0, axis=1)
genes.reset_index(drop=True, inplace=True)

# # separate all the gene names in preds file and put them in a list
# gene_names = []
# preds.apply(lambda row: gene_names.extend(row[0].split(',')), axis=1)
# gene_names = list(set(gene_names))

# # if a pair is predicted 0 and either of the genes are not in the gene_names list, pred 2
# genes['pred'] = genes.apply(lambda row: 2 if row.pred == 0 and (row.name_1.split(',')[0] not in gene_names or row.name_2.split(',')[0] not in gene_names) else row.pred, axis=1)


# print number of predicted labels 2 and their actual label (e.g. "11 os were not labeled and 16 1s were not labeled"), and remove them frof the dataframe
print("*"*20 + str(txid) + "*"*20)
print(f"{genes[(genes['true'] == 0) & (genes['pred'] == 2)].shape[0]} non-operons were not labeled and {genes[(genes['true'] == 1) & (genes['pred'] == 2)].shape[0]} operons were not labeled", end='\n\n')

# genes = genes[genes['pred'] != 2]
genes = genes[genes['true'] != 2]

y_true = genes.true
y_pred = genes.pred

# convert y_true and y_pred to int
y_true = y_true.astype(int)
y_pred = y_pred.astype(int)

# print classification report
print("Classification report")
print(classification_report(y_true, y_pred))
print(pd.crosstab(y_true, y_pred, rownames=['True'], colnames=['Predicted'], margins=True))
print("*"*50)

# save y_true, y_pred in here/outputs/NAME_txid_output.csv
genes.to_csv(str('outputs/of_' + txid + '.csv'), index=False)
