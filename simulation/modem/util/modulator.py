
import sdr_utils
import numpy as np
from .common import FrozenBoundedClass 
from .pulse_shaping import get_rc_filter, get_zf_receiver_filter
def norm_complex(data):
    return data /max( max(data.real),max(data.imag) )

class Modulator(FrozenBoundedClass):
    def __init__(self, K = 1024 ,M = 1, type_ = "ofdm"):
        self.type_ = type_ 
        self.K = K
        self.M = M
        self.g_tx = get_rc_filter(K,M)[0]

    def modulate(self, data):
        if self.type_ in ("ofdm"):
            return self._modulate_ofdm(data)
        elif self.type_ in ("gfdm_td" , "gfdm_fd", "gfdm"):
            return self._modulate_gfdm_r2(data)
        else:
            raise ValueError(f"Unknown modulator type: {self.type_}")

    def demodulate(self, data):
        if self.type_ in ("ofdm" , "OFDM"):
            return self._demodulate_ofdm(data)
        elif self.type_ in ("gfdm_fd", "gfdm"):
            return self._demodulate_gfdm_r2_fd(data)
        elif self.type_ in ("gfdm_td"):
            return self._demodulate_gfdm_r2_td(data)
        else:
            raise ValueError(f"Unknown modulator type: {self.type_}") 
    
    def _modulate_ofdm(self,data):
        return norm_complex(np.fft.ifft(data))

    def _demodulate_ofdm(self,data):
        return np.fft.fft(data)

    def _modulate_gfdm_r2(self, data):
        D = np.transpose(data)
        D = np.fft.ifft(D, axis = 1)
        D = np.fft.fft(D, axis = 0)
        D = D * self._get_gfdm_window_td()
        x = np.fft.ifft(D, axis = 0).reshape(self.K*self.M)
        return x

    def _demodulate_gfdm_r2_td(self,data):
        X = np.reshape(data, (self.M,self.K))
        X = np.fft.fft(X, axis = 0) / self._get_gfdm_window_td() 
        X = np.fft.ifft(X, axis = 0)
        d = np.fft.fft(X, axis = 1).transpose()
        return d

    def _demodulate_gfdm_r2_fd(self, data):
        X = np.reshape(data, (self.K, self.M))
        X = np.fft.ifft(X, axis=0) / self._get_gfdm_window_fd()
        X = np.fft.fft(X, axis=0)
        X = np.fft.ifft(X, axis=1)
        return X

    def _get_gfdm_window_td(self):
        g = np.reshape(self.g_tx, (self.M,self.K))
        G = np.fft.fft(g, axis=0)
        return G

    def _get_gfdm_window_fd(self):
        g = np.reshape(np.fft.fft(self.g_tx), (self.K, self.M))
        G = np.fft.ifft(g, axis = 0)
        return G

    # def _modulate_gfdm(self,data):
    #     K, M = self.K, self.M
    #     g = self.g_tx
    #     N = K * M

    #     B = np.fft.ifft(data, axis=0) * K

    #     signal = np.zeros((N, M), dtype=complex)
    #     for m in range(M):
    #         b = np.tile(B[:,m], M)
    #         signal[:, m] = b * np.roll(g, m*K)
    #     return signal.sum(axis=1)

  