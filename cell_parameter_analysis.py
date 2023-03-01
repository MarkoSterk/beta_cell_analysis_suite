"""
Analysis of all cellular parameters
- relative active time 
- average oscillation frequency
- average oscillation duration
- interoscillation interval variability
"""

import numpy as np
import matplotlib.pyplot as plt
from helper_functions.cell_parameters import find_clusters
from configurations import (PANEL_HEIGHT, MEDIAN_PROPS, BOX_PROPS,
                            SMALL_TEXT_SIZE, MEDIUM_TEXT_SIZE, BIGGER_TEXT_SIZE)

################Matplotlib configurations#######################
plt.rc('font', size=SMALL_TEXT_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_TEXT_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_TEXT_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_TEXT_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_TEXT_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_TEXT_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_TEXT_SIZE)  # fontsize of the figure title
########################################################################

# SETTINGS
INTERVAL_START_TIME = 800.0
INTERVAL_END_TIME = 1800.0

# Loads all data
binarized_time_series = np.loadtxt(
    'preprocessing/results/final_binarized_data.txt')
sampling = np.loadtxt('raw_data/sampling.txt')

interval_start_time_frames = int(INTERVAL_START_TIME*sampling)
interval_end_time_frames = int(INTERVAL_END_TIME*sampling)

binarized_time_series = binarized_time_series[interval_start_time_frames:interval_end_time_frames,:]

cell_num = len(binarized_time_series[0])
time_series_length = len(binarized_time_series)

cell_data = {
    'relative_active_times': [],
    'oscillation_frequencies': [],
    'avg_oscillation_durations': [],
    'interoscillation_int_var': []
}

for i in range(cell_num):
    cell_data['relative_active_times'].append(
        np.sum(binarized_time_series[:, i])/time_series_length)

    activity_clusters = find_clusters(binarized_time_series[:, i])

    frequency = len(activity_clusters[0]) / \
        (INTERVAL_END_TIME-INTERVAL_START_TIME)
    cell_data['oscillation_frequencies'].append(frequency)

    cell_data['avg_oscillation_durations'].append(np.average(activity_clusters[1])/sampling)

    inactivity_clusters = find_clusters(
        binarized_time_series[:, i], trigger_val=0)

    avg_inactivity_duration = np.average(inactivity_clusters[1])/sampling
    inactivity_duration_std = np.std(inactivity_clusters[1])/sampling
    cell_data['interoscillation_int_var'].append(
        inactivity_duration_std/avg_inactivity_duration)

avg_islet_values = {key: {} for key in cell_data}
for key, value in cell_data.items():
    avg_islet_values[key]['avg'] = np.average(value)
    avg_islet_values[key]['std'] = np.std(value)

AVG_DATA_STRING = ' '.join([f'{avg_islet_values[key]["avg"]:.3f} {avg_islet_values[key]["std"]:.3f}'
                        for key in avg_islet_values])
with open('results/average_islet_activity_parameters.txt',
          'w', encoding='utf-8') as file:
    print('RelActTime RelActTimeSD OscFreq OscFreqSD AvgOscDur AvgOscDurSD IOIV IOIVSD', file=file)
    print(AVG_DATA_STRING, file=file)


with open('results/cellular_activity_parameters.txt',
          'w', encoding='utf-8') as file:
    print('RelActTime OscFreq AvgOscDur IOIV', file=file)
    for i in range(cell_num):
        act_time_i = cell_data['relative_active_times'][i]
        freq_i = cell_data['oscillation_frequencies'][i]
        dur_i = cell_data['avg_oscillation_durations'][i]
        ioiv_i = cell_data['interoscillation_int_var'][i]
        print(f'{act_time_i:.2f} {freq_i:.2f} {dur_i:.2f} {ioiv_i:.2f}', file=file)


number_of_panels = len(cell_data.keys())
COLS = 3
rows = int(number_of_panels/3)+1
fig = plt.figure(figsize=(COLS*PANEL_HEIGHT, rows*PANEL_HEIGHT))
axes = [fig.add_subplot(rows, COLS, int(i+1)) for i in range(COLS*rows) if i < number_of_panels]
for (key, value), ax in zip(cell_data.items(), axes):
    ax.boxplot([value], showfliers=False, patch_artist=True,
               medianprops=MEDIAN_PROPS, boxprops=BOX_PROPS)
    ax.set_ylabel(key)
    ax.set_xticks([])
plt.subplots_adjust(wspace=0.6, hspace=0.1)
fig.savefig('results/cell_parameters_box_plots.png', dpi=300, bbox_inches='tight', pad_inches=0.01)
plt.close(fig)
