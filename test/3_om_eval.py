import pandas as pd
from sklearn.metrics import classification_report
import sys
import numpy as np

txid = sys.argv[1]
pred_path = '../../operons/data_odb/'+txid+'/om_outputs/preds.csv'
preds = pd.read_csv(pred_path)

label_path = '../../operons/data_odb/'+txid+'/gene_pairs.csv'
labels = pd.read_csv(label_path)
labels.columns = ['name_1', 'name_2', 'true']

def add_pred(row):
    pred = preds.loc[(preds['name_1'] == row.name_1) & (preds['name_2'] == row.name_2)]
    if len(pred) == 0:
        # pred = preds.loc[(preds['name_1'] == row.name_2) & (preds['name_2'] == row.name_1)]
        # if len(pred) == 0:
        #     row['pred'] = 2
        # else:
        #     row['pred'] = pred['pred'].values[0]
        row['pred'] = 0
    else:
        row['pred'] = pred['pred'].values[0]
    return row

genes = labels.copy()
genes = labels.apply(add_pred, axis=1)

# print number of predicted labels 2 and their actual label (e.g. "11 os were not labeled and 16 1s were not labeled"), and remove them from the dataframe
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
genes.to_csv(str('outputs/om_' + txid + '.csv'), index=False)
