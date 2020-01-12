import numpy as np
from matplotlib import pyplot as plt
import sklearn.model_selection as model_selection
import tensorflow as tf
from keras import layers
from keras import backend as K
from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from keras.models import Sequential, load_model, model_from_json
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.utils import to_categorical, normalize
from array_to_abt_np import array_to_abt_np, smooth_data
import pickle
#### Here is where we produce the model for digits 0-9


###################################
##### USER DEFINED INPUTS #########
###################################

name = 'model_digits_0_to_3_smooth'     # CHANGE NAME OF MODEL HERE
batch_size = 32             # CHANGE BATCH SIZE HERE
DROPOUT_RATE = 0.1        # dropout rate
mode = 1                    # 0 - no conv layer, 1 - conv layer, 2 - conv conv layer
num_classes = 4           # number of classes
all_datasets_to_train_on = 'all_datasets.p'
FEATURE_NUMS = 30
input_size = (FEATURE_NUMS,6,1)

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
    model.add(Dropout(DROPOUT_RATE))
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
    model.add(Dropout(DROPOUT_RATE))
    model.add(Dense(num_classes))                                # 1 NN layer, LAST LAYER must equal to number of classes
    model.add(Activation('softmax'))

    #opt = tf.keras.optimizers.Adam()
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    return model

def createModelwConvolutionMORE(): 

    ## DOES NOT WORK FOR NOW ##

    model = Sequential()  
    
    model.add(Conv2D(32, (3, 3), input_shape=(FEATURE_NUMS, 6, 1), padding="same"))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2), padding="same"))

    model.add(Conv2D(32, (3, 3), padding="same"))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    
    model.add(Flatten())
    model.add(Dense(batch_size))                       # 1 NN layer, FIRST LAYER must equal to batch size      
    model.add(Activation('relu'))
    model.add(Dropout(DROPOUT_RATE))
    model.add(Dense(num_classes))                                # 1 NN layer, LAST LAYER must equal to number of classes
    model.add(Activation('softmax'))

    #opt = tf.keras.optimizers.Adam()
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    return model


if mode == 0:
    model = createModel()                             
elif mode == 1:
    model = createModelwConvolution()
else:
    model = createModelwConvolutionMORE()



#####################################
#### Train model ####
#####################################

file = open(all_datasets_to_train_on,'rb')
raw_data = pickle.load(file)                             ## load data from pickle
data = raw_data['samples']                      ## 3-D data, with dimension (# of digits recorded, feature_table_dim_x, feature_table_dim_y)
labels = raw_data['labels']                            ## label the digit that the feature_table describes
file.close()

reduced_data = data[np.where(labels<num_classes)]
reduced_labels = labels[np.where(labels<num_classes)]

n_samples = reduced_data.shape[0]

features = np.empty(shape = (n_samples,input_size[0],input_size[1]))

for i,sample in enumerate(reduced_data):
    if input_size==(9,6,1):
        features[i] = array_to_abt_np(sample)
    elif input_size==(30,6,1):
        features[i] = smooth_data(sample)

features = normalize(features,axis=0)
bin_labels = to_categorical(reduced_labels)

if mode == 1:
    features = np.expand_dims(features, axis=3)
    
print('features size: {}'.format(features.shape))
print('bin_labels size: {}'.format(bin_labels.shape))

X_train, X_test, y_train, y_test = model_selection.train_test_split(features, bin_labels, train_size=0.75,test_size=0.25, random_state=10)
model.fit(X_train, y_train, batch_size = 32, epochs = 200, verbose = 1, validation_split = 0.25)

if mode:
    filename_model = name + '_conv2D' + ".hdf5"
else:
    filename_model = name + '_dense' + '.hdf5'

results = model.evaluate(X_test, y_test, batch_size=128)
print('test loss, test acc:', results)

filename_model = name + ".hdf5"
print('saved model to {}'.format(filename_model))
model.save(filename_model)











