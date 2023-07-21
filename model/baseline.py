import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import sys
import json
from pathlib import Path
import numpy as np
import tensorflow as tf
import scipy.stats as st
import matplotlib.pyplot as plt
from attention_layer import SelfAttention
from tensorflow.keras import optimizers
from tensorflow.keras.metrics import AUC
from tensorflow.keras.models import Model
from tensorflow.keras import backend as K
from tensorflow.keras.regularizers import l1
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.utils import to_categorical, plot_model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.layers import Dense, LSTM, Conv2D, Lambda, Input, Dropout
from sklearn.metrics import accuracy_score, recall_score, f1_score, classification_report, log_loss, roc_auc_score
 

SEED = 42

def model(input_shape, num_labels, LSTM_units, num_conv_filters, batch_size, F, D):

    inputs = Input(shape=input_shape)
    x = Conv2D(num_conv_filters, kernel_size = KERNEL_SIZE, strides=STRIDE, padding='valid', data_format="channels_last", kernel_regularizer=l1(L1))(inputs)

    # x = Dropout(DROPOUT_RATE)(x)

    rnn_in = Lambda(lambda x: K.squeeze(x, axis = 2))(x)
    rnn_out, _, _ = LSTM(LSTM_units, return_sequences=True, name='lstm', return_state=True, dropout=DROPOUT_RATE)(rnn_in)

    encoder_out, _ = SelfAttention(size=F, num_hops=D, use_penalization=False)(rnn_out)
    dense_out = Dense(num_labels, activation = 'Softmax')(encoder_out)

    model = Model(inputs=inputs, outputs=dense_out)

    model.summary()

    plot_model(model, to_file=SAVE_DIR / str(NAME+'_model.png'), show_shapes=True, show_layer_names=True)

    return model

def get_input(args):

    # read the hyperparameters from a jason file
    with open(args[1]) as f:
        data = json.load(f)

        global L1, STRIDE, KERNEL_SIZE, EPOCH, BATCH_SIZE, LSTM_UNITS, CNN_FILTERS, PATIENCE, F, D, NUM_LABELS, LEARNING_RATE, BASE_DIR, DATA_DIR, DATA_FILE, SAVE_DIR, CHART_DIR, NAME, DROPOUT_RATE
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
        LEARNING_RATE = data['LEARNING_RATE']
        BASE_DIR = Path(data['BASE_DIR'])
        DATA_DIR = BASE_DIR / data['DATA_DIR']
        # DATA_FILE = DATA_DIR / data['DATA_FILE']
        SAVE_DIR = BASE_DIR / data['SAVE_DIR']
        CHART_DIR = BASE_DIR / data['CHART_DIR']
        NAME = data['NAME']
        DROPOUT_RATE = data['DROPOUT_RATE']

def plot(history, metric, plot_path, figsize=[8,6], fontsize=16):
    plt.figure(figsize=figsize)
    plt.plot(history.history[metric],'r',linewidth=3.0)
    plt.plot(history.history['val_'+metric],'b',linewidth=3.0)
    plt.legend(['Training '+metric, 'Validation '+metric],fontsize=fontsize)
    plt.xlabel('Epochs ',fontsize=fontsize)
    plt.ylabel(metric,fontsize=fontsize)
    plt.ylim(0,1)
    plt.title('Learning Curve',fontsize=fontsize)
    plt.savefig(plot_path)
    plt.close()


