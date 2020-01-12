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
from read_dataset import record_data               
from matplotlib import pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model, model_from_json

# 0) Load network model
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

# 1) Setup bluetooth comms
PORT = 'COM6'
BAUDRATE = 115200

read = read_serial(PORT,BAUDRATE)
read.init_comms()

while(True): # need serial comm activity boolean
    
    ############################
    #   2) Read serial data    # 
    ############################
    read.record_data()





    ############################
    #   3) Pre-process data    # 
    ############################
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