import numpy as np
import logging
logging.basicConfig(format='%(levelname)s:%(message)s',level=logging.INFO)
def psd(iq):
    return np.fft.fftshift(20*np.log10(np.abs(np.fft.fft(iq))))

def get_tone( tone_freq = 1 * 10 ** 6, sampling_rate = 10 * 10 ** 6 ,samples = 2048):
    '''returns complex beseband tone with given parameters'''
    t = np.arange(samples)/sampling_rate
    # q =  np.sin(2*np.pi*tone_freq*t)
    # i =  np.cos(2*np.pi*tone_freq*t)
    #return i + 1j*q
    return np.exp(1j*2*np.pi*tone_freq * t)

def get_chirp(sampling_rate = 10*10**6,f_start = 1*10**6, f_stop = 2 * 10**6, samples = 2048):
    t = np.arange(samples)/sampling_rate
    f = np.linspace(f_start,f_stop,samples)
    return np.exp(1j*2*np.pi*f*t)

def get_random(samples = 2048):
    """Returns sequence of random comples samples """
    return 2*(np.random.sample((samples,)) + 1j*np.random.sample((samples,))) - (1+1j)

def plot_transmission(tx_signal, rx_signal):
    '''Plots two given signals in time and frequency domains'''
    from matplotlib.pyplot import figure, show
    
    freq = np.linspace(-1/2,1/2,len(tx_signal))
    fig = figure(1)
    ax1 = fig.add_subplot(211)
    ax1.plot(freq,psd(tx_signal))
    ax1.grid(True)
    ax1.set_xlim((-1/2, 1/2))
    ax1.set_ylabel('psd tx signal')

    freq = np.linspace(-1/2,1/2,len(rx_signal))
    ax2 = fig.add_subplot(212)
    ax2.plot(freq,psd(rx_signal))
    ax2.grid(True)
    ax2.set_xlim((-1/2, 1/2))
    ax2.set_xlabel('frequency')
    ax2.set_ylabel('psd rx signal')

    fig = figure(2)
    ax1 = fig.add_subplot(211)
    ax1.plot(tx_signal.real)
    ax1.plot(tx_signal.imag)
    ax1.grid(True)
    ax1.set_ylabel('amplitude tx signal')

    ax2 = fig.add_subplot(212)
    ax2.plot(rx_signal.real)
    ax2.plot(rx_signal.imag)
    ax2.grid(True)
    ax2.set_xlabel('sample')
    ax2.set_ylabel('amplitude rx signal')

    show()

def plot_two_signals(signal_1, signal_2, same_axis = False, show_plot = True):
    from matplotlib.pyplot import figure, show
    
    if same_axis == True:
        fig = figure(1)
        ax_1 = fig.add_subplot(1,1,1)
        ax_1.plot(signal_1.real)
        if isinstance(signal_1[0], complex):
            ax_1.plot(signal_1.imag)
        ax_1.plot(signal_2.real, dashes = [6,2])
        if isinstance(signal_2[0], complex):
            ax_1.plot(signal_2.imag, dashes = [6,2])
        if show_plot: show()
        return ax_1
    else:    
        fig = figure(1)
        ax_1 = fig.add_subplot(2,1,1)
        ax_1.plot(signal_1.real)
        if isinstance(signal_1[0], complex):
            ax_1.plot(signal_1.imag)
        ax_2  = fig.add_subplot(2,1,2)
        ax_2.plot(signal_2.real)
        if isinstance(signal_2[0], complex):
            ax_2.plot(signal_2.imag)
        if show_plot: show()
        return ax_1, ax_2
