import unittest
import numpy as np
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import vector as vec

class test_vector(unittest.TestCase):
    def test_find_peaks(self):
        NotImplemented
    def test_shift_pos_same(self):
        data_in =  np.array([0,1,2,3,4,5,6,7])
        gold_out = np.array([0,0,0,0,1,2,3,4])
        np.testing.assert_array_equal(gold_out,vec.shift(data_in,3, mode="same"))

    def test_shift_neg_same(self):
        data_in =  np.array([0,1,2,3,4,5,6,7])
        gold_out = np.array([3,4,5,6,7,0,0,0])
        np.testing.assert_array_equal(gold_out,vec.shift(data_in,-3, mode="same"))

if __name__ == "__main__":
    unittest.main()