import scipy.signal
import numpy as np
def find_peaks(x, max_num = -1, height = None, distance = None):
    '''  Find peaks positions and their heights in 1-d array of real data. (Based on `scipy.signal.find_peaks`)
    :param x: 1-d array of real data
    :param max_num: `optional` defines maximum number of peaks to return. Ignored not positive.
    :param height: `optional`  Required height of peaks. If `height` is not defined, than it is calculated as `height = np.mean(x) + 2*np.std(x)`
    :param distance: `optional` Required minimal horizontal distance ( = 1) in samples between  
    neighbouring peaks. See: `scipy.signal.find_peaks`
    :returns: tuple of arrays with peaks positions and their heights. Arrays are sorted regarding to peaks heights'''
    
    if not height:
        height = np.mean(x) + 2*np.std(x)
    
    locs, props = scipy.signal.find_peaks( x,
                                        height = height,
                                        distance = distance,
                                        )
    locs = np.array(locs)                                    
    heights = np.array(props['peak_heights'])
    sorted_idx = np.flip(heights.argsort(),axis = 0)
    locs = locs[sorted_idx]
    heights = heights[sorted_idx]
    if max_num > 0:
        if len(locs) > max_num:
            return (locs[0:max_num], heights[0:max_num])
        else :
            return (locs, heights)
    else:
        return (locs, heights)

def shift(arr, num, mode = 'same', fill_value = 0):
    ''' Shifts 1D vector rigth if shift > 0, and left if shift < 0'''
    if mode == "same":
        # from: https://stackoverflow.com/questions/30399534/shift-elements-in-a-numpy-array
        result = np.empty_like(arr)
        if num > 0:
            result[:num] = fill_value
            result[num:] = arr[:-num]
        elif num < 0:
            result[num:] = fill_value
            result[:num] = arr[-num:]
        else:
            result = arr
        return result
    else:
        raise ValueError(f"mode \"{mode}\" is not implemented")

def norm_complex(data):
    return data /max( max(data.real),max(data.imag) )