import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..','..'))

import unittest
import numpy as np

from simulation.modem import util


class Test_cyclic_prefix_suffix(unittest.TestCase):
    def test_add_remove_cp(self):
        data_in = np.array([0,1,2,3,4,5,6,7])
        gold_out = np.array([5,6,7,0,1,2,3,4,5,6,7])
        Ncp=3
        data_cp = util.add_cp(data_in, Ncp)
        np.testing.assert_array_equal(data_cp, gold_out)
        np.testing.assert_array_equal(util.remove_cp(data_cp, Ncp), data_in)
    
    def test_zero_cp(self):
        data_in = np.array([0,1,2,3,4,5,6,7])
        Ncp = 0
        data_cp = util.add_cp(data_in, Ncp)
        np.testing.assert_array_equal(data_cp, data_in)
        np.testing.assert_array_equal(util.remove_cp(data_cp, Ncp), data_in)

    def test_add_remove_cs(self):
        data_in = np.array([0,1,2,3,4,5,6,7])
        gold_out = np.array([0,1,2,3,4,5,6,7,0,1,2])
        Ncs = 3
        data_cs = util.add_cs(data_in, Ncs)
        np.testing.assert_array_equal(data_cs, gold_out)
        np.testing.assert_array_equal(util.remove_cs(data_cs, Ncs), data_in)
    
    def test_zero_cs(self):
        data_in = np.array([0,1,2,3,4,5,6,7])
        Ncs = 0
        data_cs = util.add_cs(data_in, Ncs)
        np.testing.assert_array_equal(data_cs, data_in)
        np.testing.assert_array_equal(util.remove_cs(data_cs, Ncs), data_in)
    
    def test_add_cp_cs(self):
        data_in = np.array([0,1,2,3,4,5,6,7])
        gold_out = np.array([5,6,7,0,1,2,3,4,5,6,7,0,1,2])
        Ncp = 3
        Ncs = 3
        np.testing.assert_array_equal(
            gold_out, util.add_cp_cs(data_in, Ncp, Ncs)  
        )
        
if __name__ == "__main__":
    unittest.main()