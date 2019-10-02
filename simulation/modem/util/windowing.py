import numpy as np


class Windowing:
    def __init__(self, Ncp, Ncs, alpha):
        self.alpha = alpha
        self.Ncp = Ncp
        self.Ncs = Ncs
        raise_window_len = int(self.Ncp * self.alpha)
        fall_window_len = int(self.Ncs * self.alpha)
        self.raise_window = np.blackman(
            raise_window_len * 2)[:raise_window_len]
        self.fall_window = np.blackman(fall_window_len * 2)[-fall_window_len:]

    def apply_window(self, samples):
        window = np.concatenate(
            [self.raise_window, np.ones(len(samples) - len(self.raise_window) - len(self.fall_window)), self.fall_window])
        return samples * window
