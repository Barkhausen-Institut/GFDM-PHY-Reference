import typing
import numpy as np
import os
import unittest
import shutil

def array_to_file(array_in, file_name:str, as_complex = True):
    with open(file_name,"w+") as f:
        for s in array_in:
            if as_complex:
                f.write(f"{s.real} {s.imag}\n")
            else:
                f.write(f"{s}\n")

def transform_complex(line):
    return line[0]+1j*line[1]

def file_to_array(file_name:str):
    with open(file_name, 'r') as f:
        arr = np.loadtxt(f)
    if arr.ndim == 2:
        return arr[:,0]+1j*arr[:,1]
    elif arr.ndim == 1:
        return arr
    else:
        raise ValueError("Invalid format: to many columns")
        
def get_filtered_file_names(path, pattern):
    import os, fnmatch
    return fnmatch.filter(os.listdir(path), pattern)

def load_all_files(path, pattern):
    file_names = get_filtered_file_names(path, pattern)
    d ={}
    for file_name in file_names:
        d[file_name] = file_to_array(path+file_name)
    return d

def plot_all_data(data, same_axis = False, show = True):
    import matplotlib.pyplot as plt
    plt.figure()
    for file_name in data:
        if same_axis:
            if isinstance(data[file_name][0],complex):
                plt.plot(data[file_name].real, label = file_name + " real")
                plt.plot(data[file_name].imag, label = file_name + " imag")
            else:
                plt.plot(data[file_name], label = file_name)
        else:
            plt.figure()
            if isinstance(data[file_name][0],complex):
                plt.plot(data[file_name].real, label = "real")
                plt.plot(data[file_name].imag, label = "imag")
            else:
                plt.plot(data[file_name])
            plt.title(file_name)
    plt.legend()    
    if show:    
        plt.show()

class TestThis(unittest.TestCase):
    test_path = "test_folder_3687/"
    def setUp(self):
        if not os.path.exists(self.test_path):
            os.makedirs(self.test_path)
        else:
            shutil.rmtree(self.test_path)
            os.makedirs(self.test_path)

    def test_array_to_file_file_to_array_real(self):
        arr_1 = np.arange(10)/10
        array_to_file(arr_1, self.test_path + "test1.txt")  
        arr_2 = file_to_array(self.test_path + "test1.txt")
        np.testing.assert_array_equal(arr_1,arr_2)
   
    def test_array_to_file_file_to_array_complex(self):
        arr_1 = np.arange(10)/10 + 1.0654684354687543j
        array_to_file(arr_1, self.test_path + "test1.txt")  
        arr_2 = file_to_array(self.test_path + "test1.txt")
        np.testing.assert_array_equal(arr_1,arr_2)
    def test_get_filtered_names(self):
        arr = [1,2,3]
        array_to_file(arr, self.test_path+"test_file_1.txt")
        array_to_file(arr, self.test_path+"test_file_2.txt")
        array_to_file(arr, self.test_path+"file_3.txt")
        array_to_file(arr, self.test_path+"test_file_4.dat")
        file_names = get_filtered_file_names(self.test_path,"test_*.txt")
        self.assertTrue("test_file_1.txt" in file_names)
        self.assertTrue("test_file_2.txt" in file_names)
        self.assertTrue(len(file_names)==2)
    def test_plot_all(self):
        arr_1 = np.arange(6.28*100)/100
        arr_2 = np.sin(arr_1) + 1j*np.cos(arr_1)
        array_to_file(arr_1, self.test_path + "test_1.txt", as_complex= False) 
        array_to_file(arr_2, self.test_path + "test_2.txt") 
        plot_all_data(load_all_files(self.test_path, "test_*.txt"), same_axis=False)
        plot_all_data(load_all_files(self.test_path, "test_*.txt"), same_axis=True)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_path):
            shutil.rmtree(cls.test_path)


def main():
    unittest.main()
if __name__ == "__main__":
    main()