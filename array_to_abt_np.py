# Input is a Pandas table of ax, ay, az, gx, gy, gz over time
## Output is a np table of ax, ay, az, gx, gy, gz and selected features
import numpy as np
import pandas as pd
from scipy import stats, fft, fftpack

ARRAY_LENGTH = 30

def array_to_abt_np(dataframe):
    '''
    
    '''
    sensor_data = np.array(dataframe)
    #print(sensor_data.shape)
    #want to see (# of samples,6)
    
    means = np.mean(sensor_data, axis=0)
    ranges = np.ptp(sensor_data, axis = 0)
    stds = np.std(sensor_data, axis=0)
    moment_3 = stats.moment(sensor_data, moment=3, axis=0)
    
    dcts = fftpack.dct(sensor_data, axis=0)
    sorted_dcts = np.sort(dcts, axis=0)
    max_dcts = sorted_dcts[0]
    second_max_dcts = sorted_dcts[1]
    third_max_dcts = sorted_dcts[2]

    ffts = fft(sensor_data, axis=0)
    sorted_ffts = np.sort(ffts,axis=0)
    max_ffts = sorted_ffts[0]
    second_max_ffts = sorted_ffts[1]
    third_max_ffts = sorted_ffts[2]
    
    to_be_stacked = (means, ranges, stds, moment_3, max_dcts,
                    second_max_dcts, third_max_dcts,
                    max_ffts, second_max_ffts, third_max_ffts)
    
    abt_table = np.vstack(to_be_stacked)
    
    return abt_table

def array_to_wang2012(dataframe): 
    sensor_data = np.array(dataframe)
    # smooth/interpolate

    # mean,std,var,iqr,corr,mad,rms,energy
    means = np.mean(sensor_data, axis=0)
    stds = np.std(sensor_data, axis=0)
    iqrs = np.percentile(sensor_data,75,axis=0) - np.percentile(sensor_data,25,axis=0)
    
def smooth_data(dataframe): 
    sensor_data = np.array(dataframe)
    return np.resize(sensor_data,(ARRAY_LENGTH,6))
    


