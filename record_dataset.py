#output random digit between 0-9
from datetime import datetime
from random import randint
from random import seed
from read_serial import read_serial
import pickle
import os
import numpy as np

def generate_randint():
    while True:
        yield randint(0,9)

def read_dataset(dataset_filename):
    
    if not os.path.isfile(dataset_filename):
        print('{} not found'.format(dataset_filename))
        with open(dataset_filename, 'wb') as f:
            pickle.dump({'samples':[],'labels':[]},f)
            
    with open(dataset_filename,'rb') as f:
        try:
            digits_data = pickle.load(f)
        except EOFError:
            print('Empty file')
            digits_data = {'samples':[],'labels':[]}
            
    return digits_data

def write_dataset(dataset_filename, dataset):
    with open(dataset_filename,'wb') as f:
        pickle.dump(dataset, f)

# function to record data to create training dataset
def record_training_data(dataset_filename,read_serial,num_samples):
    '''
    tell user to write down digit
    record raw values
    perform feature extraction
    pickle the data
    '''
    # initialize communication
    read_serial.init_comms()

    digits_data = read_dataset(dataset_filename)
    
    samples = digits_data['samples']
    labels = digits_data['labels']
    
    random_integer = generate_randint()

    for _ in range(num_samples):
        try:
            integer = next(random_integer)
            print('Write {}'.format(integer))            
            samples.append(read_serial.read_data())
            labels.append(integer)
        except KeyboardInterrupt:
            print('Keyboard Interrupt')
            read_serial.close_comms()
            break

    # done reading, close comms
    read_serial.close_comms()

        
    digits_data['labels'] = np.array(labels)
    digits_data['samples'] = np.array(samples)
    
    print(digits_data)
    input('Press enter to approve of appending to dataset')
    write_dataset(dataset_filename, digits_data)

def record_data(read_serial): 
    '''
    records data and spits out np.array
    '''
    # initialize communication
    read_serial.init_comms()

    while True: # need to update with serial check
        try:            
            data = read_serial.read_data()
            print('Data successfully collected')
            return data

        except KeyboardInterrupt:
            print('Keyboard Interrupt')
            read_serial.close_comms()
            break

if __name__ == '__main__':
    PORT = 'COM6'
    BAUDRATE = 115200
    NUM_SAMPLES = 100
    seed(datetime.now())
    dataset_filename = 'digits_data.p'

    read = read_serial(PORT,BAUDRATE)
    record_training_data(dataset_filename,read,NUM_SAMPLES)