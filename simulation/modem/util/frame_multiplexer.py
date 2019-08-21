

import numpy as np

class FrameMultiplexer():

    def multiplex_frame(self, data, preamble):
        ''' Frame Multilpexer

            Parameters
            ----------
            data : 1d or 2d array
                Array of data blocks. 
                1st dimension - number of blocks, 
                2st didension - block length

            preamble : 1d array
                contains preamble
        '''
        if np.ndim(data) == 2:
            return  np.concatenate( 
                        (preamble, np.concatenate([d for d in data]))
                    )
        elif np.ndim(data) == 1:
            return np.concatenate((preamble, data))
