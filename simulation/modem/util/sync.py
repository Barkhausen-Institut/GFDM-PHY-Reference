
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..','..'))

import numpy as np
import commpy 
from sdr_utils import vector as vec
from sdr_utils import plot_two_signals
class synchronization():
    def __init__(self, param):
        self.halfpreamble = param.halfpreamble
        self.full_pream_len = len(self.halfpreamble)*2
        self.Ncp = param.Ncp
        self.Ncs = param.Ncs
        self.K = param.K
        self.M = param.M
       # self.B = param.B 
        self.N = param.K * param.M
            
    # def sync(self,data):
    #     ''' returns tupel of 2-D arrrays (payload, preamble), where the 1st dimension is number of detected 
    #     preambles and the second dimension is the length on payload / data'''
    #     preamble_starts = self.detect_preamble_starts(data)
    #     preamble = np.vstack([data[(start):(start + self.full_pream_len)] for start in preamble_starts])
    #     payload = np.vstack(
    #         [data[(start + self.full_pream_len + self.Ncs+ self.Ncp ) + np.arange(self.N)] for start in preamble_starts]
    #     )
    #     return (payload, preamble)

    def detect_preamble_starts(self,data):
        self.half_peam_len = len(self.halfpreamble)
        metric = self._calc_metric(data)
        
        peak_locs = self._find_metric_peaks(metric)
        #peak_locs = self._find_single_peak(metric)
        preamble_starts = peak_locs - int(self.half_peam_len/2)
        #print(preamble_starts)
        #plot_two_signals(data, metric) # XXX
        return preamble_starts

    def _calc_metric(self,data):
        cross_corr = np.correlate(data,self.halfpreamble, mode = "same")
        #plot_two_signals(data, cross_corr) # XXX
        metric = cross_corr + vec.shift(cross_corr, -self.half_peam_len)
        metric = (metric.real)**2 + (metric.imag)**2
        #plot_two_signals(cross_corr, metric) # XXX
        autocorr = self._calc_moving_autocorr(data)
        #plot_two_signals(metric/max(abs(metric)), autocorr/max(abs(autocorr)), same_axis=False) 
        return metric*autocorr

    def _calc_threshold(self, metric):
        half_peam_len = len(self.halfpreamble)
        threshold = np.empty(len(metric))
        metric = np.pad(metric,(half_peam_len,0),'constant')
        for i in range(half_peam_len+1, len(metric)):
            window = metric[i-half_peam_len:i]
            window[np.where(window>threshold[i-half_peam_len-1])]/=2
            threshold[i-half_peam_len] = np.sum(window)
        threshold = vec.shift(threshold/2,half_peam_len//4,mode="same",fill_value=threshold[-1]/2)
        threshold[np.where(threshold<max(metric)/100)]= max(metric)/100 
        #plot_two_signals(metric, threshold, same_axis=True) 
        return threshold

    def _find_metric_peaks(self, metric):
        threshold = self._calc_threshold(metric)
        # step 1: find peaks
        locs = np.where(
                (metric>vec.shift(metric,1)) & (metric>vec.shift(metric,-1,fill_value=metric[-1])) & 
                (metric>threshold)
                )[0]
        # step 2: find max peak in window with length of fullpreamble
        last_peak = metric[locs[0]]
        last_loc = locs[0]
        locs_out = np.array([],int)
        for l in locs:
            if ((l - last_loc) > (self.half_peam_len+5)):
                locs_out = np.append(locs_out,last_loc)
                last_peak = 0.0
            if last_peak<metric[l]:
                last_peak = metric[l]
                last_loc = l
        locs_out = np.append(locs_out,last_loc)
        return locs_out
    def _find_single_peak(self, metric):
        threshold = self._calc_threshold(metric)
        loc = np.argmax(metric)
        if metric[loc]>threshold[loc]:
            return np.array([loc])
        else:
            return np.array([])

    def _calc_moving_autocorr(self, data):
        half_peam_len = len(self.halfpreamble)
        Ncp_cs = self.Ncp + self.Ncs
        autocorr = data * vec.shift(data,half_peam_len)
        autocorr_metric = np.empty_like(autocorr)
        for i in range(half_peam_len, len(autocorr)):
            autocorr_metric[i-half_peam_len] = np.sum(autocorr[i-half_peam_len:i])
        autocorr_metric = np.abs(autocorr_metric)
        autocorr_out = np.empty_like(autocorr_metric)
        for i in range(Ncp_cs-2, len(autocorr)):
            autocorr_out[i-Ncp_cs-2] = np.sum(autocorr_metric[i-Ncp_cs-2:i])  
        return  autocorr_out/max(autocorr_out)  #vec.shift(autocorr_out,Ncp_cs+half_peam_len)
