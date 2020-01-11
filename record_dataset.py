#output random digit between 0-9

from random import randint
from random import seed
import os

seed()
dataset_filename = 'digits_data.p'
def generate_randint():
    while True:
        yield randint(0,9)

def read_dataset():
    
    if not os.path.isfile(dataset_filename):
        print('{} not found'.format(dataset_filename))
        with open(dataset_filename, 'wb+') as f:
            pickle.dump(f,{})
            
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
def record_training_data():
    '''
    tell user to write down digit
    record raw values
    perform feature extraction
    pickle the data
    '''
    digits_data = read_dataset()
    
    samples = digits_data['samples']
    labels = digits_data['labels']
    
    random_integer = generate_randint()
    
    for i in range(num_samples):
        integer = next(random_integer)
        print('Write {}'.format(integer))
        
        samples.append(input('Press any key'))
        labels.append(integer)
        
    digits_data['labels'] = labels
    digits_data['samples'] = samples
    
    print(digits_data)
    input('Press enter to approve of appending to training dataset')
    write_dataset(digits_data)