import numpy as np

import record_dataset

num_samples = 8000
fake_samples = np.random.random(size = (num_samples,300,6))*255
fake_labels = np.random.randint(10, size=(num_samples))

fake_dataset = {}
fake_dataset['samples'] = fake_samples
fake_dataset['labels'] = fake_labels

record_dataset.write_dataset(fake_dataset)
