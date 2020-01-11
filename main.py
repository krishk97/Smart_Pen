import numpy as np
import cv2
import pickle
import pandas as pd
from scipy import stats, fft, fftpack
from read_serial import read_serial
from matplotlib import pyplot as plt

import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model, model_from_json

PORT = 'COM6'
BAUDRATE = 115200


classes = {
    0: '0',
    1: '1',
    2: '2',
    3: '3',
    4: '4',
    5: '5',
    6: '6',
    7: '7',
    8: '8',
    9: '9'
}


name = 'model_digits_1'                                 # CHANGE NAME OF MODEL HERE
filename = name + ".hdf5"
model = load_model(filename, compile=False)
np.resize(model, 10)

read = read_serial(PORT,BAUDRATE)


while(True):
    
    ############################
    ## Read real-time writing ##
    ############################
    
    
    # Here, we want to 1) Read from Bluetooth serial, 2) pd-to-abt-np. 
    # Input_array should be array of features        
    # 1) Setup read from bluetooth 
    read.init_comms()
    read.read_data()
    input_array =   ########################################## ENTER YOUR INPUT HERE ##################################
    
    
    
    ########################################
    ## Identify digit using trained model ##
    ########################################
    
    prediction = model.predict(input_array)
    predi = prediction[0].argmax()             # get index of greatest confidence
    digit = classes[predi]                     # identify digit
    
    
    
    ###########################################
    ## Display prediction confidence results ##
    ###########################################
    
    disp_x = 800
    disp_y = 800
    data_display = np.zeros((disp_x, disp_y, 3), np.uint8)       
    positions = {                                            
        'digit': (15, 400), # hand pose text
        'fps': (15, 20), # fps counter
        'null_pos': (200, 200) # used as null point for mouse control
    }
    
    for i, pred in enumerate(prediction[0]):
        # Draw confidence bar for each gesture
        barx = positions['hand_pose'][0]
        bary = 60 + i*60
        bar_height = 20
        bar_length = int(400 * pred) + barx # calculate length of confidence bar

        # Make the most confidence prediction green
        if i == predi:
            colour = (0, 255, 0)
        else:
            colour = (0, 0, 255)

        cv2.putText(data_display, "{}: {}".format(classes[i], pred), (positions['digit'][0], 30 + i*60), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
        cv2.rectangle(data_display, (barx, bary), (bar_length, bary - bar_height), colour, -1, 1)
        cv2.putText(data_display, "digit: {}".format(gesture), positions['digit'], cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
        
        cv2.imshow('data', data_display)
    
    
    
    ####################
    ## Display digits ##
    ####################
    
    x = 600
    y = 520
    img = np.zeros((x, y, 3),np.uint8)+255

    i = 0
    j = 0

    cv2.imshow('Notes',img)
    k = cv2.waitKey(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img,chr(k),(80+i,100+j), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 1, cv2.LINE_AA) 
    i += 20
    if i >= 360:
        j += 30
        i = 0
            
    if k == 27:        # press 'ESC' to quit
        break

        
cap.release()
cv2.destroyAllWindows()