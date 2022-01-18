from os import listdir
from os.path import isfile, join
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import cv2 as cv
import tensorflow as tf
from tensorflow.keras import datasets, layers, models
from keras.regularizers import l2
import keras

def prepare_data():
    path = 'big_symbols/'
    all_path = listdir('symbols_data')
    all_path.remove('.ipynb_checkpoints')

    subsets_len = []
    for j in range(len(all_path)):
        dir_path = path+all_path[j]+'/'
        symbol_dir = listdir(dir_path)
        subsets_len.append(len(symbol_dir))
    min_sub = min(subsets_len)

    X_train = []
    Y_train = []
    X_test = []
    Y_test = []
    for j in range(len(all_path)):
        dir_path = path+all_path[j]+'/'
        symbol_dir = listdir(dir_path)
        for i in range(len(symbol_dir)):
            if(symbol_dir[i] != '.ipynb_checkpoints'):
                img = cv.imread(dir_path+symbol_dir[i])
                gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
                gray = cv.resize(gray, (45,45), interpolation=cv.INTER_AREA)
                #thresh = gray
                ret, thresh = cv.threshold(gray,0,255,cv.THRESH_BINARY_INV+cv.THRESH_OTSU)
                thresh = cv.ximgproc.thinning(thresh) #možda maknuti treba
                if (i/(len(symbol_dir)))<0.7:
                    X_train.append(thresh)
                    Y_train.append(all_path[j])
                else:
                    X_test.append(thresh)
                    Y_test.append(all_path[j])
    X_train = np.asarray(X_train)/255
    Y_train = np.asarray(Y_train)
    X_test = np.asarray(X_test)/255
    Y_test = np.asarray(Y_test)

    layer2 = tf.keras.layers.CategoryEncoding(num_tokens=16, output_mode="one_hot")
    layer1 = tf.keras.layers.StringLookup(vocabulary=all_path)

    y_train = layer2(layer1(Y_train)-1)
    y_test = layer2(layer1(Y_test)-1)
    X_train = X_train.reshape([X_train.shape[0],X_train.shape[1],X_train.shape[2],1])
    X_test = X_test.reshape([X_test.shape[0],X_train.shape[1],X_train.shape[2],1])
    XTrain = tf.convert_to_tensor(X_train)
    yTrain = tf.convert_to_tensor(y_train)
    xTest = tf.convert_to_tensor(X_test)
    yTest = tf.convert_to_tensor(y_test)
    return XTrain,yTrain,xTest,yTest

#The model
def train_model():
    XTrain,yTrain,xTest,yTest = prepare_data()
    model = models.Sequential()
    model.add(layers.Conv2D(32, (5,5), activation='relu', input_shape=(45, 45, 1)))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(32, (3,3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(32, (3, 3), activation='relu'))
    model.add(layers.Flatten())
    model.add(layers.Dropout(0.2))
    model.add(layers.Dense(32, activation='relu'))
    #model.add(layers.Dropout(0.3))
    model.add(layers.Dense(16,activation='softmax'))

    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    history = model.fit(XTrain,yTrain, batch_size=32, epochs = 30, shuffle=True,validation_data=(xTest,yTest))
    model.save('model')
    return model