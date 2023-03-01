"""
Time series filtration
"""
# pylint: disable=C0103
# pylint: disable=W0611
import os
import numpy as np
import matplotlib.pyplot as plt
from helper_functions.filters import Filter, FFTFilter
from configurations import (INTERVAL_START_TIME_SECONDS, INTERVAL_END_TIME_SECONDS,
                            SAMPLING, FILTER_SELECTION, FIRST_COLUMN_TIME,
                            LOW_FREQUENCY_CUTOFF, HIGH_FREQUENCY_CUTOFF)
import plot_configurations

###Loads raw time series array (NxM) and sampling data
### N - number of time points
### M - number of cells
data = np.loadtxt('raw_data/data.txt') ##loads all data except first column (time column)
if FIRST_COLUMN_TIME:
    data = data[:,1:]

########################################################
#######################Settings##########################

filter_type = FILTER_SELECTION ##select filter type
low_frequency = LOW_FREQUENCY_CUTOFF ##select low frequency threshold
high_frequency = HIGH_FREQUENCY_CUTOFF ###select high frequency threshold

######################END OF SETTINGS#####################
###########################################################

start_time_frames = int(INTERVAL_START_TIME_SECONDS*SAMPLING)
end_time_frames = int(INTERVAL_END_TIME_SECONDS*SAMPLING)
number_of_cells = len(data[0])

time = [i/SAMPLING for i in range(len(data))]

###Creates results/filt_traces folder structure of it does not exist
if not os.path.exists('preprocessing/filt_traces'):
    os.makedirs('preprocessing/filt_traces')

filtered_series = np.zeros((len(data), number_of_cells), float)
smoothed_series = np.zeros((len(data), number_of_cells), float)

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

    print(f'Filtering time series {ts_num}')

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
        f"preprocessing/filt_traces/cell_{ts_num}.jpg", dpi=200, bbox_inches='tight')
    plt.close(fig)

    cut_signal[:] = (cut_signal[:] - np.min(cut_signal[:])) / \
        (np.max(cut_signal[:]) - np.min(cut_signal[:]))

    filtered_series[:,ts_num] = cut_signal

np.savetxt('preprocessing/filtered_data.txt', filtered_series, fmt='%.3lf')
