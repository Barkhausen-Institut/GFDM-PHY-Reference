import unittest
import numpy as np

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import simulation.modem.util as util

from commpy.utilities import bitarray2dec, dec2bitarray
                                    
class TestCoder(unittest.TestCase):
    
    def test_identity_coder(self):
        coder = util.Coder("identity") 
        data = np.arange(255)
        self._test_coder(coder, data)

    def test_identity_coder_transosed_data(self):
        coder = util.Coder("identity") 
        data = np.arange(255).transpose()
        self._test_coder(coder, data)

    def test_identity_coder_data_out_of_range(self):
        coder = util.Coder("identity") 
        data = np.arange(300).transpose()
        with self.assertRaises(ValueError) as _:
            coder.encode(data)
        
    def _test_coder(self, coder, data):
        encoded_data = coder.encode(data) 
        # test if data is converted to bits 
        self.assertEqual( 
            len(encoded_data), int(len(data)*coder.byte_width*(1/coder.code_rate)) 
        )
        np.testing.assert_array_equal(
            np.array([0,1]), np.sort(np.unique(encoded_data))
        )     
        # test if data is decoded correctly 
        np.testing.assert_array_equal(
            data, coder.decode(encoded_data)
        )
if __name__ == "__main__":
    unittest.main()
