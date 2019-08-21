import numpy as np 

class ResourceMapper():
    def __init__(self, K, M, Kset = [0], Mset = [0], pilot_pos = []):
        self.K = K
        self.M = M
        self.Kset = Kset
        self.Mset = Mset
        self.pilot_pos = pilot_pos

    @property
    def _Kset(self):
        return  np.delete(   self.Kset, 
                            np.where((np.array(self.Kset)>=self.K)|(np.array(self.Kset)<0))
                            )

    @property
    def _Mset(self):
        return np.delete(   self.Mset, 
                            np.where((np.array(self.Mset)>=self.M)|(np.array(self.Mset)<0))
                            )

    @property
    def resource_map(self):
        r_map = np.full((self.K,self.M),'-')
        idx = np.array(np.meshgrid(self._Kset, self._Mset)).T.reshape(-1,2)
        r_map[(idx[:,0],idx[:,1])] = 'D'
        r_map[self.pilot_pos] = 'P'
        return r_map
    
    @property
    def nof_pilots_per_block(self):
        return (self.resource_map == 'P').sum()
    
    @property
    def nof_symbols_per_block(self):
        return (self.resource_map == 'D').sum()
        
    def mapper(self, data, pilots):
        mapped_res = np.zeros((self.K,self.M),dtype=type(data[0]))
        mapped_res[np.where(self.resource_map=='D')] = data
        mapped_res[np.where(self.resource_map=='P')] = pilots

        return mapped_res

    def demapper(self, mapped_data):
        data   = mapped_data[np.where(self.resource_map=='D')]
        pilots = mapped_data[np.where(self.resource_map=='P')]
        return (data, pilots)


    
    