"""
Time series binarization
"""
# pylint: disable=C0103
# pylint: disable=W0611
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, peak_widths
from helper_functions.ploting_funcs import binarized_plot
from configurations import (AMP_FACT, INTERPEAK_DISTANCE, PEAK_WIDTH,
                            PROMINENCE, REL_HEIGHT, INTERVAL_START_TIME_SECONDS,
                            INTERVAL_END_TIME_SECONDS, SAMPLING)
import plot_configurations
############################################
###### Settings#################
# For signal visualization
start_time_seconds = INTERVAL_START_TIME_SECONDS
end_time_seconds = INTERVAL_END_TIME_SECONDS

# For binarization
amp_fact = AMP_FACT  # rise from average signal
distance = INTERPEAK_DISTANCE  # min distance between peaks (in samples)
width = PEAK_WIDTH  # approximate width of peaks (in samples)
prominence = PROMINENCE  # required prominance/rise of peaks to be considered
rel_height = REL_HEIGHT  # calculates the peak width relative to its prominance
###### End of settings###########
#############################################


# Loads all data
data = np.loadtxt('preprocessing/smoothed_traces.txt')

# Calculates and sets necessary data
number_of_cells = len(data[0])
time = [i/SAMPLING for i in range(len(data))]
bin_signal = np.zeros((len(data), number_of_cells), int)

start_time_frames = int(start_time_seconds*SAMPLING)
end_time_frames = int(end_time_seconds*SAMPLING)

if not os.path.exists('preprocessing/binarized_traces'):
    os.makedirs('preprocessing/binarized_traces')

for i in range(number_of_cells):
    print(f'Binarization of time series {i}')
    # peaks: indexes of detected peaks
    peaks, properties = find_peaks(data[:, i],
                                   height=amp_fact*np.average(data[:, i]),
                                   distance=distance,
                                   width=width,
                                   prominence=prominence)

    widths, width_heights, left_ips, right_ips = peak_widths(data[:, i],
                                                             peaks,
                                                             rel_height=rel_height)

    bin_signal[peaks, i] = 1
    for index, left_points, right_points in zip(peaks, left_ips, right_ips):
        left_width = index - (index - int(round(left_points)))
        right_width = index + (int(round(right_points)) - index)
        max_amp = np.amax(data[index-left_width:index+right_width+1, i])
        min_amp = np.amin(data[index-left_width:index+right_width+1, i])
        threshold_amp = min_amp + (max_amp - min_amp)/2.0

        # Binarizes points left and right from the detected peak
        # if amplitude >= threshold_amp
        for j in range(1, max(left_width, right_width), 1):
            if index-j >= 0:
                if data[index-j, i] >= threshold_amp:
                    if data[index-j+1, i] > threshold_amp:
                        bin_signal[index-j, i] = 1
            if index+j < len(data)-1:
                if data[index+j, i] >= threshold_amp:
                    if data[index+j-1, i] > threshold_amp:
                        bin_signal[index+j, i] = 1

    fig, (ax1, ax2) = plt.subplots(2, 1)
    ax1.set_title(f'Cell {i}')
    ax1.plot(time, data[:, i], c='dimgray', linewidth=0.5)
    ax1.set_ylabel('Signal (a.u.)')

    ax2.plot(time, data[:, i], c='dimgray', linewidth=0.5)
    ax2.plot(time, bin_signal[:, i], c='red', linewidth=0.5)
    ax2.set_xlabel('time (s)')
    ax2.set_ylabel('Binarized signal')
    ax2.set_xlim(start_time_seconds, end_time_seconds)

    plt.subplots_adjust(hspace=0.15)
    fig.savefig(f'preprocessing/binarized_traces/binarized_traces_{i}.png',
                dpi=200, bbox_inches='tight', pad_inches=0.01)
    plt.close(fig)

np.savetxt('preprocessing/binarized_traces.txt', bin_signal, fmt='%d')

fig = binarized_plot(time, bin_signal)
fig.savefig('preprocessing/raster_plot.png', dpi=200, bbox_inches='tight')
plt.close(fig)
