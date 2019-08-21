import numpy as np

class Equalizer():
    def __init__(self):
        self.channel_length = 32

    def equalize(self,freq_data,freq_response):
        self.Ndata = len(freq_data)
        self.freq_resp_interp = self._fft_interpolate(freq_response)
        return freq_data / self.freq_resp_interp

    def _fft_interpolate(self, freq_response):
        impulse_resp = np.fft.ifft(freq_response)
        impulse_resp_pad = np.concatenate([impulse_resp[0:self.channel_length],np.zeros(self.Ndata-2*self.channel_length), impulse_resp[-self.channel_length:]])
        return np.fft.fft(impulse_resp_pad)