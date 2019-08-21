import unittest
import numpy as np

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import simulation.modem.util as util
from simulation.modem import Modem, get_ofdm_preamble_based
import sdr_utils

class TestEqualizer(unittest.TestCase):
    #   Frame 1:
    #       Frame structure:
    #       <-zeros-><-cp-><---hp---><---hp---><-cs-><-cp-><--------------------data-------------------><-cs->
    #       zeros = 255, cp = 16, cs = 16, hp = 65, data = 1024 
    def setUp(self):
        pass
    def test_channel_equalizer(self):
        ch = sdr_utils.Channel()
        ch.impulse_response = ch.test_impulse_response
        modem = Modem(get_ofdm_preamble_based())
        p = modem.param   
        tx_frame = modem.transmitter()
        rx_frame = ch.multipath(tx_frame)  
        idx = p.Ncp + p.Npreamble_cp_cs + np.arange(p.Npayload)
        tx_payload = tx_frame[idx]
        rx_payload = rx_frame[idx]
        ch_estimator = util.ChannelEstimation()
        estimated_channel = ch_estimator.estimate_channel_form_preamble(rx_frame[p.Ncp+np.arange(p.Npreamble)], p.halfpreamble)  
        equalizer = util.Equalizer()
        eq_payload = np.fft.ifft(equalizer.equalize(np.fft.fft(rx_payload), estimated_channel))
        np.testing.assert_array_almost_equal(tx_payload, eq_payload, decimal= 1)

if __name__ == "__main__":
    unittest.main()
