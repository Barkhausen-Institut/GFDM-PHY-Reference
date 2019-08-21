import numpy as np
import numpy as np 
import matplotlib as plt 
from commpy.utilities import bitarray2dec, dec2bitarray
from itertools import product

class QamMapper():
    """ Creates a Quadrature Amplitude Modulation (QAM) Modem object.
    
    Modified code from commpy library
    """

    def _constellation_symbol(self, i):
        return (2*i[0]-1) + (2*i[1]-1)*(1j)

    def __init__(self, m):
        """ Creates a Quadrature Amplitude Modulation (QAM) Modem object.

        Parameters
        ----------
        m : int
            Size of the QAM constellation.

        """
        self.m = m
        sqrt_m = int(np.sqrt(self.m))
        self.num_bits_symbol = int(np.log2(self.m))
        gray_mapping = self.bin2gray(np.arange(self.m))
        mapping_array = np.arange(1, np.sqrt(self.m)+1) - (np.sqrt(self.m)/2)
        self.constellation = list(map(self._constellation_symbol,
                                 list(product(mapping_array, repeat=2))))
        self.constellation = np.reshape(self.constellation,(sqrt_m,sqrt_m))
        self.constellation = np.transpose(self.constellation)  
        self.constellation = list(zip(*self.constellation[::-1]))
        self.constellation = np.transpose(self.constellation)        
        self.constellation[1::2,::] = np.flip(self.constellation[1::2,::],1)
        self.constellation = np.reshape(self.constellation,m)
        sort_idx = np.argsort(gray_mapping)
        self.constellation = self.constellation[sort_idx]
       
    def modulate(self, input_bits):
        """ Modulate (map) an array of bits to constellation symbols.

        Parameters
        ----------
        input_bits : 1D ndarray of ints
            Inputs bits to be modulated (mapped).

        Returns
        -------
        baseband_symbols : 1D ndarray of complex floats
            Modulated complex symbols.

        """      
        mapfunc = np.vectorize(lambda i:
            self.constellation[bitarray2dec(input_bits[i:i+self.num_bits_symbol])])

        baseband_symbols = mapfunc(np.arange(0, len(input_bits), self.num_bits_symbol))
        return baseband_symbols

    def bin2gray(self,n):
        return n ^ (n >> 1)

    def demodulate(self, data):
        """ Demodulate (map) a set of constellation symbols to corresponding bits.

        Supports hard-decision demodulation only.

        Parameters
        ----------
        data : 1D ndarray of complex floats
            Input symbols to be demodulated.

        Returns
        -------
        demod_bits : 1D ndarray of ints
            Corresponding demodulated bits.

        """
        index_list = map(lambda i: np.argmin(abs(data[i] - self.constellation)), 
                             range(0, len(data)))
        demod_bits = np.hstack(list(map(lambda i: dec2bitarray(i, self.num_bits_symbol),
                                index_list)))
        return demod_bits

if __name__ == "__main__":
    pass
