#   Frame 1:
#       Frame structure:
#       <-zeros-><-cp-><---hp---><---hp---><-cs-><-cp-><--------------------data-------------------><-cs->
#       zeros = 255, cp = 16, cs = 16, hp = 65, data = 1024 

import pickle

def get_test_data(file_name:str):
    with open(file_name,"rb") as f:
        test_data = pickle.load(f)
    return test_data

def save_test_data(file_name:str, data):
    with open(file_name,"w+") as f:
        print("BÄM!")
    with open(file_name,"wb") as f:
        pickle.dump(data,f)

    # def test_save_test_frame(self):
    #     import test_data
    #     frame,halfpreamble,payload = self._get_frame()
    #     data = {"frame":frame,"halfpreamble":halfpreamble,"payload":payload, "Ncp":16, "Ncs":16,
    #     "Nhp":64, "Ndata":1024}
    #     test_data.save_test_data("test_data/frame_1",data)
    #     data_r = test_data.get_test_data("test_data/frame_1")
    #     np.testing.assert_array_equal(frame,data_r["frame"])
    #     np.testing.assert_array_equal(halfpreamble,data_r["halfpreamble"])
    #     np.testing.assert_array_equal(payload,data_r["payload"])