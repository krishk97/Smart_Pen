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
from record_dataset import record_data               
from matplotlib import pyplot as plt
import tensorflow as tf
from multiprocessing import SimpleQueue, Process
from keras.models import Sequential, load_model, model_from_json
from array_to_abt_np import array_to_abt_np
import time
from read_serial import read_serial


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

PORT = 'COM6'
BAUDRATE = 115200

read = read_serial(PORT,BAUDRATE)


def read_data(stream_queue):
    while True:
        letter = read.read_data()
        abt = array_to_abt_np(letter)
        stream_queue.put(abt)
        time.sleep(0.01)

def feed_into_nn(stream_queue):
    while True:
        if stream_queue.empty():
            time.sleep(0.01)
            continue
        else:
            input_array = stream_queue.get()
            prediction = model.predict(input_array)
            predi = prediction[0].argmax()             # get index of greatest confidence
            digit = classes[predi]  # identify digit
            #display_digits(digit)

def display_digits(digit):
    x = 600
    y = 520
    
    img = np.zeros((x, y, 3),np.uint8)+255

    i = 0
    j = 0

    cv2.imshow('Notes',img)
    k=digit
    #k = cv2.waitKey(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img,chr(k),(80+i,100+j), font, 1, (0,0,0), 1, cv2.LINE_AA) 
    i += 20
    if i >= 360:
        j += 30
        i = 0
    if j>=420:
        j=0
        i=0
        img = np.zeros((x, y, 3),np.uint8)+255

def main():
    # 1) Setup bluetooth comms

    read.init_comms()

    #create queue of streaming data
    stream_queue = SimpleQueue()

    p_read = Process(target=read_data, args=stream_queue)
    p_predict = Process(target=feed_into_nn, args = stream_queue)

    try:
        p_read.start()
        p_predict.start()
    except KeyboardInterrupt:
        p_read.join()
        p_predict.join()
        cv2.destroyAllWindows()
        read.close_comms()


        
