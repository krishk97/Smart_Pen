## Input is a Pandas table of ax, ay, az, gx, gy, gz over time
## Output is a np table of ax, ay, az, gx, gy, gz and selected features
import numpy as np
import pandas as pd
from scipy import stats, fft, fftpack
import serial
import ast
import signal
import atexit
from array_to_abt_np import smooth_data
'''
Class that handles comms with smart pen
'''
class read_serial: 
    def __init__(self, port_name, baudrate):
            self.port_name = port_name
            self.baudrate = baudrate
            print('Connected to port...')
            self.init_comms()
            
    def init_comms(self): 
        self.ser = serial.Serial(self.port_name)
        self.ser.baudrate = self.baudrate
        print('Initialized connection...')
    
    def read_data(self):
        self.receive_data = False
        data = []
        # begin reading data from pen
        while True: 
            line = self.ser.readline()[:-2] # Strip Line feed and carriage return
            line = line.decode("utf-8") # Decode UTF-8 Bytes

            if (line == '{'):
                self.receive_data = True
                    
            elif (line == '}'):
                #self.print_data(data)
                self.receive_data = False
                #self.close_comms()
                return data

            elif (self.receive_data):
                try:
                    data.append(ast.literal_eval(line))
                except SyntaxError:
                    pass
    
                                    
    def print_data(self,data):
            print('Sample Received: \n')
            data = np.asarray(data)
            print(data)
                  
    def close_comms(self):
            self.ser.close()
            print('Closed connection to port...')

# example code:
def main():
    pass

if __name__ == '__main__':
    main()			
    
    PORT = 'COM10'
    BAUDRATE = 115200

    read = read_serial(PORT,BAUDRATE) # set up serial communication with pen 
    # read.init_comms() # initialize comms

    # begin collecting data until KeyboardInterrupt
    while True: 
        try: 
            data = read.read_data()
            print('smoothed data: \n', smooth_data(data))
        except KeyboardInterrupt: 
            read.close_comms()
            break