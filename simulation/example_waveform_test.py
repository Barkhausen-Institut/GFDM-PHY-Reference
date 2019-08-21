import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from sdr_utils import plot_transmission
from modem import Modem, get_ofdm_preamble_based, get_ofdm_pilot_based, get_gfdm_preable_based
import sdr_utils
import time

import numpy as np
import matplotlib.pyplot as plt
class Session():
    def __init__(self, modem):
        self.modem = modem
        self.modem.param.qam_order = 16
        self.modem.save_intern_data = True
        self.channel = sdr_utils.Channel()
        self.channel.impulse_response = self.channel.test_impulse_response
        self.nof_transmissions = 100
        self.stop_flag = False
        self._prepare_plot()

    def _handle_plot_close(self, evt):
        self.stop_flag = True 
    
    def _prepare_plot(self):
        self.fig_constell = plt.figure()
        self.fig_constell.canvas.mpl_connect('close_event', self._handle_plot_close)
        self.ax_constell = self.fig_constell.add_subplot(1,1,1)
        self.fig_sig = plt.figure()
        self.ax_sig = self.fig_sig.add_subplot(1,1,1)

    def _update_plot(self, data):
        # plot constellation
        iq_data = data["phase_corrector"]
        if iq_data.size > 0:
            self.ax_constell.scatter(iq_data.real, iq_data.imag, marker=".")
            self.ax_constell.grid(True)
        else: 
            self.ax_constell.cla()
        #plot received samples
        rx_samples = data["receiver"]
        if rx_samples.size > 0: 
            self.ax_sig.cla()
            self.ax_sig.plot(rx_samples.real)
            self.ax_sig.plot(rx_samples.imag)
        plt.draw()
        plt.pause(0.01)

    def run(self):
        self.stop_flag = False
        for _ in range(self.nof_transmissions):
            data = self._get_transmission()
            self._update_plot(data)
            if self.stop_flag == True:
                return

    def _get_transmission(self):
        tx_samples = self.modem.transmitter()
        rx_samples = self.channel.multipath(np.pad(tx_samples, (100,100), 'constant'),snr_db=70)*0.1
        #rx_samples = tx_samples
        self.modem.receiver(rx_samples)    
        data = self.modem.intern_data
        return data
  
def main():
    #modem = Modem(get_ofdm_preamble_based())
    modem = Modem(get_gfdm_preable_based())
    session = Session(modem)
    session.run()

if __name__ == "__main__":
    main()
