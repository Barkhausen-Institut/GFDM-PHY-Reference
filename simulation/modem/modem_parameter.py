import numpy as np
import commpy
from .util import FrozenBoundedClass


class ModemParameter(FrozenBoundedClass):
    def __init__(self):
        # common parameter
        self.K = 1024
        self.M = 1
        self.Ncp = 32
        self.Ncs = 32
        self.B = 1
        # modulator parameter
        self.modulator_type = "ofdm"  # "ofdm", "gfdm"

        # qam parameter
        self.qam_order = 16

        # synq parameter
        self.halfpreamble = np.fft.ifft(commpy.sequences.zcsequence(1, 64))
        self.halfpreamble = (self.halfpreamble) / max(abs(self.halfpreamble))

        # resource mapper
        self.Kset = np.concatenate([np.arange(16, 429), np.arange(600, 1000)])

        self.Mset = np.arange(self.M)
        self.pilot_pos = (self.Kset[0], self.Mset[0])
        self.pilots = 3 + 3j

        # coder
        self.coder_type = "identity"

        self.receiver_structure = ["sync", "channel_est_eq", "demodulator",
                                   "resource_demapper", "phase_corrector",
                                   "qam_demapper", "decoder"]
        self.transmitter_structure = ["encoder", "qam_mapper",
                                      "resource_mapper", "modulator",
                                      "add_cp_cs", "frame_multiplexer"]

        # channel estimation
        self.channel_estimation_type = "preamble"  # "preamble", "pilot"

        # windowing
        self.windowing_alpha = 1

        self._freeze()

    @property
    def fullpreamble(self):
        return np.concatenate([self.halfpreamble, self.halfpreamble])

    @property
    def Nhpreamble(self):
        return len(self.halfpreamble)

    @property
    def Npreamble(self):
        return len(self.halfpreamble) * 2

    @property
    def Npayload(self):
        return self.K * self. M

    @property
    def Npreamble_cp_cs(self):
        return self.Npreamble + self.Ncp + self.Ncs

    @property
    def Npayload_cp_cs(self):
        return self.Npayload + self.Ncp + self.Ncs


def get_ofdm_preamble_based():
    return ModemParameter()


def get_ofdm_pilot_based():
    p = ModemParameter()
    p.channel_estimation_type = "pilot"
    p.pilot_pos = np.arange(0, 1023, 16)
    p.pilots = 3 * commpy.sequences.zcsequence(1, len(p.pilot_pos))
    return p


def get_gfdm_preamble_based():
    p = ModemParameter()
    p.modulator_type = "gfdm"
    p.channel_estimation_type = "preamble"
    p.K = 64
    p.M = 16
    p.Kset = np.concatenate([np.arange(4, 28), np.arange(38, 60)])
    p.Mset = np.arange(1, 14)
    return p
