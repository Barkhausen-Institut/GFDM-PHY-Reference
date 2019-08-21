import numpy as np

def add_cp(data, Ncp):
    if Ncp:
        return np.concatenate([data[-Ncp:],data])
    else: 
        return data

def remove_cp(data, Ncp):
    return data[Ncp:]

def add_cs(data, Ncs):
    return np.concatenate([data,data[:Ncs]])

def remove_cs(data, Ncs):
    if Ncs:
        return data[:-Ncs]
    else: 
        return data 

def add_cp_cs(data, Ncp, Ncs):
    if Ncp > 0 :
        return np.concatenate([data[-Ncp:],data,data[:Ncs]])
    else :
        return add_cs(data, Ncs)