import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..','..'))


import unittest
import sdr_utils

import commpy
from commpy.utilities import bitarray2dec, dec2bitarray
import simulation.modem as modem 
from simulation.modem.util import synchronization
import numpy as np 
import simulation.modem.util as util

class TestSynchronization(unittest.TestCase):
    def _createFullPreamble(self, param):
        return util.add_cp_cs(np.hstack([param.halfpreamble, param.halfpreamble]), param.Ncp, param.Ncs)  

    def setUp(self):
        self.param = modem.ModemParameter()
        self.sync = synchronization(self.param) 

    def test_identityChannel_preamble_at_beginning(self):
        data = np.hstack([self._createFullPreamble(self.param), np.zeros(1000)])
        self.assertEqual(self.sync.detect_preamble_starts(data), [self.param.Ncp])

    def test_identityChannel_preamble_in_middle_default_cp_cs(self):
        data = self._get_test_data(255,1)
        np.testing.assert_array_equal(self.sync.detect_preamble_starts(data), [255+self.param.Ncp])

    def test_identityChannel_preamble_in_middle_zero_cp_cs(self):
        self.param.Ncp , self.param.Ncs = 0, 0
        data = self._get_test_data(255,1)
        self.sync = synchronization(self.param) 
        np.testing.assert_array_equal(self.sync.detect_preamble_starts(data), [255+self.param.Ncp])
   
    def test_identityChannel_preamble_in_middle_cp_cs_16(self):
        self.param.Ncp , self.param.Ncs = 16, 16
        data = self._get_test_data(255,1)
        self.sync = synchronization(self.param) 
        np.testing.assert_array_equal(self.sync.detect_preamble_starts(data), [255+self.param.Ncp])

    def test_identityChannel_preamble_in_middle_cp_cs_32(self):
        self.param.Ncp , self.param.Ncs = 32, 32
        data = self._get_test_data(255,1)
        self.sync = synchronization(self.param) 
        np.testing.assert_array_equal(self.sync.detect_preamble_starts(data), [255+self.param.Ncp])

    def test_identityChannel_two_preambles(self):
        data = np.hstack([self._createFullPreamble(self.param), np.zeros(1000)])
        data_double = np.hstack([data, data])
        np.testing.assert_array_equal(self.sync.detect_preamble_starts(data_double), [self.param.Ncp, len(data)+self.param.Ncp])
    
    def test_awgn_channel(self):
        ch = sdr_utils.Channel()
        tx_data = self._get_test_data(255,1)
        
        np.testing.assert_array_equal(
            self.sync.detect_preamble_starts(ch.awgn(tx_data, snr_db = 10)), [255+self.param.Ncp]
            )

    def test_multipath_cahnnel(self):
        tx_data = self._get_test_data(255,1)
        ch = sdr_utils.Channel()
        ch.impulse_response = np.array([1+1j,0,0,0,0,1+1j,0,0,0,0,1+1j,0,0,0,0,1+1j,0,0,0,0])
        ch.impulse_response *= np.exp(np.linspace(0,-10,len(ch.impulse_response)))
        ch.impulse_response /= np.linalg.norm(ch.impulse_response) 
        rx_data = ch.multipath(tx_data)
        np.testing.assert_array_equal(self.sync.detect_preamble_starts(rx_data), [255+self.param.Ncp])

    def _get_test_data(self, interval= 255, frames = 1):
        tx_data = np.hstack(
            [np.hstack(
                [np.hstack([np.zeros(interval), self._createFullPreamble(self.param)]) for _ in range(frames)]
                ), np.zeros(interval)]   )
        return tx_data
if __name__ == "__main__":
    unittest.main()
    