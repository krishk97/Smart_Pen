#output random digit between 0-9

from random import randint
from random import seed
from read_serial import read_serial
import pickle
import os

PORT = 'COM6'
BAUDRATE = 115200

seed()
dataset_filename = 'digits_data.p'

read = read_serial(PORT,BAUDRATE)

def generate_randint():
    while True:
        yield randint(0,9)

def read_dataset():
    
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

def write_dataset(dataset):
    with open(dataset_filename,'wb') as f:
        pickle.dump(dataset, f)


num_samples = 5

#function to record data to create dataset
def record_data():
    '''
    tell user to write down digit
    record raw values
    perform feature extraction
    pickle the data
    '''
    # initialize communication
    read.init_comms()

    digits_data = read_dataset()
    
    samples = digits_data['samples']
    labels = digits_data['labels']
    
    random_integer = generate_randint()
    for _ in range(num_samples):
        try:
            integer = next(random_integer)
            print('Write {}'.format(integer))            
            samples.append(read.read_data())
            labels.append(integer)
        except KeyboardInterrupt:
            print('Keyboard Interrupt')
            read.close_comms()
            break

    # done reading, close comms
    read.close_comms()

        
    digits_data['labels'] = np.array(labels)
    digits_data['samples'] = np.array(samples)
    
    print(digits_data)
    input('Press enter to approve of appending to dataset')
    write_dataset(digits_data)

if __name__ == '__main__':
    record_data()