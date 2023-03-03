"""
Time series filtration
"""
# pylint: disable=C0103
# pylint: disable=W0611
# pylint: disable=R0915, R0914
import os
import numpy as np
import matplotlib.pyplot as plt
from helper_functions.utility_functions import print_progress_bar
from helper_functions.filters import FFTFilter, Filter
from methods import plot_configurations

def filter_data(CONFIG_DATA: dict, data: np.array, pos: np.array) -> np.array:
    """
    Filter time series data
    """
    INTERVAL_START_TIME_SECONDS = CONFIG_DATA['INTERVAL_START_TIME_SECONDS']
    INTERVAL_END_TIME_SECONDS = CONFIG_DATA['INTERVAL_END_TIME_SECONDS']
    SAMPLING = CONFIG_DATA['SAMPLING']
    FILTER_SELECTION = CONFIG_DATA['FILTER_SELECTION']
    FIRST_COLUMN_TIME = CONFIG_DATA['FIRST_COLUMN_TIME']
    LOW_FREQUENCY_CUTOFF = CONFIG_DATA['LOW_FREQUENCY_CUTOFF']
    HIGH_FREQUENCY_CUTOFF = CONFIG_DATA['HIGH_FREQUENCY_CUTOFF']
    EXPERIMENT_NAME = CONFIG_DATA['EXPERIMENT_NAME']

    # data = np.loadtxt('raw_data/data.txt')
    # pos = np.loadtxt('raw_data/koordinate.txt')
    if FIRST_COLUMN_TIME:
        data = data[:,1:] ##loads all data except first column (time column)

    if len(data[0]) != len(pos):
        # pylint: disable-next=W0719
        raise BaseException("""Number of time series does not match the number of coordinates.
                            Meybe check if the first column in data represents (or not) time?""")
    ########################################################
    #######################Settings##########################

    filter_type = FILTER_SELECTION ##select filter type
    low_frequency = LOW_FREQUENCY_CUTOFF ##select low frequency threshold
    high_frequency = HIGH_FREQUENCY_CUTOFF ###select high frequency threshold

    ######################END OF SETTINGS#####################
    ###########################################################
    number_of_cells = len(data[0])

    time = [i/SAMPLING for i in range(len(data))]

    ###Creates results/filt_traces folder structure of it does not exist
    if not os.path.exists(f'preprocessing/{EXPERIMENT_NAME}/filt_traces'):
        os.makedirs(f'preprocessing/{EXPERIMENT_NAME}/filt_traces')

    filtered_series = np.zeros((len(data), number_of_cells), float)

    for ts_num in range(number_of_cells):
        cut_signal = None
        if filter_type == 'analog':
            signal_filter = Filter(data[:,ts_num], SAMPLING)
            cut_signal = signal_filter.bandpass(low_frequency, high_frequency)
        elif filter_type == 'fft':
            signal_filter = FFTFilter(data[:,ts_num], time)
            signal_filter.find_fftfreq()
            signal_filter.rfft()
            signal_filter.bandpass_filt(low_frequency, high_frequency)
            cut_signal = signal_filter.get_filtered_signal()

        print_progress_bar(ts_num+1, number_of_cells, f'Filtering time series {ts_num} ')

        fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
        ax1.set_title('Raw signal')
        ax1.plot(time, data[:,ts_num], linewidth=0.5, color='dimgrey')
        ax1.set_ylabel('Signal (a.u)')

        ax2.set_title('Raw signal outtake')
        ax2.plot(time, data[:, ts_num], linewidth=0.67, color='dimgrey')
        ax2.set_xlim([INTERVAL_START_TIME_SECONDS, INTERVAL_END_TIME_SECONDS])
        ax2.set_ylabel('Signal (a.u)')

        ax3.set_title('Filtered signal outtake')
        ax3.plot(time, cut_signal, linewidth=0.67, color='dimgrey')
        ax3.set_xlim([INTERVAL_START_TIME_SECONDS, INTERVAL_END_TIME_SECONDS])
        ax3.set_ylabel('Signal (a.u)')
        ax3.set_xlabel('time (s)')
        plt.subplots_adjust(hspace=0.6)
        fig.savefig(
            f"preprocessing/{EXPERIMENT_NAME}/filt_traces/cell_{ts_num}.jpg",
            dpi=200, bbox_inches='tight')
        plt.close(fig)

        cut_signal[:] = (cut_signal[:] - np.min(cut_signal[:])) / \
            (np.max(cut_signal[:]) - np.min(cut_signal[:]))

        filtered_series[:,ts_num] = cut_signal

    np.savetxt(f'preprocessing/{EXPERIMENT_NAME}/filtered_data.txt',
               filtered_series, fmt='%.3lf')
    return filtered_series
