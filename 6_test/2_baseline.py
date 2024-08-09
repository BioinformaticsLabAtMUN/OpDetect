import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import numpy as np
import pandas as pd
from sklearn.metrics import classification_report
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Model
from tensorflow.keras import backend as K
from tensorflow.keras.layers import Dense, LSTM, Conv2D, Lambda, Input, Dropout
from tensorflow.keras.regularizers import l1
import sys
import json
from pathlib import Path


sys.path.insert(1, "../5_model/")
from attention_layer import SelfAttention

def model(input_shape, num_labels, LSTM_units, num_conv_filters, batch_size, F, D):

    inputs = Input(shape=input_shape)
    x = Conv2D(num_conv_filters, kernel_size = KERNEL_SIZE, strides=STRIDE, padding='valid', data_format="channels_last", kernel_regularizer=l1(L1))(inputs)

    x = Dropout(DROPOUT_RATE)(x)

    rnn_in = Lambda(lambda x: K.squeeze(x, axis = 2))(x)
    rnn_out, _, _ = LSTM(LSTM_units, return_sequences=True, name='lstm', return_state=True, kernel_regularizer=l1(L1))(rnn_in) #return_state=True

    encoder_out, _ = SelfAttention(size=F, num_hops=D, use_penalization=False)(rnn_out)
    dense_out = Dense(num_labels, activation = 'Softmax')(encoder_out)

    model = Model(inputs=inputs, outputs=dense_out)

    return model

def get_input(args):

    # read the hyperparameters from a jason file
    with open(args[1]) as f:
        data = json.load(f)

        global L1, STRIDE, KERNEL_SIZE, EPOCH, BATCH_SIZE, LSTM_UNITS, CNN_FILTERS, PATIENCE, F, D, NUM_LABELS, BASE_DIR, DATA_DIR, DATA_FILE, SAVE_DIR, NAME, DROPOUT_RATE
        L1 = data['L1']
        STRIDE = data['STRIDE']
        KERNEL_SIZE = data['KERNEL_SIZE']
        EPOCH = data['EPOCH']
        BATCH_SIZE = data['BATCH_SIZE']
        LSTM_UNITS = data['LSTM_UNITS']
        CNN_FILTERS = data['CNN_FILTERS']
        PATIENCE = data['PATIENCE']
        F = data['F']
        D = data['D']
        NUM_LABELS = data['NUM_LABELS']
        BASE_DIR = Path(data['BASE_DIR'])
        DATA_DIR = BASE_DIR / data['DATA_DIR']
        DATA_FILE = DATA_DIR / args[3]
        SAVE_DIR = BASE_DIR / data['SAVE_DIR']
        NAME = data['NAME']
        DROPOUT_RATE = data['DROPOUT_RATE']
        

if __name__ == '__main__':

    get_input(sys.argv)

    label_path = DATA_DIR / sys.argv[2]
    genes = pd.read_csv(label_path)
    genes = genes[['name_1', 'name_2', 'label']]
    genes.columns = ['name_1', 'name_2', 'true']

    tmp = np.load(DATA_FILE, allow_pickle=True)

    data = tmp['data']
    X = data[:,2]
    X = np.array([X[i] for i in range(len(X))])
    X /= 255
    y = data[:,3]
    y = to_categorical(y)

    test_model = model(input_shape= X.shape[1:], num_labels = NUM_LABELS, LSTM_units = LSTM_UNITS, \
        num_conv_filters = CNN_FILTERS, batch_size = BATCH_SIZE, F = F, D= D)

    # keep the prediction of each fold in a list
    # y_pred_list = []
    for fold in range(10):
        weights = SAVE_DIR / str(NAME + '_best_model_' + '_fold_' + str(fold) + '.h5')
        test_model.load_weights(weights)

        # test model with test data
        y_pred = test_model.predict(X, batch_size=BATCH_SIZE, verbose=0)
        y_pred = np.argmax(y_pred, axis=1)

        y_true = np.argmax(y, axis=1)

        # y_pred_list.append(y_pred)

        # print classification report
        # print("Classification report for fold " + str(fold))
        # print(classification_report(y_true, y_pred))

        # # # print confusion matrix
        # print(pd.crosstab(y_true, y_pred, rownames=['True'], colnames=['Predicted'], margins=True))
        # print("\n\n")

        # make a df of names from column 0  and 1 data and predictions from y_pred
        pred = pd.DataFrame(data[:,0:2], columns=['name_1', 'name_2'])
        pred[f'pred_{fold}'] = y_pred

        def get_pred(name_1, name_2):
            # if pred[name_1, name_2] or pred[name_2, name_1] is present return its f'pred_{i}' else return Nan
            if pred[(pred['name_1'] == name_1) & (pred['name_2'] == name_2)].shape[0] > 0:
                return pred[(pred['name_1'] == name_1) & (pred['name_2'] == name_2)][f'pred_{fold}'].values[0]
            elif pred[(pred['name_1'] == name_2) & (pred['name_2'] == name_1)].shape[0] > 0:
                return pred[(pred['name_1'] == name_2) & (pred['name_2'] == name_1)][f'pred_{fold}'].values[0]
            else:
                return None

        genes[f'pred_{fold}'] = genes.apply(lambda row: get_pred(row['name_1'], row['name_2']), axis=1)


    def median_pred(row):
        # RETURN MEDIAN UNLESS THERE IS A NAN THEN RETURN None
        if row.isna().sum() > 0:
            return None
        else:
            return int(np.median(row[3:]))

    # get the median of the predictions of reps as pred
    genes['pred'] = genes.apply(lambda row: median_pred(row), axis=1)

    # print number of predicted labels None and their actual label (e.g. "11 os were not labeled and 16 1s were not labeled"), and remove them from the dataframe
    txid = str(label_path).split('/')[-2]
    print("*"*20 + str(txid) + "*"*20)
    print(f"{genes[genes['true'] == 0]['pred'].isna().sum()} non-operons were not labeled and {genes[genes['true'] == 1]['pred'].isna().sum()} operons were not labeled ", end='\n\n')


    genes = genes[genes['pred'].notna()]

    # get the median of the predictions of all folds as the voting prediction
    # y_pred_list = np.array(y_pred_list)
    # y_pred_list = np.transpose(y_pred_list, (1, 0))
    # y_pred = np.median(y_pred_list, axis=1)
    # y_pred = np.rint(y_pred)

    y_true = genes.true
    y_pred = genes.pred

    # print classification report
    print("Classification report")
    print(classification_report(y_true, y_pred))
    print(pd.crosstab(y_true, y_pred, rownames=['True'], colnames=['Predicted'], margins=True))
    print("*"*50)

    # save y_true, y_pred in here/outputs/NAME_txid_output.csv
    genes.to_csv(str('outputs/' + NAME + '_' + txid + '.csv'), index=False)
