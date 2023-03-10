"""
Time series smoothing
"""
# pylint: disable=C0103
# pylint: disable=W0611
# pylint: disable=R0914

import os
import numpy as np
import matplotlib.pyplot as plt
from helper_functions.smoothing import smooth_ts
from helper_functions.utility_functions import print_progress_bar
from methods import plot_configurations

def smooth_data(CONFIG_DATA: dict, data: np.array) -> np.array:
    """
    Smooths time series data
    """
    SAMPLING = CONFIG_DATA['SAMPLING']
    INTERVAL_START_TIME_SECONDS = CONFIG_DATA['INTERVAL_START_TIME_SECONDS']
    INTERVAL_END_TIME_SECONDS = CONFIG_DATA['INTERVAL_END_TIME_SECONDS']
    SMOOTHING_POINTS = CONFIG_DATA['SMOOTHING_POINTS']
    SMOOTHING_REPEATS = CONFIG_DATA['SMOOTHING_REPEATS']
    EXPERIMENT_NAME = CONFIG_DATA['EXPERIMENT_NAME']
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
    #data = np.loadtxt(f'preprocessing/{EXPERIMENT_NAME}/filtered_data.txt')
    cell_num = len(data[0]) #number of cells

    time = [i/SAMPLING for i in range(len(data))]
    smoothed_data = np.zeros((len(data), len(data[0])), float)

    if not os.path.exists(f'preprocessing/{EXPERIMENT_NAME}/smoothed_traces'):
        os.makedirs(f'preprocessing/{EXPERIMENT_NAME}/smoothed_traces')

    for i in range(cell_num):
        print_progress_bar(i+1, cell_num, f'Smoothing time series {i} ')

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
            f'preprocessing/{EXPERIMENT_NAME}/smoothed_traces/smoothed_trace_{i}.png',
            dpi=200, bbox_inches='tight')
        plt.close(fig)

    np.savetxt(f'preprocessing/{EXPERIMENT_NAME}/smoothed_traces.txt', smoothed_data, fmt='%.3lf')
    return smoothed_data
