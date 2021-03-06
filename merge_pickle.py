'''
example call: python merge_pickle.py krish.p daniel.p aidan.p calvin.p max.p
'''
import sys
import pickle
import os
import numpy as np
from record_dataset import read_dataset, write_dataset

desired_pickle_jar = 'pickle_jar'
ultimate_dataset_name = 'all_datasets.p'

def main():
    pickles_to_combine = []
    for file in os.listdir(desired_pickle_jar):
        if file.endswith('.p'):
            pickles_to_combine.append(os.path.join(desired_pickle_jar,file))

    datasets = {'samples':np.array([]),'labels':np.array([])}

    for dataset in pickles_to_combine:

        if not os.path.isfile(dataset):
            raise FileNotFoundError('{} not found'.format(dataset))
            sys.exit(1)
        
        print('Reading {}'.format(dataset))
        data = read_dataset(dataset)
        print('{} samples: {}'.format(dataset, data['samples'].shape))
        print('{} labels: {}'.format(dataset, data['labels'].shape))

        assert (type(data)==dict), "{} is not a dict".format(data)

        samples = data['samples']
        labels = data['labels']

        datasets['samples'] = np.concatenate((datasets['samples'], samples))
        datasets['labels'] = np.concatenate((datasets['labels'], labels))

    print('samples_size: {}'.format(datasets['samples'].shape))
    print('labels_size: {}'.format(datasets['labels'].shape))

    write_dataset(ultimate_dataset_name, datasets)

main()

    




