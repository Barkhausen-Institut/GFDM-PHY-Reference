import logging
import numpy as np

from .util.modulator import norm_complex
from .util import (QamMapper, Coder, add_cp_cs, Windowing, FrameMultiplexer,
                   add_cp, remove_cp, add_cs, remove_cs, Modulator,
                   synchronization, ChannelEstimation, Equalizer,
                   ResourceMapper)

# logging.basicConfig(format='%(levelname)s:%(message)s',level=logging.DEBUG)


class Modem:
    def __init__(self, param):
        self.param = param
        self._qam4_mapper = QamMapper(4)
        self._qam16_mapper = QamMapper(16)
        self._qam64_mapper = QamMapper(64)
        self.intern_data = {}
        self.save_intern_data = False

    def _run_chain(self, data, structure):
        data_in = data
        for block in structure:
            if np.size(data_in) > 0:
                logging.debug(f"BLOCK : {block}; shape:{np.shape(data_in)}")
                data_out = getattr(self, block)(data_in)
            data_in = data_out
            if self.save_intern_data:
                self.intern_data[block] = data_out
        return data_out

    def transmitter(self, data=[]):
        if len(data) == 0:
            data = np.random.randint(0, 255, self.bytes_per_frame)
        if self.save_intern_data:
            self.intern_data["bytes_in"] = data
        # TODO else check size and reshape
        return self._run_chain(data, self.param.transmitter_structure)

    def receiver(self, data):
        if self.save_intern_data:
            self.intern_data["receiver"] = data
        return self._run_chain(data, self.param.receiver_structure)

    # ------------------PROPERTIES-------------------------#
    @property
    def bytes_per_frame(self):
        # payload bytes per frame
        if self.bits_per_frame % 8 == 0:
            return self.bits_per_frame // 8
        else:
            raise ValueError(f"invalid number of bits: {self.bits_per_frame}")

    @property
    def bits_per_frame(self):
        # payload bits ber frame
        return int(self.symbols_per_frame * np.log2(self.param.qam_order) /
                   self._coder.code_rate)

    @property
    def symbols_per_frame(self):
        # encoded symbols in the frame
        return self._resource_mapper.nof_symbols_per_block * self.param.B

    #-------------------- CODER ---------------------------#
    @property
    def _coder(self):
        return Coder(type_=self.param.coder_type)

    def encoder(self, data):
        return self._coder.encode(data)

    def decoder(self, data):
        return self._coder.decode(data)

    #--------------- FRAME MULTIPLEXER ----------------------#
    @property
    def _fullpreamble(self):
        return np.concatenate((self.param.halfpreamble,
                               self.param.halfpreamble))

    @property
    def _fullpreamble_cpcs(self):
        return add_cp_cs(self._fullpreamble, self.param.Ncp, self.param.Ncs)

    @property
    def _windowing(self):
        return Windowing(self.param.Ncp, self.param.Ncs,
                         self.param.windowing_alpha)

    def frame_multiplexer(self, data):
        fmux = FrameMultiplexer()
        return fmux.multiplex_frame(
            self._windowing.apply_window(data),
            self._windowing.apply_window(self._fullpreamble_cpcs)
        )

    #--------------- CYCLIC PREFIX/SUFFIX -------------------#
    def add_cp(self, data):
        return add_cp(data, self.param.Ncp)

    def remove_cp(self, data):
        return remove_cp(data, self.param.Ncp)

    def add_cs(self, data):
        return add_cs(data, self.param.Ncs)

    def remove_cs(self, data):
        return remove_cs(data, self.param.Ncs)

    def add_cp_cs(self, data):
        return np.concatenate(
            [add_cp_cs(data[b], self.param.Ncp, self.param.Ncs)
             for b in range(self.param.B)]
        )

    #--------------- QAM Mapper-Demepper -------------------#
    def qam_mapper(self, data):
        return getattr(self, f"_qam{self.param.qam_order}_mapper").modulate(data)

    def qam_demapper(self, data):
        return getattr(self, f"_qam{self.param.qam_order}_mapper").demodulate(data)

    # ----------------------- MODULATOR ----------------------#
    @property
    def _modulator(self):
        return Modulator(self.param.K, self.param.M, self.param.modulator_type)

    def modulator(self, data):
        data_out = np.empty((self.param.B, self.param.K *
                             self.param.M), dtype=data.dtype)
        for b in range(self.param.B):
            if self.param.modulator_type in ("OFDM", "ofdm"):
                data_out[b] = norm_complex(
                    self._modulator.modulate(data[b, :, 0]))
            elif self.param.modulator_type in ("GFDM", "gfdm"):
                data_out[b] = norm_complex(
                    self._modulator.modulate(data[b]))
        return data_out

    def demodulator(self, data):
        '''
        Paremeter
        ---------
        data: shape = (B, Npayload)

        Return
        ------
        demodulated_sympols: shape = (B,K,M)
        '''
        if self.param.modulator_type in ("ODFM", "ofdm"):
            # skip demodulation since fft alrady perfomed by equalization
            # only resize
            return np.resize(data, (self.param.B, self.param.K, self.param.M))
        elif self.param.modulator_type in ("GDFM", "gfdm"):
            return np.array([self._modulator.demodulate(data[b]) for b in range(self.param.B)])

    # ------------------- SYNC   ------------------------#
    @property
    def _synchronization(self):
        return synchronization(self.param)

    def sync(self, data):
        '''
        Return
        ------
        (payload, preamble) : shape = ((B,Npayload),Npreamble)
        '''

        preamble_starts = self._synchronization.detect_preamble_starts(data)
        if len(preamble_starts) == 0:
            return np.array([])
        # take only first detected frame (discard other)
        preamble_start = preamble_starts[0]
        if self.save_intern_data:
            self.intern_data["preamble_start"] = preamble_start
        Npre_cp_cs = self.param.Ncp + self.param.Ncs + self.param.Npreamble
        Npay_cp_cs = self.param.Ncp + self.param.Ncs + self.param.Npayload
        try:
            preamble = data[preamble_start:preamble_start +
                            self.param.Npreamble]
            idx = np.arange(self.param.Npayload)
            payload = np.vstack(
                [data[(preamble_start + Npre_cp_cs + Npay_cp_cs * b) + idx]
                 for b in range(self.param.B)]
            )
            return (payload, preamble)
        except IndexError:
            return np.array([])

    #---------------Channel Estimation & Equalization-----------#
    def channel_est_eq(self, data):
        if self.param.channel_estimation_type == "preamble":
            return self._channel_est_eq_preamble(data)
        elif self.param.channel_estimation_type == "pilot":
            return self._channel_est_eq_pilot(data)

    def _channel_est_eq_preamble(self, data):
        '''
        Parameter
        ---------
        data = (received_payload, received_preamble)
            received_payload: shape = (B, Npayload)
            received_preamble: shape = Npreamble

        Return
        ------
        equalized_payload_freq: shape = (B, Npayload)
        '''
        received_payload, received_preamble = data[0], data[1]
        estimator = ChannelEstimation()
        freq_response = estimator.estimate_channel_form_preamble(
            received_preamble, self.param.halfpreamble)
        equalizer = Equalizer()

        data_out = np.vstack(
            [equalizer.equalize(np.fft.fft(received_payload[b]), freq_response)
             for b in range(self.param.B)]
        )
        self.intern_data["estimated_freq_resp"] = equalizer.freq_resp_interp
        return data_out

    def _channel_est_eq_pilot(self, data):
        payload = np.fft.fft(data[0], axis=1)
        demapped_data = self.resource_demapper(
            np.resize(payload, (self.param.B, self.param.K, self.param.M)))
        estimator = ChannelEstimation()
        equalizer = Equalizer()
        r = [equalizer.equalize(payload[b],
                                estimator.estimate_channel_from_pilots(
                                    demapped_data[b][1], self.param.pilots))
             for b in range(self.param.B)]
        return np.vstack(r)

    #--------------------- RESOURCE MAPPER ---------------------#
    @property
    def _resource_mapper(self):
        return ResourceMapper(self.param.K, self.param.M, self.param.Kset,
                              self.param.Mset, self.param.pilot_pos)

    def resource_mapper(self, data):
        data_out = np.empty((self.param.B, self.param.K, self.param.M),
                            dtype=type(data[0]))
        data_resh = np.reshape(data, (self.param.B, -1))
        for b in range(self.param.B):
            data_out[b] = self._resource_mapper.mapper(
                data_resh[b], self.param.pilots)
        return data_out

    def resource_demapper(self, data):
        '''
        Parameter
        ---------
        data : shape = (B, K, M)

        Return:
        -------
        demapped_data = [(symbols, pilots)], shape = (B,)

        '''
        return np.vstack([self._resource_mapper.demapper(data[b]) for b in range(self.param.B)])

    def phase_corrector(self, data):
        '''
        Parameter
        ---------
        data = [(data, pilots)]: shape = (B,)

        Return
        ------
        corrected_data: shape = (symbols_per_frame,)
        '''
        if self.param.channel_estimation_type == "preamble":
            return np.concatenate([data[b][0] * np.mean(self.param.pilots / data[b][1]) for b in range(self.param.B)])
        elif self.param.channel_estimation_type == "pilot":
            return np.concatenate([data[b][0] for b in range(self.param.B)])


if __name__ == "__main__":
    pass