if __name__ == '__main__':
    tf.random.set_seed(SEED)
    np.random.seed(SEED)

    get_input(sys.argv)

    DATA_FILE = DATA_DIR / sys.argv[2]


    tmp = np.load(DATA_FILE, allow_pickle=True)

    data = tmp['data']
    X = data[:,2]
    X = np.array([X[i] for i in range(len(X))])
    X /= 255
    y = data[:,3]
    y = to_categorical(y)

    folds = tmp['folds_index']

    avg_acc = []
    avg_recall = []
    avg_f1 = []
    avg_auc_roc = []

    for i in range(len(folds)):
    # for i in range(1):
        print("fold", i)

        train_idx = folds[i][0]
        test_idx = folds[i][1]

        X_train, y_train = X[train_idx], y[train_idx]
        X_test, y_test = X[test_idx], y[test_idx]

        fold_model = model(input_shape= X.shape[1:], num_labels = NUM_LABELS, LSTM_units = LSTM_UNITS, \
            num_conv_filters = CNN_FILTERS, batch_size = BATCH_SIZE, F = F, D= D)

        met = ['acc', tf.keras.metrics.AUC(curve='PR', name='auc-prc'),  tf.keras.metrics.AUC(curve='ROC', name='auc-roc')]
        met_names = ['acc', 'auc-prc', 'auc-roc']
        opt = optimizers.Adam(learning_rate=LEARNING_RATE)
        model_filename = SAVE_DIR / str(NAME+'_best_model_' + '_fold_' + str(i) + '.h5')        
        callbacks = [EarlyStopping(monitor='val_auc-roc', patience=PATIENCE), ModelCheckpoint(filepath=model_filename, monitor='val_auc-roc', save_best_only=True, mode='max')]

        fold_model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=[met])

        history = fold_model.fit(X_train, y_train, epochs=EPOCH, batch_size=BATCH_SIZE, verbose=2, callbacks=callbacks, validation_data=(X_test, y_test))

        early_stopping_epoch = callbacks[0].stopped_epoch
        print('Early stopping epoch: ' + str(early_stopping_epoch))

        # random model to label 0 or 1
        y_pred_random = np.random.randint(NUM_LABELS, size=y_test.shape[0]) 
        y_pred_random = to_categorical(y_pred_random)

        #Plot the Loss and Metric Curves
        plot_path = CHART_DIR / str(NAME + '_loss_' + 'fold_' + str(i) + '.png')
        plot(history, 'loss', plot_path)

        for met_name in met_names:
            plot_path = CHART_DIR / str(NAME + '_'+met_name+'_' + 'fold_' + str(i) + '.png')
            plot(history, met_name, plot_path)

        # Evaluate model and predict data on TEST 
        print("******Evaluating TEST set*********")
        fold_model.load_weights(model_filename)
        y_test_predict = fold_model.predict(X_test, batch_size=BATCH_SIZE, verbose=2)
        y_test_predict = np.argmax(y_test_predict, axis=1)
        y_test = np.argmax(y_test, axis=1)

        # calculate AUC_ROC
        fold_auc_roc = roc_auc_score(y_test, y_test_predict, average='macro')
        avg_auc_roc.append(fold_auc_roc)

        # calculate accuracy
        fold_acc = accuracy_score(y_test, y_test_predict)
        avg_acc.append(fold_acc)

        # calculate recall
        fold_recall = recall_score(y_test, y_test_predict, average='macro')
        avg_recall.append(fold_recall)

        # calculate f1
        fold_f1 = f1_score(y_test, y_test_predict, average='macro')
        avg_f1.append(fold_f1)        

        # print classification report
        print(classification_report(y_test, y_test_predict))

        print("******Evaluating RANDOM Model*********")
        y_pred_random = np.argmax(y_pred_random, axis=1)
        print(classification_report(y_test, y_pred_random))
        print('______________________________________________________')


    print(fold_model.summary())

    ic_auc_roc = st.t.interval(0.9, len(avg_auc_roc) - 1, loc=np.mean(avg_auc_roc), scale=st.sem(avg_auc_roc))
    ic_acc = st.t.interval(0.9, len(avg_acc) - 1, loc=np.mean(avg_acc), scale=st.sem(avg_acc))
    ic_recall = st.t.interval(0.9, len(avg_recall) - 1, loc=np.mean(avg_recall), scale=st.sem(avg_recall))
    ic_f1 = st.t.interval(0.9, len(avg_f1) - 1, loc = np.mean(avg_f1), scale=st.sem(avg_f1))

    print('Mean AUC_ROC[{:.4f}] IC [{:.4f}, {:.4f}]'.format(np.mean(avg_auc_roc), ic_auc_roc[0], ic_auc_roc[1]))
    print('Mean Accuracy[{:.4f}] IC [{:.4f}, {:.4f}]'.format(np.mean(avg_acc), ic_acc[0], ic_acc[1]))
    print('Mean Recall[{:.4f}] IC [{:.4f}, {:.4f}]'.format(np.mean(avg_recall), ic_recall[0], ic_recall[1]))
    print('Mean F1[{:.4f}] IC [{:.4f}, {:.4f}]'.format(np.mean(avg_f1), ic_f1[0], ic_f1[1]))

    print('Median AUC_ROC[{:.4f}]'.format(np.median(avg_auc_roc)))
    print('Median Accuracy[{:.4f}]'.format(np.median(avg_acc)))
    print('Median Recall[{:.4f}]'.format(np.median(avg_recall)))
    print('Median F1[{:.4f}]'.format(np.median(avg_f1)))
