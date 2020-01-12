## MAIN.PY -- VERSION 1, no threading
''' Script outline: 
0) Load network model 
1) Setup bluetooth comms
While comms active: 
    try: 
        2) Read serial data
        3) Pre-process data
        4) feed data into network
        5) display data in GUI 
    except KeyboardInterrupt: 
        6) Close comms
        break
'''
import numpy as np
import cv2
import pickle
import pandas as pd
from scipy import stats, fft, fftpack
from read_serial import read_serial
from record_dataset import record_data   
from array_to_abt_np import array_to_abt_np, smooth_data            
from matplotlib import pyplot as plt
import tensorflow as tf
import keras
from keras.utils import to_categorical, normalize
from keras.models import Sequential, load_model, model_from_json

# 0) Load network model
classes = {
    0: '0',
    1: '1',
    2: '2',
    3: '3',
    4: '4'#,
    #5: '5',
    #6: '6',
    #7: '7',
    #8: '8',
    #9: '9'
}

NUM_CLASSES = len(classes)
mode=0 # mode 1 = abt, mode 0 = smooth

if mode ==1: 
    name = 'model_digits_0_to_3_abt' 
elif mode ==0: 
    #name = 'model_digits_0_to_3_smooth'
    name = 'model_digits_0_to_4_smooth30_version69'
                                    
                                    # CHANGE NAME OF MODEL HERE
filename = name + ".hdf5"
model = load_model(filename, compile=False)
np.resize(model, NUM_CLASSES)

# 1) Setup bluetooth comms
PORT = 'COM10'
BAUDRATE = 115200

read = read_serial(PORT,BAUDRATE)
#read.init_comms()

i = 0
j = 0

     
x = 600
y = 520
img = np.zeros((x, y, 3),np.uint8)+255

while(True): # need serial comm activity boolean

    try: 
        ############################
        #   2) Read serial data    # 
        ############################
        data = record_data(read)

        ############################
        #   3) Pre-process data    # 
        ############################
    
        if mode==1:
            input_array_orig = array_to_abt_np(data)
        elif mode==0:
            input_array_orig = smooth_data(data)

        input_array = normalize(input_array_orig,axis=0)
        input_array = np.expand_dims(input_array_orig, axis=3)
        input_array = np.expand_dims(input_array, axis=0)
        
        
        ############################################
        # 4.1) Identify digit using trained model  #
        ############################################
        
        prediction = model.predict(input_array)
        predi = prediction[0].argmax()             # get index of greatest confidence
        digit = classes[predi]                     # identify digit
            
        print("PredictionL ", digit)

        ###############################################
        # 4.2) Display prediction confidence results  #
        ###############################################
        
        '''
        disp_x = 1000
        disp_y = 800
        data_display = np.zeros((disp_x, disp_y, 3), np.uint8)       
        positions = {                                            
            'digit': (15, 400), # hand pose text
            'fps': (15, 20), # fps counter
            'null_pos': (200, 200) # used as null point for mouse control
        }
        
        for k, pred in enumerate(prediction[0]):
            # Draw confidence bar for each digit
            barx = positions['digit'][0]
            bary = 60 + k*60
            bar_height = 20
            bar_length = int(400 * pred) + barx # calculate length of confidence bar

            # Make the most confidence prediction green
            if k == predi:
                colour = (0, 255, 0)
            else:
                colour = (0, 0, 255)

            cv2.putText(data_display, "{}: {}".format(classes[k], pred), (positions['digit'][0], 30 + k*60), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
            cv2.rectangle(data_display, (barx, bary), (bar_length, bary - bar_height), colour, -1, 1)
            cv2.putText(data_display, "digit: {}".format(digit), positions['digit'], cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
            
            cv2.imshow('data', data_display)
        '''
        
        #######################
        # 5) Display digits   #
        #######################


        cv2.putText(img,digit,(80+i,100+j), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 1, cv2.LINE_AA)  
        i += 20
        if i >= 360:
            j += 30
            i = 0
        if j > 420:
            i = 0
            j = 0
            img = np.zeros((x, y, 3),np.uint8)+255
        cv2.imshow('Notes',img)
        key = cv2.waitKey(1)

        
    except KeyboardInterrupt: 
        print('Exiting!')
        cv2.destroyAllWindows()
        read.close_comms()
        break