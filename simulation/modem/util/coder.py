import numpy as np
from commpy.utilities import bitarray2dec, dec2bitarray


class Coder():
    def __init__(self, type_="identity"):
            self.type_ = type_
            self.byte_width = 8

    @property
    def code_rate(self):
        if self.type_ == "identity":
            return 1
        else:
            raise ValueError(f"unknown encode type: {self.type_}")

    def _check_data(self, data):
        if (max(data) > 2**self.byte_width) | (min(data) < 0):
            raise ValueError(f"Data should be in interval [0..{2**self.byte_width}]")

    def encode(self, data):
        self._check_data(data)
        if self.type_ == "identity":
            return self._identity_encode(data)
        else:
            raise ValueError(f"unknown encode type: {self.type_}")

    def decode(self, data):
        if self.type_ == "identity":
            return self._identity_decode(data)
        else:
            raise ValueError(f"unknown encode type: {self.type_}")

    def _identity_encode(self, data):
        return np.hstack([dec2bitarray(d, self.byte_width ) for d in data])

    def _identity_decode(self,data):
        data = np.reshape(data,(-1,self.byte_width))
        return np.hstack([bitarray2dec(d) for d in data])
