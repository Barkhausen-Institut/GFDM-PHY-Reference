import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..','..'))


import unittest
import sdr_utils

import commpy
from commpy.utilities import bitarray2dec, dec2bitarray
from simulation.modem import Modem, ModemParameter, get_gfdm_preable_based, get_ofdm_pilot_based, get_ofdm_preamble_based
import numpy as np 

import simulation.modem.util as util

def norm_complex(data):
    max_val = max( max(abs(data.real)),max(abs(data.imag)) )
    if max_val > 0:
        return data / max_val
    else: 
        return data

class TestModem(unittest.TestCase):   
    def test_gfdm_b_1(self):
        p = get_gfdm_preable_based()
        m = Modem(p)
        self._test_modem(m)

    def test_ofdm_b_1(self):
        p = get_ofdm_preamble_based()
        m = Modem(p)
        self._test_modem(m)
        
    def test_ofdm_b_2(self):
        p = get_ofdm_preamble_based()
        p.B = 2
        m = Modem(p)
        self._test_modem(m)

    def test_ofdm_b_1_pilot(self):
        p = get_ofdm_pilot_based()
        p.B = 1
        m = Modem(p)
        self._test_modem(m)

    def _test_modem(self,modem):
        modem.save_intern_data = True
        modem.receiver(modem.transmitter())
        p = modem.param
        data = modem.intern_data
        # TX
        self.assertEqual(np.shape(data["bytes_in"]),(modem.bytes_per_frame,) )
        self.assertEqual(np.shape(data["encoder"]),(modem.bits_per_frame,) )
        self.assertEqual(np.shape(data["qam_mapper"]),(modem.symbols_per_frame,) )
        self.assertEqual(np.shape(data["resource_mapper"]),(p.B,p.K,p.M) )
        self.assertEqual(np.shape(data["modulator"]),(p.B,p.K*p.M) )
        self.assertEqual(np.shape(data["add_cp_cs"]),(p.B*(p.Ncp+p.Ncs+p.Npayload),) )
        self.assertEqual(np.shape(data["frame_multiplexer"]),(p.B*(p.Ncp+p.Ncs+p.Npayload)+(p.Ncp+p.Ncs+p.Npreamble),) )
        # RX
        self.assertEqual(np.shape(data["sync"][0]),(p.B,p.Npayload))
        self.assertEqual(np.shape(data["sync"][1]),(p.Npreamble,))
        self.assertEqual(np.shape(data["channel_est_eq"]),(p.B,p.Npayload) )
        self.assertEqual(np.shape(data["demodulator"]),(p.B,p.K,p.M) )
        self.assertEqual(np.shape(data["resource_demapper"]), (p.B, 2) )
        self.assertEqual(np.shape(data["phase_corrector"]),(modem.symbols_per_frame,) )
        self.assertEqual(np.shape(data["qam_demapper"]),(modem.bits_per_frame,) )
        self.assertEqual(np.shape(data["decoder"]),(modem.bytes_per_frame,) )

        np.testing.assert_array_equal(data["sync"][1], p.fullpreamble) 
        for b in range(p.B):
            np.testing.assert_array_equal(
                data["sync"][0][b], data["frame_multiplexer"][p.Ncp +p.Npreamble_cp_cs +np.arange(p.Npayload)+b*p.Npayload_cp_cs]
            ) 
            
            np.testing.assert_array_almost_equal(
                norm_complex(data["channel_est_eq"][b]), 
                norm_complex(np.fft.fft(data["frame_multiplexer"][p.Ncp +p.Npreamble_cp_cs +np.arange(p.Npayload)+b*p.Npayload_cp_cs]))
            )

        np.testing.assert_array_almost_equal(
            data["phase_corrector"], data["qam_mapper"]
        ) 
        np.testing.assert_array_equal(data["bytes_in"], data["decoder"]) 
        
 


if __name__ == "__main__":
    unittest.main()
    
