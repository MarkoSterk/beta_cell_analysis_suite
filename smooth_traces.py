"""
Time series smoothing
"""
# pylint: disable=C0103
# pylint: disable=W0611

import os
import numpy as np
import matplotlib.pyplot as plt
from helper_functions.smoothing import smooth_ts
from configurations import (SAMPLING, INTERVAL_START_TIME_SECONDS, INTERVAL_END_TIME_SECONDS,
                            SMOOTHING_POINTS, SMOOTHING_REPEATS)
import plot_configurations

# Smoothing settings
number_of_points = SMOOTHING_POINTS  # integer number > 0. Number of points to average over
number_of_smoothings = SMOOTHING_REPEATS  # integer number. Number of repeats

start_time_seconds = INTERVAL_START_TIME_SECONDS
end_time_seconds = INTERVAL_END_TIME_SECONDS
##########################

# Loads raw time series array (NxM) and sampling data
# N - number of time points
# M - number of cells
# loads all data except first column (time column)
data = np.loadtxt('preprocessing/filtered_data.txt')

start_time_frames = int(start_time_seconds*SAMPLING)
end_time_frames = int(end_time_seconds*SAMPLING)

time = [i/SAMPLING for i in range(len(data))]
smoothed_data = np.zeros((len(data), len(data[0])), float)

if not os.path.exists('preprocessing/smoothed_traces'):
    os.makedirs('preprocessing/smoothed_traces')

for i in range(len(data[0])):
    print(f'Smoothing time series {i}')

    fig, (ax1, ax2) = plt.subplots(2, 1)

    ax1.set_title(f'Cell {i}')
    ax1.plot(time, data[:, i], linewidth=0.5, color='dimgrey')
    ax1.set_title('Filtered data')
    ax1.set_xlim(start_time_seconds, end_time_seconds)
    ax1.set_ylabel('Signal (a.u.)')

    smoothed_data[:, i] = smooth_ts(data[:, i],
                                    number_of_points,
                                    number_of_smoothings)

    ax2.plot(time, smoothed_data[:, i], linewidth=0.5, color='dimgrey')
    ax2.set_title('Smoothed data')
    ax2.set_xlim(start_time_seconds, end_time_seconds)
    ax2.set_xlabel('time (s)')
    ax2.set_ylabel('Signal (a.u.)')

    plt.subplots_adjust(hspace=0.3)
    fig.savefig(
        f'preprocessing/smoothed_traces/smoothed_trace_{i}.png', dpi=200, bbox_inches='tight')
    plt.close(fig)

np.savetxt('preprocessing/smoothed_traces.txt', smoothed_data, fmt='%.3lf')
