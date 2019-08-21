import unittest
import numpy as np

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import simulation.modem.util as util

from commpy.utilities import bitarray2dec, dec2bitarray
                                    
class TestFrameMultiplexor(unittest.TestCase):
    def test_construct_frame_B_greater_one(self):
        multiplexer = util.FrameMultiplexer()
        data = np.array([[1,2,3,4,5],[6,7,8,9,10]])
        preamble = np.array([-3,-2,-1])
        gold_out = np.array([-3,-2,-1,1,2,3,4,5,6,7,8,9,10])
        np.testing.assert_array_equal(
            gold_out, multiplexer.multiplex_frame(data, preamble)
        )
    def test_construct_frame_B_is_one(self):
        multiplexer = util.FrameMultiplexer()
        data = np.array([1,2,3,4,5])
        preamble = np.array([-3,-2,-1])
        gold_out = np.array([-3,-2,-1,1,2,3,4,5])
        np.testing.assert_array_equal(
            gold_out, multiplexer.multiplex_frame(data, preamble)
        )

if __name__ == "__main__":
    unittest.main()
