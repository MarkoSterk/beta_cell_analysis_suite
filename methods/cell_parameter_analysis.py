"""
Analysis of all cellular parameters
- relative active time 
- average oscillation frequency
- average oscillation duration
- interoscillation interval variability
"""
# pylint: disable=W0611
# pylint: disable=C0103
# pylint: disable=R0914
import os
import numpy as np
import matplotlib.pyplot as plt
from helper_functions.cell_parameters import find_clusters
from methods import plot_configurations
from methods.plot_configurations import PANEL_HEIGHT, MEDIAN_PROPS, BOX_PROPS

def cell_activity_data(CONFIG_DATA: dict, binarized_time_series: np.array):
    """
    Performs cell activity parameter analysis
    """
    INTERVAL_START_TIME_SECONDS = CONFIG_DATA["INTERVAL_START_TIME_SECONDS"]
    INTERVAL_END_TIME_SECONDS = CONFIG_DATA["INTERVAL_END_TIME_SECONDS"]
    SAMPLING = CONFIG_DATA["SAMPLING"]
    EXPERIMENT_NAME = CONFIG_DATA["EXPERIMENT_NAME"]

    if not os.path.exists(f'results/{EXPERIMENT_NAME}'):
        os.makedirs(f'results/{EXPERIMENT_NAME}')

    sampling = SAMPLING

    interval_start_time_frames = int(INTERVAL_START_TIME_SECONDS*sampling)
    interval_end_time_frames = int(INTERVAL_END_TIME_SECONDS*sampling)

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
        frequency = np.nan
        osc_dur = np.nan
        if len(activity_clusters[1])>0:
            frequency = len(activity_clusters[0]) / \
                (INTERVAL_END_TIME_SECONDS-INTERVAL_START_TIME_SECONDS)
            osc_dur = np.average(activity_clusters[1])/sampling

        cell_data['oscillation_frequencies'].append(frequency)
        cell_data['avg_oscillation_durations'].append(osc_dur)

        inactivity_clusters = find_clusters(
            binarized_time_series[:, i], trigger_val=0)

        avg_inactivity_duration = np.nan
        inactivity_duration_std = np.nan
        if len(inactivity_clusters[1] > 2):
            inactivity_duration_std = np.std(inactivity_clusters[1])/sampling
            avg_inactivity_duration = np.average(inactivity_clusters[1])/sampling

        intosc_int_var = np.nan
        if np.nan not in (inactivity_duration_std, avg_inactivity_duration):
            intosc_int_var = inactivity_duration_std/avg_inactivity_duration
        cell_data['interoscillation_int_var'].append(intosc_int_var)

    avg_islet_values = {key: {} for key in cell_data}
    for key, value in cell_data.items():
        avg_islet_values[key]['avg'] = np.nanmean(value)
        avg_islet_values[key]['std'] = np.nanstd(value)

    AVG_DATA_STRING = ' '.join([f'{avg_islet_values[key]["avg"]:.4f} {avg_islet_values[key]["std"]:.4f}'
                            for key in avg_islet_values])
    with open(f'results/{EXPERIMENT_NAME}/average_islet_activity_parameters.txt',
            'w', encoding='utf-8') as file:
        print('RelActTime RelActTimeSD OscFreq OscFreqSD AvgOscDur AvgOscDurSD IOIV IOIVSD', file=file)
        print(AVG_DATA_STRING, file=file)


    with open(f'results/{EXPERIMENT_NAME}/cellular_activity_parameters.txt',
            'w', encoding='utf-8') as file:
        print('RelActTime OscFreq AvgOscDur IOIV', file=file)
        for i in range(cell_num):
            act_time_i = cell_data['relative_active_times'][i]
            freq_i = cell_data['oscillation_frequencies'][i]
            dur_i = cell_data['avg_oscillation_durations'][i]
            ioiv_i = cell_data['interoscillation_int_var'][i]
            print(f'{act_time_i:.4f} {freq_i:.4f} {dur_i:.4f} {ioiv_i:.4f}', file=file)


    number_of_panels = len(cell_data.keys())
    COLS = number_of_panels
    rows = 1
    fig = plt.figure(figsize=(COLS*PANEL_HEIGHT, rows*PANEL_HEIGHT))
    axes = [fig.add_subplot(rows, COLS, int(i+1)) for i in range(COLS*rows) if i < number_of_panels]
    for (key, value), ax in zip(cell_data.items(), axes):
        ax.boxplot([val for val in value if np.isfinite(val)], showfliers=False, patch_artist=True,
                medianprops=MEDIAN_PROPS, boxprops=BOX_PROPS)
        ax.set_ylabel(key)
        ax.set_xticks([])
    plt.subplots_adjust(wspace=0.6, hspace=0.1)
    fig.savefig(f'results/{EXPERIMENT_NAME}/cell_parameters_box_plots.png',
                dpi=300, bbox_inches='tight', pad_inches=0.01)
    plt.close(fig)

    print('Cell parameter analysis finished successfully.')
