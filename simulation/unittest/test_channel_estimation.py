import unittest
import numpy as np

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import simulation.modem.util as util
from simulation.modem import Modem, get_ofdm_preamble_based
import sdr_utils

class TestChannelEstimation(unittest.TestCase):
    #   Frame 1:
    #       Frame structure:
    #       <-zeros-><-cp-><---hp---><---hp---><-cs-><-cp-><--------------------data-------------------><-cs->
    #       zeros = 255, cp = 16, cs = 16, hp = 65, data = 1024 
    def setUp(self):
        pass
    def test_channel_estimation(self):
        ch = sdr_utils.Channel()
        ch.impulse_response = ch.test_impulse_response
        # use modem to generate frame 
        modem = Modem(get_ofdm_preamble_based()) 
        p = modem.param   
        tx_frame = modem.transmitter()
        rx_frame = ch.multipath(tx_frame)

        ch_estimator = util.ChannelEstimation()
        estimated_channel = ch_estimator.estimate_channel_form_preamble(rx_frame[p.Ncp+np.arange(p.Npreamble)], p.halfpreamble)
        estimated_impulse_response = np.fft.ifft(estimated_channel)
        np.testing.assert_array_almost_equal(ch.last_impulse_response, estimated_impulse_response[:len(ch.last_impulse_response)],decimal=2)

if __name__ == "__main__":
    unittest.main()
