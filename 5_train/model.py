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
from tensorflow.keras.models import Model
from tensorflow.keras import backend as K
from tensorflow.keras.utils import to_categorical
# from tensorflow.keras.utils.vis_utils import plot_model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.layers import Dense, LSTM, Conv2D, Lambda, Input
from sklearn.metrics import accuracy_score, recall_score, f1_score, classification_report, roc_auc_score

SEED = 42

def model(input_shape, num_labels, lstm_units, cnn_filters, F, D):

    inputs = Input(shape=input_shape)
    cnn = Conv2D(cnn_filters, kernel_size = kernel_size, padding='valid', data_format="channels_last")(inputs)
    
    rnn_in = Lambda(lambda l: K.squeeze(l, axis = 2))(cnn)

    rnn_out, _, _ = LSTM(lstm_units, return_sequences=True, name='lstm', return_state=True, dropout=dropout_rate)(rnn_in)

    encoder_out, _ = SelfAttention(size=F, num_hops=D, use_penalization=False)(rnn_out)

    # normalizing the output of the encoder lambda layer
    encoder_out = Lambda(lambda x: K.l2_normalize(x, axis=1))(encoder_out)

    dense_out = Dense(num_labels, activation='softmax')(encoder_out)

    model = Model(inputs=inputs, outputs=dense_out)

    model.summary()

    # plot_model(model, to_file=models_dir+ '/' +str(model_name+'_model.png'), show_shapes=True, show_layer_names=True)

    return model

def get_input(args):

    # read the hyperparameters from a jason file
    hyperparameters_file = Path(args[1])
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

        global input_file, models_dir, figs_dir, model_name
        data_dir =  data['data_dir']
        input_file = data_dir+ '/' +data['input_file']
        models_dir =  data_dir+ '/' +data['models_dir']
        if not os.path.exists(models_dir):
            os.makedirs(models_dir)
        figs_dir =  data_dir+ '/' +data['figs_dir']
        if not os.path.exists(figs_dir):
            os.makedirs(figs_dir)
        model_name = data['model_name']

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


    tmp = np.load(input_file, allow_pickle=True)

    data = tmp['data']
    X = data[:,2]
    X = np.array([X[i] for i in range(len(X))])
    y = data[:,3]
    y = to_categorical(y)

    folds = tmp['folds_index']

    avg_acc = []
    avg_recall = []
    avg_f1 = []
    avg_AUROC = []

    for i in range(len(folds)):
        print("fold", i)

        train_idx, test_idx = folds[i]

        X_train, y_train = X[train_idx], y[train_idx]
        X_test, y_test = X[test_idx], y[test_idx]

        fold_model = model(input_shape= X.shape[1:], num_labels = num_labels, lstm_units = lstm_units, \
            cnn_filters = cnn_filters, F = F, D= D)

        metrics = [tf.keras.metrics.AUC(curve='PR', name='AUPRC'), 'acc',  tf.keras.metrics.AUC(curve='ROC', name='AUROC')]
        metrics_names = ['AUPRC', 'acc' , 'AUROC']

        optimizer = optimizers.Adam(learning_rate=learning_rate)

        model_filename = models_dir+ '/' +str(model_name+'_best_model_' + '_fold_' + str(i) + '.keras')        
        checkpoint = ModelCheckpoint(filepath=model_filename, monitor='val_AUROC', save_best_only=True, mode='max')
        early_stopping = EarlyStopping(monitor='val_AUROC', patience=patience, restore_best_weights = True)

        fold_model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=metrics)

        history = fold_model.fit(X_train, y_train, epochs=epoch, batch_size=batch_size, verbose=2, callbacks=[early_stopping, checkpoint], validation_data=(X_test, y_test))

        early_stopping_epoch = early_stopping.stopped_epoch

        # random model to label 0 or 1
        y_pred_random = np.random.randint(num_labels, size=y_test.shape[0]) 
        y_pred_random = to_categorical(y_pred_random)

        #Plot the Loss and Metric Curves
        plot_path = figs_dir+ '/' +str(model_name + '_loss_' + 'fold_' + str(i) + '.png')
        plot(history, 'loss', plot_path)

        for metric_name in metrics_names:
            plot_path = figs_dir+ '/' +str(model_name + '_'+metric_name+'_' + 'fold_' + str(i) + '.png')
            plot(history, metric_name, plot_path)

        # Evaluate model and predict data on TEST 
        print("******Evaluating TEST set*********")
        fold_model.load_weights(model_filename)
        y_test_predict = fold_model.predict(X_test, batch_size=batch_size, verbose=2)
        y_test_predict = np.argmax(y_test_predict, axis=1)
        y_test = np.argmax(y_test, axis=1)

        # calculate AUROC
        fold_AUROC = roc_auc_score(y_test, y_test_predict, average='macro')
        avg_AUROC.append(fold_AUROC)

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

    ic_AUROC = st.t.interval(0.9, len(avg_AUROC) - 1, loc=np.mean(avg_AUROC), scale=st.sem(avg_AUROC))
    ic_acc = st.t.interval(0.9, len(avg_acc) - 1, loc=np.mean(avg_acc), scale=st.sem(avg_acc))
    ic_recall = st.t.interval(0.9, len(avg_recall) - 1, loc=np.mean(avg_recall), scale=st.sem(avg_recall))
    ic_f1 = st.t.interval(0.9, len(avg_f1) - 1, loc = np.mean(avg_f1), scale=st.sem(avg_f1))

    print('Mean  AUROC[{:.4f}] IC [{:.4f}, {:.4f}]'.format(np.mean(avg_AUROC), ic_AUROC[0], ic_AUROC[1]))
    print('Mean Accuracy[{:.4f}] IC [{:.4f}, {:.4f}]'.format(np.mean(avg_acc), ic_acc[0], ic_acc[1]))
    print('Mean Recall[{:.4f}] IC [{:.4f}, {:.4f}]'.format(np.mean(avg_recall), ic_recall[0], ic_recall[1]))
    print('Mean F1[{:.4f}] IC [{:.4f}, {:.4f}]'.format(np.mean(avg_f1), ic_f1[0], ic_f1[1]))

    print('Median  AUROC[{:.4f}]'.format(np.median(avg_AUROC)))
    print('Median Accuracy[{:.4f}]'.format(np.median(avg_acc)))
    print('Median Recall[{:.4f}]'.format(np.median(avg_recall)))
    print('Median F1[{:.4f}]'.format(np.median(avg_f1)))
