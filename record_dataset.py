#output random digit between 0-9
from datetime import datetime
from random import randint
from random import seed
from read_serial import read_serial
import pickle
import os
import numpy as np

MIN_SIZE = 10

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
    
    counter = 0 
    while counter < num_samples: 
        try: 
            integer = next(random_integer)
            print('Write {}'.format(integer))
            data = read_serial.read_data()
            
            if len(data) < MIN_SIZE:  
                read_serial.print_data(data)           
                print('Not enough data, please try again...')
            else:     
                read_serial.print_data(data)
                samples.append(data)
                labels.append(integer)
                counter = counter+1
    
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
            if len(data) < MIN_SIZE: 
                read_serial.print_data(data)
                print('Not enough data, please try again...') 
            else: 
                read_serial.print_data(data)
                print('Data successfully collected...')
                return data

        except KeyboardInterrupt:
            print('Keyboard Interrupt')
            read_serial.close_comms()
            break

if __name__ == '__main__':
<<<<<<< HEAD
    main()
    PORT = 'COM12'
    BAUDRATE = 115200
    seed(123)
    NUM_SAMPLES = None    
    while type(NUM_SAMPLES) is not int:
        try:
            NUM_SAMPLES = input('Enter number of samples to test on: ')
            NUM_SAMPLES = int(NUM_SAMPLES)
            print("You entered: %d" % NUM_SAMPLES)
        except ValueError:
            print("%s is not an integer.\n" % NUM_SAMPLES)
=======
    PORT = 'COM6'
    BAUDRATE = 115200
    NUM_SAMPLES = 100
    seed(datetime.now())
    dataset_filename = 'digits_data.p'
>>>>>>> 57b0ecf5ab6f911e017c340879b442437a16764c

    dataset_filename = str(input('dataset filename: ')) + '.p'
    
    read = read_serial(PORT,BAUDRATE)

    record_training_data(dataset_filename,read,NUM_SAMPLES)