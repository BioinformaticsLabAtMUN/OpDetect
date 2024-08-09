# load the model and test it on the test data
# model file is in ../5_train/model.py, and weights are at models_dir+ '/' +str(model_name+'_best_model_' + '_fold_' + str(i) + '.keras')
# test data is in ../3_preprocess/test_data.npy
# test labels are in ../3_preprocess/test_labels.npy
# output is the accuracy of the model on the test data
# output is saved in ../6_test/accuracy.npy

import numpy as np
import pandas as pd
import sys
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from tensorflow.keras.models import load_model
from sklearn.metrics import classification_report
from tensorflow.keras.utils import to_categorical


# models_dir = '../5_train/models'
# model_name = 'model'
# test_data_path = '../3_preprocess/test_data.npy'
# test_labels_path = '../3_preprocess/test_labels.npy'
# output_path = '../6_test/accuracy.npy'

# test_data = np.load(test_data_path)
# test_labels = np.load(test_labels_path)

# accuracy = []
# for i in range(5):
#     model = load_model(models_dir+ '/' +str(model_name+'_best_model_' + '_fold_' + str(i) + '.keras'))
#     y_pred = model.predict(test_data)
#     y_pred = np.argmax(y_pred, axis=1)
#     accuracy.append(accuracy_score(test_labels, y_pred))

# accuracy = np.array(accuracy)
# np.save(output_path, accuracy)
# print('accuracy:', accuracy)


if __name__ == '__main__':
    data_dir = sys.argv[1]
    model_dir = data_dir+'/'+sys.argv[2]
    model_name = sys.argv[3]
    test_data_path = data_dir+'/'+sys.argv[4]
    test_labels_path = data_dir+'/'+sys.argv[5]
    print('data_dir:', data_dir)

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

    for fold in range(10):

        test_model = load_model(model_dir+ '/' +str(model_name+'_best_model_' + '_fold_' + str(fold) + '.keras'))
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




    
    

