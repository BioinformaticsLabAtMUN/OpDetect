# Imports
from sklearn.metrics import classification_report, accuracy_score, recall_score, f1_score
from keras.utils import to_categorical
from matplotlib import pyplot as plt
from keras.optimizers import Adam
from keras.models import Model
from keras.metrics import AUC
from scipy import stats as st
from keras import callbacks
from typing import Tuple
from keras import layers
import tensorflow as tf
import numpy as np
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Settings
DATA_FILE = '../../operons/data_odb/data_processed.npz'
CHART_DIR = '../../operons/charts'
SAVE_DIR = '../../operons/results'
NAME = 'V13'
SEED = 42

tf.random.set_seed(SEED)
np.random.seed(SEED)

# Hyperparameters
KERNEL_SIZE = [5, 6]
LEARNING_RATE = 1e-3
ATTENTION_SIZE = 64
ATTENTION_HOPS = 32
DROPOUT_RATE = 1e-1
CNN_FILTERS = 128
NUM_EPOCHS = 100
STRIDES = [3, 3]
BATCH_SIZE = 32
LSTM_UNITS = 32
PATIENCE = 10

# Self Attention Layer
class SelfAttention(layers.Layer):
    def __init__(self, size:int, numHops:int) -> None:
        super().__init__()

        self.numHops = numHops
        self.size = size

    def get_config(self) -> dict:
        baseConfig = super().get_config()

        baseConfig['numHops'] = self.numHops
        baseConfig['size'] = self.size

        return baseConfig
    
    def build(self, inputShape:Tuple[int]) -> None:
        self.w1 = self.add_weight(name = 'w1', shape = (self.size, int(inputShape[2])), initializer = 'glorot_uniform', trainable = True)
        self.w2 = self.add_weight(name = 'w2', shape = (self.numHops, self.size), initializer = 'glorot_uniform', trainable = True)

        super().build(inputShape)

    def call(self, inputs:tf.Tensor) -> tf.Tensor:
        w1, w2 = self.w1[None, :, :], self.w2[None, :, :]
        w1, w2 = tf.tile(w1, [1, 1, 1]), tf.tile(w2, [1, 1, 1])

        hiddenStatesTransposed = layers.Permute(dims = (2, 1))(inputs)
        attentionScore = layers.Activation('tanh')(tf.matmul(w1, hiddenStatesTransposed))
        attentionWeights = layers.Activation('softmax')(tf.matmul(w2, attentionScore))
        embeddingMatrix = layers.Flatten()(tf.matmul(attentionWeights, inputs))

        return embeddingMatrix
    
# Initialize Model
def getModel(inputShape:Tuple[int]) -> Model:
    inputLayer = layers.Input(shape = inputShape)

    cnn = layers.Conv2D(CNN_FILTERS, kernel_size = KERNEL_SIZE, strides = STRIDES, padding = 'valid', data_format = 'channels_last')(inputLayer)

    resized = layers.Lambda(lambda x:tf.squeeze(x, axis = 2))(cnn)
    rnn, _, _ = layers.LSTM(LSTM_UNITS, dropout = DROPOUT_RATE, return_sequences = True, return_state = True)(resized)

    attention = SelfAttention(size = ATTENTION_SIZE, numHops = ATTENTION_HOPS)(rnn)

    outputLayer = layers.Dense(2, activation = 'softmax')(attention)

    model = Model(inputs = inputLayer, outputs = outputLayer)
    model.summary()

    return model

# Plot Model History
def plot(history:callbacks.History, metric:str, plotPath:str) -> None:
    plt.figure(figsize = [8, 6])

    plt.title('Learning Curve', fontsize = 16)
    plt.plot(history.history[f'val_{metric}'], 'b', linewidth = 3.0)
    plt.plot(history.history[metric], 'r', linewidth = 3.0)

    plt.legend([f'Validation {metric}', f'Training {metric}'], fontsize = 16)
    plt.xlabel('Epochs', fontsize = 16)
    plt.ylabel(metric, fontsize = 16)
    plt.ylim(0, 1)

    plt.savefig(plotPath)
    plt.close()

# Process Data
dataFile = np.load(DATA_FILE, allow_pickle = True)
data = dataFile['data']

X = data[:, 2]
X = np.array([X[q] for q in range(len(X))])
X /= 255

y = to_categorical(data[:, 3])

folds = dataFile['folds_index']

# Iterate Folds
recall, acc, F1 = [], [], []
for q in range(len(folds)):
    print(f'\nFold #{q}...')

    trainIndex, testIndex = folds[q]

    XTrain, yTrain = X[trainIndex], y[trainIndex]
    XTest, yTest = X[testIndex], y[testIndex]

    model = getModel(inputShape = X.shape[1:])

    optimizer = Adam(learning_rate = LEARNING_RATE)
    earlyStopping = callbacks.EarlyStopping(monitor = 'val_auc', patience = 10, restore_best_weights = True)
    modelCheckpoint = callbacks.ModelCheckpoint(filepath = f'{SAVE_DIR}/{NAME}_best_model_fold_{q}.h5', monitor = 'val_auc', save_best_only = True, mode = 'max')

    model.compile(optimizer = optimizer, loss = 'categorical_crossentropy', metrics = ['acc', AUC(curve = 'PR', name = 'auc')])
    history = model.fit(XTrain, yTrain, epochs = NUM_EPOCHS, batch_size = BATCH_SIZE, verbose = 2, callbacks = [earlyStopping, modelCheckpoint], validation_data = (XTest, yTest))

    plot(history, 'loss', f'{CHART_DIR}/{NAME}_loss_fold_{q}.png')
    plot(history, 'acc', f'{CHART_DIR}/{NAME}_acc_fold_{q}.png')
    plot(history, 'auc', f'{CHART_DIR}/{NAME}_auc_fold_{q}.png')

    print('\n##### Test Set #####')
    model.load_weights(f'{SAVE_DIR}/{NAME}_best_model_fold_{q}.h5')
    yPred = np.argmax(model.predict(XTest, batch_size = BATCH_SIZE, verbose = 2), axis = 1)
    yTest = np.argmax(yTest, axis = 1)

    recall += [recall_score(yTest, yPred, average = 'macro')]
    F1 += [f1_score(yTest, yPred, average = 'macro')]
    acc += [accuracy_score(yTest, yPred)]

    print(classification_report(yTest, yPred))

    print('\n##### Random Set #####')
    yPred = np.argmax(to_categorical(np.random.randint(2, size = len(yTest))), axis = 1)
    print(classification_report(yTest, yPred))

accInterval = st.t.interval(0.9, len(acc) - 1, loc = np.mean(acc), scale = st.sem(acc))
recallInterval = st.t.interval(0.9, len(recall) - 1, loc = np.mean(recall), scale = st.sem(recall))
F1Interval = st.t.interval(0.9, len(F1) - 1, loc = np.mean(F1), scale = st.sem(F1))

# Print Statistics
print(f'Mean Accuracy: {np.mean(acc):.4f}, IC: [{accInterval[0]:.4f}, {accInterval[1]:.4f}]')
print(f'Mean Recall: {np.mean(recall):.4f}, IC: [{recallInterval[0]:.4f}, {recallInterval[1]:.4f}]')
print(f'Mean F1: {np.mean(F1):.4f}, IC: [{F1Interval[0]:.4f}, {F1Interval[1]:.4f}]')

print(f'Median Accuracy: {np.median(acc):.4f}')
print(f'Median Recall: {np.median(recall):.4f}')
print(f'Median F1: {np.median(F1):.4f}')