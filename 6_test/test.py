import sys
sys.path.insert(1, "../5_train/")
from model import *
import pandas as pd
from sklearn.metrics import classification_report
from tensorflow.keras.utils import to_categorical
import numpy as np
import json


def get_input(hyperparameters_file):

    # read the hyperparameters from a jason file
    with open(hyperparameters_file) as f:
        data = json.load(f)

        global kernel_size, epoch, batch_size, lstm_units, cnn_filters, dropout_rate, patience, F, D, num_labels, learning_rate
        kernel_size = data['kernel_size']
        epoch = data['epoch']
        batch_size = data['batch_size']
        lstm_units = data['lstm_units']
        cnn_filters = data['cnn_filters']
        dropout_rate = data['dropout_rate']
        patience = data['patience']
        F = data['F']
        D = data['D']
        num_labels = data['num_labels']
        learning_rate = data['learning_rate']


if __name__ == '__main__':
    get_input("../5_train/hyp.json")
    data_dir = sys.argv[1]
    model_dir = data_dir+'/'+sys.argv[2]
    model_name = sys.argv[3]
    test_data_path = data_dir+'/'+sys.argv[4]
    test_labels_path = data_dir+'/'+sys.argv[5]
    # load the labels
    test_labels = pd.read_csv(test_labels_path)
    test_labels = test_labels[['name_1', 'name_2', 'label']]
    test_labels.columns = ['name_1', 'name_2', 'true']

    # load the data
    tmp = np.load(test_data_path, allow_pickle=True)

    test_data = tmp['data']
    X = test_data[:,2]
    X = np.array([X[i] for i in range(len(X))])
    y = test_data[:,3]
    y = to_categorical(y)

    test_model = model(input_shape= X.shape[1:], num_labels = num_labels, lstm_units = lstm_units, \
        cnn_filters = cnn_filters, F = F, D= D, kernel_size = kernel_size, dropout_rate = dropout_rate)

    for fold in range(10):
        test_model.load_weights(model_dir+ '/' +str(model_name+'_best_model_' + '_fold_' + str(fold) + '.keras'))
        y_pred = test_model.predict(X, verbose=0)
        y_pred = np.argmax(y_pred, axis=1)

        y_true = np.argmax(y, axis=1)

        pred = pd.DataFrame(test_data[:,0:2], columns=['name_1', 'name_2'])
        pred[f'pred_{fold}'] = y_pred

        def get_pred(name_1, name_2):
            # if pred[name_1, name_2] or pred[name_2, name_1] is present return its f'pred_{i}' else return Nan
            if pred[(pred['name_1'] == name_1) & (pred['name_2'] == name_2)].shape[0] > 0:
                return pred[(pred['name_1'] == name_1) & (pred['name_2'] == name_2)][f'pred_{fold}'].values[0]
            elif pred[(pred['name_1'] == name_2) & (pred['name_2'] == name_1)].shape[0] > 0:
                return pred[(pred['name_1'] == name_2) & (pred['name_2'] == name_1)][f'pred_{fold}'].values[0]
            else:
                return None

        test_labels[f'pred_{fold}'] = test_labels.apply(lambda row: get_pred(row['name_1'], row['name_2']), axis=1)
    
    def median_pred(row):
        # RETURN MEDIAN UNLESS THERE IS A NAN THEN RETURN None
        if row.isna().sum() > 0:
            return None
        else:
            return int(np.median(row[3:]))

    # get the median of the predictions of reps as pred
    test_labels['pred'] = test_labels.apply(lambda row: median_pred(row), axis=1)

    # print number of predicted labels None and their actual label (e.g. "11 os were not labeled and 16 1s were not labeled"), and remove them from the dataframe
    txid = str(test_labels_path).split('/')[-2]
    print("*"*20 + str(txid) + "*"*20)
    print(f"{test_labels[test_labels['true'] == 0]['pred'].isna().sum()} non-operons were not labeled and {test_labels[test_labels['true'] == 1]['pred'].isna().sum()} operons were not labeled ", end='\n\n')


    test_labels = test_labels[test_labels['pred'].notna()]

    y_true = test_labels.true
    y_pred = test_labels.pred

    # print classification report
    print("Classification report")
    print(classification_report(y_true, y_pred))
    print(pd.crosstab(y_true, y_pred, rownames=['True'], colnames=['Predicted'], margins=True))
    print("*"*50)

    # save y_true, y_pred in here/outputs/NAME_txid_output.csv
    # test_labels.to_csv(str('outputs/' + model_name + '_' + txid + '.csv'), index=False)




    
    

