import unittest
import numpy as np
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import channel as Channel
from waveform import get_random
class test_channel(unittest.TestCase):
    def setUp(self): 
        self.ch = Channel.Channel()
 
    def test_awgn(self): 
        data_in = get_random(1024*1000)
        data_out = self.ch.awgn(data_in, snr_db = 0)
        self.assertEqual(len(data_in),len(data_out))
        self.assertAlmostEqual(np.var(data_in),np.var(data_out)/2.0, places=2)

    def test_multipath(self):
        data_in = np.zeros(10, dtype = complex)
        data_in[2] = 1.0 + 0.0j
        self.ch.impulse_response = np.arange(10)+1j*np.arange(10)
        data_out = self.ch.multipath(data_in)
        np.testing.assert_array_almost_equal(data_out[2:12], self.ch.last_impulse_response)
        #self.assertAlmostEqual(np.linalg.norm(data_in), np.linalg.norm(data_out))

if __name__ == "__main__":
    unittest.main()
    