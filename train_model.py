import numpy as np
from matplotlib import pyplot as plt

import tensorflow as tf
from keras import layers
from keras import backend as K
from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from keras.models import Sequential, load_model, model_from_json
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.utils import to_categorical, normalize

from array_to_abt_np import array_to_abt_np
import pickle
#### Here is where we produce the model for digits 0-9


###################################
##### USER DEFINED INPUTS #########
###################################

name = 'model_digits_1'     # CHANGE NAME OF MODEL HERE
batch_size = 32             # CHANGE BATCH SIZE HERE
mode = 0                    # 0 - no conv layer, 1 - conv layer
input_size = (30,6,1)       #size of input tensor 
                            #(30,6,1) is temporal raw data
                            #(10,6,1) is feature extraction abt
                            
num_classes = 10            # number of classes
all_datasets_to_train_on = 'all_datasets.p'

#print(tf.__version__)



############################################
####   Model (modified from jrobchin)   ####
#### 3 conv + pool layers + 2 NN layers ####
############################################


def createModel():                                                            # Create model function
    model = Sequential()                                             

    model.add(Flatten())
    model.add(Dense(batch_size))                       # 1 NN layer, FIRST LAYER must equal to batch size      
    model.add(Activation('relu'))
    model.add(Dropout(0.2))
    model.add(Dense(num_classes))                                # 1 NN layer, LAST LAYER must equal to number of classes
    model.add(Activation('softmax'))

    #opt = tf.keras.optimizers.Adam()
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    return model

def createModelwConvolution():                                                            # Create model function
    model = Sequential()  
    
    model.add(Conv2D(32, (3, 3), input_shape=input_size))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    
    model.add(Flatten())
    model.add(Dense(batch_size))                       # 1 NN layer, FIRST LAYER must equal to batch size      
    model.add(Activation('relu'))
    model.add(Dropout(0.2))
    model.add(Dense(num_classes))                                # 1 NN layer, LAST LAYER must equal to number of classes
    model.add(Activation('softmax'))

    #opt = tf.keras.optimizers.Adam()
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    return model


if mode == 0:
    model = createModel()                             
else:
    model = createModelwConvolution()



#####################################
#### Train model ####
#####################################

file = open(all_datasets_to_train_on,'rb')
raw_data = pickle.load(file)                             ## load data from pickle
data = raw_data['samples']                      ## 3-D data, with dimension (# of digits recorded, feature_table_dim_x, feature_table_dim_y)
labels = raw_data['labels']                            ## label the digit that the feature_table describes
file.close()

n_samples = data.shape[0]

features = np.empty(shape = (n_samples,input_size[0],input_size[1]))

for i,sample in enumerate(data):
    #print('sample.shape: {}'.format(sample.shape))
    #print('features[i].shape: {}'.format(features[i].shape))
    abt = array_to_abt_np(sample)
    #print('abt.shape: {}'.format(abt.shape))
    features[i] = array_to_abt_np(sample)

features = normalize(features,axis=0)


bin_labels = to_categorical(labels)

if mode == 1:
    features = np.expand_dims(features, axis=3)

print('features size: {}'.format(features.shape))
print('bin_labels size: {}'.format(bin_labels.shape))

model.fit(features, bin_labels, batch_size = 32, epochs = 50, verbose = 1, validation_split = 0.2)

if mode:
    filename_model = name + 'conv2D' + ".hdf5"
else:
    filename_model = name + 'dense' + '.hdf5'

model.save(filename_model)











