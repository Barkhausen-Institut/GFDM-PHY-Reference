import unittest
import numpy as np

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import simulation.modem.util as util


                                    
class TestResourceMapper(unittest.TestCase):
    def test_generate_ofdm_resource_map(self): 
        K = 8
        M = 1
        Kset = [1,2,4,5]
        gold_resource_map = np.array(['-','D','D','-','D','D','-','-']).reshape(8,1)
        mapper = util.ResourceMapper(K=K,M=M,Kset=Kset)
        np.testing.assert_array_equal(gold_resource_map,mapper.resource_map)
        
    def test_generate_gfdm_resource_map(self):
        K = 8
        M = 4
        Kset = [1,2,4,5]
        Mset = [1,2]
        gold_resource_map = np.array([  ['-','-','-','-'],
                                        ['-','D','D','-'],
                                        ['-','D','D','-'],
                                        ['-','-','-','-'],
                                        ['-','D','D','-'],
                                        ['-','D','D','-'],
                                        ['-','-','-','-'],
                                        ['-','-','-','-']  ] ) 
        mapper = util.ResourceMapper(K=K,M=M,Kset=Kset, Mset= Mset)
        np.testing.assert_array_equal(gold_resource_map,mapper.resource_map)      

    def test_KMset_out_of_range(self):
        K = 8
        M = 4
        Kset = [-1,0,1,2,3,4,5,6,7,8,9]
        Mset = [-1,1,2,4]
        gold_resource_map = np.array([  ['-','D','D','-'],
                                        ['-','D','D','-'],
                                        ['-','D','D','-'],
                                        ['-','D','D','-'],
                                        ['-','D','D','-'],
                                        ['-','D','D','-'],
                                        ['-','D','D','-'],
                                        ['-','D','D','-']  ] ) 
        mapper = util.ResourceMapper(K=K,M=M,Kset=Kset, Mset= Mset)
        np.testing.assert_array_equal(gold_resource_map,mapper.resource_map) 
    

    def test_resouce_map_with_pilots(self):
        K = 8
        M = 4
        Kset = [-1,0,1,2,3,4,5,6,7,8,9]
        Mset = [-1,1,2,4]
        pilot_pos = ([0,4],[1,1])
        gold_resource_map = np.array([  ['-','P','D','-'],
                                        ['-','D','D','-'],
                                        ['-','D','D','-'],
                                        ['-','D','D','-'],
                                        ['-','P','D','-'],
                                        ['-','D','D','-'],
                                        ['-','D','D','-'],
                                        ['-','D','D','-']  ] ) 
        mapper = util.ResourceMapper(K=K,M=M,Kset=Kset, Mset= Mset, pilot_pos=pilot_pos)
        np.testing.assert_array_equal(gold_resource_map,mapper.resource_map)

    def test_mapper_demapper(self):
        mapper = util.ResourceMapper(K=6,M=1, Kset=[1,2,4,5],pilot_pos=[0,3])
        data_in , pilots_in=[1,2,3,4] , [100,200]
        gold_mapped = np.array([100,1,2,200,3,4]).reshape(6,1)
        mapped_data = mapper.mapper(data=data_in, pilots=pilots_in)
        np.testing.assert_array_equal(gold_mapped, mapped_data)
        np.testing.assert_array_equal(data_in,list(mapper.demapper(mapped_data)[0]))
        np.testing.assert_array_equal(pilots_in,list(mapper.demapper(mapped_data)[1]))

    def test_mapper_data_type(self):
        K = 8
        M = 4
        Kset = [1,2,4,5]
        Mset = [1,2]
        gold_resource_map = np.array([  ['-','-','-','-'],
                                        ['-','D','D','-'],
                                        ['-','D','D','-'],
                                        ['-','-','-','-'],
                                        ['-','D','D','-'],
                                        ['-','D','D','-'],
                                        ['-','-','-','-'],
                                        ['-','-','-','-']  ] ) 
        mapper = util.ResourceMapper(K=K,M=M, Kset=Kset,Mset=Mset,pilot_pos=[])
        data_in = np.array([-1.+1.j,  3.-1.j,  3.-1.j, -3.-3.j,  1.+1.j,  3.+1.j, -1.+1.j,  3.-1.j,])
        mapped_data = mapper.mapper(data_in, [])
        self.assertTrue(mapped_data.dtype == data_in.dtype)

    def test_number_of_symbols_per_frame(self):
        K = 8
        M = 4
        Kset = [1,2,4,5]
        Mset = [1,2]
        mapper = util.ResourceMapper(K=K,M=M,Kset=Kset, Mset= Mset, pilot_pos=[(0,1),(0,1)])
        self.assertEqual(mapper.nof_symbols_per_block, 7)
        self.assertEqual(mapper.nof_pilots_per_block, 2)

if __name__ == "__main__":
    unittest.main()
