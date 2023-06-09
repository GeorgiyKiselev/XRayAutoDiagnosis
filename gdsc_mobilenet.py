# -*- coding: utf-8 -*-
"""GDSC_mobilenet.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vxYlKNijlSrUibzO8tvq6Q9uJTdnAYCG
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np 
import os
import pandas as pd 
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
# %matplotlib inline
from IPython.display import Image

import tensorflow as tf
from tensorflow.keras.models import Sequential,load_model, Model
from tensorflow.keras.layers import Dense, Flatten, Conv2D, Dropout,MaxPool2D, LSTM, GRU, BatchNormalization,Input
from tensorflow.keras.layers import Embedding, concatenate, Reshape,Activation
from tensorflow.keras.callbacks import ReduceLROnPlateau,EarlyStopping,ModelCheckpoint
from tensorflow.keras.layers import ELU


from tensorflow.keras.layers.experimental.preprocessing import RandomFlip
import tensorflow.keras.layers as tfl
from tensorflow.keras.preprocessing import image_dataset_from_directory
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import warnings
from keras.applications.mobilenet_v2 import MobileNetV2
from keras.applications import mobilenet_v2
from keras.utils import plot_model
from keras.callbacks import ReduceLROnPlateau, EarlyStopping, ModelCheckpoint
import keras.optimizers
warnings.filterwarnings('ignore')

from google.colab import drive
from pathlib import Path
import sys
drive.mount('/content/drive', force_remount=True)
base = Path('/content/drive/MyDrive')
sys.path.append(str(base))

zip_path = base/'XR_train.zip'
!cp {zip_path} .
!unzip -q XR_train.zip
!rm XR_train.zip

zip_path = base/'XR_test.zip'
!cp {zip_path} .
!unzip -q XR_test.zip
!rm XR_test.zip

train_df = pd.read_csv('/content/XR_train/train_df.csv')
test_df = pd.read_csv('/content/XR_test/test_df.csv')
train_path = '/content/XR_train/train_images'
test_path = '/content/XR_test/test_images'

img_size = 128
batch_size = 32

labels = os.listdir('/content/XR_test/test_images')


train_data = image_dataset_from_directory(train_path,
                                          labels = 'inferred',
                                          class_names = labels,
                                          color_mode = 'rgb',
                                          seed = 42,
                                          validation_split = 0.1,
                                          subset = 'training',
                                          batch_size = batch_size,
                                          image_size = (img_size, img_size),
                                          shuffle = True,
                                          label_mode = 'categorical'
                                          )

validation_data = image_dataset_from_directory(train_path,
                                          labels = 'inferred',
                                          class_names = labels,
                                          color_mode = 'rgb',
                                          seed = 42,
                                          validation_split = 0.1,
                                          subset = 'validation',
                                          batch_size = batch_size,
                                          image_size = (img_size, img_size),
                                          shuffle = False,
                                          label_mode = 'categorical')

TUNE = tf.data.experimental.AUTOTUNE
train_data = train_data.prefetch(buffer_size = TUNE)

from keras.applications.mobilenet import MobileNet
from keras.models import Sequential
from keras.layers import Flatten, Dense, Dropout, BatchNormalization, AveragePooling2D
raw_model = MobileNet(input_shape=(128,128,3), include_top = False, weights = None)
full_model = Sequential()
full_model.add(AveragePooling2D((2,2), input_shape = (img_size, img_size, 3)))
full_model.add(BatchNormalization())
full_model.add(raw_model)
full_model.add(Flatten())
full_model.add(Dropout(0.5))
full_model.add(Dense(64))
full_model.add(Dense(14, activation = 'sigmoid'))
full_model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['acc'])
full_model.summary()

from keras.callbacks import ModelCheckpoint, LearningRateScheduler, EarlyStopping, ReduceLROnPlateau
file_path="weights.best.hdf5"
checkpoint = ModelCheckpoint(file_path, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
early = EarlyStopping(monitor="val_acc", mode="max", patience=3)
callbacks_list = [checkpoint, early] #early

full_model.fit(train_data, 
               validation_data = validation_data,
               epochs=5, 
               verbose = True,
              shuffle = 'batch',
              callbacks = callbacks_list)