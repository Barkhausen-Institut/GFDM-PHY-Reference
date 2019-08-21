import numpy as np
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..','..','..'))
import sdr_utils

def get_rc_filter(K, M):
    N = M*K

    if M%2 ==0:
        shift = 0.5
    else:
        shift = 0
    f = np.linspace(-0.5,(0.5-1/N),N)+shift/N 
    g_f = np.zeros_like(f)
    idx = np.where(np.abs(f)<=(1)/(2*K))
    g_f[idx] = 1
    gain = np.linalg.norm(g_f)
    g_f = np.sqrt(N)*g_f/gain
    g_f = np.fft.fftshift(g_f)
    g = np.fft.ifft(g_f)
    return (g, gain)

def get_zf_receiver_filter(tx_filter, K, M):
    # a = tx_filter.reshape((M,K))
    # b = np.reshape(
    #     np.hstack(
    #         [np.fft.ifft(np.reciprocal(np.conjugate(np.fft.fft(a[:,k])))) for k in range(K)]
    #     ), K*M
    # ) 
    gm = np.reshape(tx_filter, (K, M))
    Gm = np.fft.fft(gm, axis=1)
    iGm = 1/ np.conj(Gm)
    gmd = np.fft.ifft(iGm, axis=1)
    gd = np.reshape(gmd, K*M)
    return gd


def main():
    
    K, M = 32, 6
    tx_filter = np.fft.fft(get_rc_filter(K,M)[0])
    sdr_utils.plot_two_signals(get_rc_filter(K,M)[0],tx_filter)

if __name__ == "__main__":
    main()
