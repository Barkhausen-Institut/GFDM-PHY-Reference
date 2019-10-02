from matplotlib.pyplot import figure, show


def plot_two_signals(signal_1, signal_2, same_axis=False, show_plot=True):

    if same_axis:
        fig = figure(1)
        ax_1 = fig.add_subplot(1, 1, 1)
        ax_1.plot(signal_1.real)
        if isinstance(signal_1[0], complex):
            ax_1.plot(signal_1.imag)
        ax_1.plot(signal_2.real, dashes=[6, 2])
        if isinstance(signal_2[0], complex):
            ax_1.plot(signal_2.imag, dashes=[6, 2])
        if show_plot:
            show()
        return ax_1
    else:
        fig = figure(1)
        ax_1 = fig.add_subplot(2, 1, 1)
        ax_1.plot(signal_1.real)
        if isinstance(signal_1[0], complex):
            ax_1.plot(signal_1.imag)
        ax_2 = fig.add_subplot(2, 1, 2)
        ax_2.plot(signal_2.real)
        if isinstance(signal_2[0], complex):
            ax_2.plot(signal_2.imag)
        if show_plot:
            show()
        return ax_1, ax_2
