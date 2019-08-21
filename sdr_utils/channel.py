import commpy

import numpy as np
 
# TODO: make this code importable:
class _frozen_bounded_class(object): 
    # TODO: This code is copied from another project, so it should be imported
    __is_frozen = False
    def __setattr__(self, key, value):
        if hasattr(self.__class__, "bounds"):
            bounds = getattr(self.__class__,"bounds")
            if key in bounds:
                if value > bounds[key][1] or value < bounds[key][0]:
                    raise ValueError (str(value)+" is out of bounds: ("+
                        str(bounds[key][0])+", "+str(bounds[key][1])+")" )
        if self.__is_frozen and not hasattr(self, key):
            raise TypeError( "%r is a frozen class" % self )
        object.__setattr__(self, key, value)

    def _freeze(self):
        self.__is_frozen = True


class Channel(_frozen_bounded_class):
    def __init__(self):
        self.impulse_response = []
        self.last_impulse_response = None
        test_impulse_response = np.array([1+1j,0,0,0,0,1+1j,0,0,0,0,1+1j,0,0,0,0,1+1j,0,0,0,0])
        test_impulse_response *= np.exp(np.linspace(0,-3,len(test_impulse_response)))
        test_impulse_response /= np.linalg.norm(test_impulse_response) 
        self.test_impulse_response = test_impulse_response
        self._freeze()
    def awgn(self, data, snr_db):
        """
        Addditive White Gaussian Noise (AWGN) Channel.

        :param data: 1D ndarray of complex floats
            Input signal to the channel.

        :param snr_dB:  Output SNR required in dB.
        :type snr_dB: float

        :return  output_signal: 1D ndarray of floats. Output signal from the channel with the specified SNR.
        """
        return commpy.channels.awgn(data, snr_db)

    def multipath(self, data, taps = 8, distrib = "exp", snr_db = None):
        """
        Multipath channel with specified impulse_response. Thre are two ways to specify the impulse_response. 
        First option: define `taps` and `distrib` -> the impulse_response will be generated automatically.
        Second optinon: define `Channel.impulse_response`, befor using Channel.multipath. If `Channel.impulse_response` is defined,
        it is used for channel.

        Last used impulse_response is stored in `Channel.last_impulse_response`  

        :param data: 1D ndarray of complex floats
            Input signal to the channel.
        
        :param typs: Number of channel taps, default: 8

        :param distrib: Impulse response distribution.\"exp\" - exponentional, \"uniform\" - uniform
            default:  \"exp\"

        :param snr_dB:  If defeined, the singnal will be additinaly passed through the AWGN channel with SNR specified in dB.
        :type snr_dB: float

        :return  output_signal: 1D ndarray of floats. Output signal from the channel with the specified SNR.
        """
        if len(self.impulse_response) > 0:
            self.last_impulse_response = self.impulse_response
        else:
            self.last_impulse_response = 1/2*(np.random.randn((taps)) + 1j*np.random.randn((taps)))
            if distrib == "exp" : self.last_impulse_response *= np.exp(np.linspace(0,-3,taps)) 
            self.last_impulse_response = self.last_impulse_response/np.linalg.norm(self.last_impulse_response)      
        
        if snr_db:
            return self.awgn(np.convolve(self.last_impulse_response,data, mode= 'full'), snr_db)
        else:
            return np.convolve(self.last_impulse_response, data, mode= 'full')

