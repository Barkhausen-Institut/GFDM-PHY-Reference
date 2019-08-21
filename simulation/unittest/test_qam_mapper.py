import unittest
import numpy as np

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import simulation.modem.util as util

from commpy.utilities import bitarray2dec, dec2bitarray
                                    
class TestQamMapper(unittest.TestCase):
    def _test_qam_mapper_demapper(self, m):
        mapper = util.QamMapper(m)
        data_in = np.hstack([dec2bitarray(n, int(np.sqrt(m))) for n in range(m)])
        qam_data = mapper.modulate(data_in)
        
        self.assertEqual(len(qam_data),(len(data_in)//np.log2(m)))
        self.assertTrue(len(set(qam_data))==m)
        data_out = mapper.demodulate(qam_data)
        np.testing.assert_array_almost_equal(data_out,data_in)

    def test_qam16_mapper_demapper(self):
        self._test_qam_mapper_demapper(16)
    
    def test_qam4_mapper_demapper(self):
        self._test_qam_mapper_demapper(4)


if __name__ == "__main__":
    unittest.main()
