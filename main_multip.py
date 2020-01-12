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
import pickle
import time
from multiprocessing import Process, SimpleQueue

import cv2
import numpy as np
import pandas as pd
import tensorflow as tf
from keras.models import Sequential, load_model, model_from_json
from matplotlib import pyplot as plt
from scipy import fft, fftpack, stats

from array_to_abt_np import array_to_abt_np
from read_serial import read_serial
from record_dataset import record_data

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
mode = 0 #0 for dense NN, 1 for conv2d 
name = 'model_digits_1'                                 # CHANGE NAME OF MODEL HERE

if mode:
    name = name + 'conv2d'
else:
    name = name + 'dense'

filename = name + ".hdf5"
model = load_model(filename, compile=False)
np.resize(model, 10)

PORT = 'COM6'
BAUDRATE = 115200

read = read_serial(PORT,BAUDRATE)


def read_data(stream_queue):
    #letter_gen = fake_data_letter()
    while True:
        letter = read.read_data()
        #letter = next(letter_gen)
        #print(letter.shape)

        abt = array_to_abt_np(letter)
        #print(abt.shape)
        #need to make the input conv2d a 4d array (1, 10, 6, 1)
        #if inputted into dense NN, input (1, 10, 6)
        if mode:
            abt = np.expand_dims(abt, axis=-1)

        sample = np.expand_dims(abt, axis = 0)
        print(sample.shape)
        stream_queue.put(sample)
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
            print('predicted digit: {}'.format(digit))

            #display_digits(digit)
def fake_data_letter():
    while True:
        time.sleep(np.random.random(1)*3)
        fake_samples = np.random.random(size = (300,6))*255
        yield fake_samples

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

    p_read = Process(target=read_data, args=(stream_queue,))
    p_predict = Process(target=feed_into_nn, args = (stream_queue,))

    try:
        p_read.start()
        p_predict.start()
    except KeyboardInterrupt:
        p_read.join()
        p_predict.join()
        cv2.destroyAllWindows()
        read.close_comms()

if __name__ == "__main__":
    main()