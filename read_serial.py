#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 01:10:43 2020

@author: aidancookson
"""
import serial
import ast
import signal
import atexit
import numpy as np


def init_comms():
    ser = serial.Serial('/dev/tty.wchusbserial1420')
    ser.baudrate = 115200
    
    receive_data = False
    data = []
    
    while True:
        
        line = ser.readline()[:-2] # Strip Line feed and carriage return
        line = line.decode("utf-8") # Decode UTF-8 Bytes
        
        if (line == '{'):
            receive_data = True
        elif (line == '}'):
            print_data(data)
            receive_data = False
            data = []
        elif (receive_data):
                try:
                    data.append(ast.literal_eval(line))
                except SyntaxError:
                    pass

def print_data(data):
    print("Sample Received: ")
    data = np.asarray(data)
    print (data)

def handle_exit():
    print('Closed Serial Port')
    #ser.close()

if __name__ == "__main__":
   # atexit.register(handle_exit)
    #signal.signal(signal.SIGTERM, handle_exit)
    #signal.signal(signal.SIGINT, handle_exit)
    init_comms()