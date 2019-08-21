import unittest
import sys, os

import unittest
import numpy as np

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import simulation.modem.util as util
import sdr_utils


class TestModulator(unittest.TestCase):
    
    def test_ofdm_modulator_demodulator(self):
        modulator = util.Modulator() 
        modulator.type_ = "ofdm"
        modulator.K = 1024
        modulator.M = 1
        data = sdr_utils.get_random(1024)
        modulated_data = modulator.modulate(data)
        np.testing.assert_array_almost_equal(modulated_data, sdr_utils.norm_complex(np.fft.ifft(data)))
        np.testing.assert_array_almost_equal(
            sdr_utils.norm_complex(modulator.demodulate(modulated_data)),sdr_utils.norm_complex(data)
        ) 
    def test_ofdm_modulator_demodulator_vertical_data(self):
        modulator = util.Modulator() 
        data = np.array([   [ 1.+0.j],
                            [-1.+1.j],
                            [ 3.-1.j],
                            [-1.-3.j], 
                            [ 3.-1.j],
                            [-3.+3.j]])
        modulated_data = modulator.modulate(data)
        np.testing.assert_array_almost_equal(modulated_data,sdr_utils.norm_complex( np.fft.ifft(data)))
        np.testing.assert_array_almost_equal(
            sdr_utils.norm_complex(modulator.demodulate(modulated_data)),sdr_utils.norm_complex( data)
        ) 

    def test_gfdm_modulator_demodulator_fd(self):
        K, M = 64, 16

        modulator = util.Modulator(K=K, M= M,type_="gfdm")
        data = sdr_utils.get_random(K*M).reshape(K,M)
        data[:,-1] = 0 + 0j  
        data[:,1] = 0 + 0j   
        data[:,0] = 0 + 0j  
        modulated_data = modulator.modulate(data)
        self.assertAlmostEqual(np.abs(modulated_data[K]),0)
        self.assertAlmostEqual(np.abs(modulated_data[-K]),0)
        self.assertAlmostEqual(np.abs(modulated_data[0]),0)
        self.assertAlmostEqual(np.abs(modulated_data[-1]),0,places=3)

        demodulated_data = modulator.demodulate(np.fft.fft(modulated_data))
        np.testing.assert_array_almost_equal(data, demodulated_data)

if __name__ == "__main__":
    unittest.main()