
import pandas as pd
from sklearn.metrics import classification_report
import sys
import numpy as np

if __name__ == '__main__':

    # read gene_pairs and true labels
    dir = sys.argv[1]
    label_path = dir + '/' + sys.argv[2]
    reps = sys.argv[3].split(',')

    genes = pd.read_csv(label_path)
    genes = genes[['name_1', 'name_2', 'label']]
    genes.columns = ['name_1', 'name_2', 'true']

    # remove pairs with label 2
    genes = genes[genes['true'] != 2]
    
    for i, rep in enumerate(reps):
        
        models = ['GNB', 'LR', 'MLP', 'RF', 'SVM', 'XGB']
        # models = ['GNB']
        # for each models reaf predicted labels and merge them together
        # create a empty dataframe with columns name_1, name_2
        pred = pd.DataFrame(columns=['name_1', 'name_2'])
        for model in models:
            path = dir + '/os_outputs/' + rep + '_' + model + '_predictions.csv'
            pred_model = pd.read_csv(path, sep="\t")
            pred_model.columns = ['name_1', 'name_2'] + [model]
            pred = pd.merge(pred, pred_model[['name_1', 'name_2', model]], on=['name_1', 'name_2'], how='outer')

        # vote 
        pred[f'pred_{i}'] = pred.apply(lambda row: 1 if sum(row[models]) >= 4 else 0, axis=1)

        def get_pred(name_1, name_2):
            # if pred[name_1, name_2] or pred[name_2, name_1] is present return its f'pred_{i}' else return Nan
            if pred[(pred['name_1'] == name_1) & (pred['name_2'] == name_2)].shape[0] > 0:
                return pred[(pred['name_1'] == name_1) & (pred['name_2'] == name_2)][f'pred_{i}'].values[0]
            elif pred[(pred['name_1'] == name_2) & (pred['name_2'] == name_1)].shape[0] > 0:
                return pred[(pred['name_1'] == name_2) & (pred['name_2'] == name_1)][f'pred_{i}'].values[0]
            else:
                return None

        genes[f'pred_{i}'] = genes.apply(lambda row: get_pred(row['name_1'], row['name_2']), axis=1)

        
    def median_pred(row):
        # RETURN MEDIAN UNLESS THERE IS A NAN THEN RETURN None
        if row.isna().sum() > 0:
            return None
        else:

            return int(np.median(row[3:]))

    # get the median of the predictions of reps as pred
    genes['pred'] = genes.apply(lambda row: median_pred(row), axis=1)

    # print number of predicted labels None and their actual label (e.g. "11 os were not labeled and 16 1s were not labeled"), and remove them from the dataframe
    txid = label_path.split('/')[-2]
    print("*"*20 + str(txid) + "*"*20)
    print(f"{genes[genes['true'] == 0]['pred'].isna().sum()} non-operons were not labeled and {genes[genes['true'] == 1]['pred'].isna().sum()} operons were not labeled ", end='\n\n')
    

    genes = genes[genes['pred'].notna()]
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
    genes.to_csv(str('outputs/os_' + txid + '.csv'), index=False)
