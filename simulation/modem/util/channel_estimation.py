import numpy as np


class ChannelEstimation():

    def estimate_channel_form_preamble(self, rx_preamble_time, tx_halfpreamble_time):
        tx_reciproc_half_pream_in_freq = np.reciprocal( np.fft.fft(tx_halfpreamble_time))
        half_preamble_len = len(tx_halfpreamble_time)
        avrege_rx_preamble = (rx_preamble_time[:half_preamble_len] + rx_preamble_time[half_preamble_len:])/2
        avrege_rx_preamble_f = np.fft.fft(avrege_rx_preamble)
        estimated_channel = avrege_rx_preamble_f * tx_reciproc_half_pream_in_freq
        return  estimated_channel

    def estimate_channel_from_pilots(self, rx_pilots_freq, tx_pilots_freq):
        #plot_two_signals(tx_pilots_freq,rx_pilots_freq)
        return rx_pilots_freq /tx_pilots_freq

