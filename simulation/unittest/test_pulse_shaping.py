import unittest
import numpy as np

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import simulation.modem.util as util

                                    
class TestPulseShaping(unittest.TestCase):
    def test_generate_rc_filter(self):
        values = list()
        with open(os.path.join(os.path.dirname(__file__), 'rc_filter_64_16_ref.txt')) as h:
            for line in h:
                values.append(eval(line))
        reference = np.array(values)
        rc_filter, _ = util.get_rc_filter(K=64, M =16)

        np.testing.assert_array_almost_equal(rc_filter, reference)

if __name__ == "__main__":
    unittest.main()
