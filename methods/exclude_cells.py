"""
Excludes all selected traces from the data set
"""
# pylint: disable=C0103
# pylint: disable=R0914
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from helper_functions.ploting_funcs import binarized_plot
from helper_functions.exclude_cells import pick_exclude_cells
from methods.plot_configurations import PANEL_WIDTH


def exclude_data(CONFIG_DATA: dict, smoothed_data: np.ndarray,
                 binarized_data: np.ndarray, pos: np.ndarray,
                 response_times: np.ndarray) -> tuple:
    """
    Excludes bad data
    """

    SAMPLING = CONFIG_DATA["SAMPLING"]
    EXPERIMENT_NAME = CONFIG_DATA["EXPERIMENT_NAME"]
    use_file = input('Use existing excluded cells file? (yes/no): ')
    excluded_cells = None
    if use_file.lower() == 'yes':
        excluded_cells = list(np.loadtxt(f'preprocessing/{EXPERIMENT_NAME}/excluded_cells.txt'))
        excluded_cells = set(excluded_cells) ##returns unordered collection of unique elements
        excluded_cells = list(excluded_cells) ##turns set to list type
        excluded_cells.sort() ##orders list of unique elements in ascending order
    else:
        excluded_cells = pick_exclude_cells(CONFIG_DATA, smoothed_data, binarized_data)
    ##Checks (and creates) folder structure
    if not os.path.exists(f'preprocessing/{EXPERIMENT_NAME}/results'):
        os.makedirs(f'preprocessing/{EXPERIMENT_NAME}/results')

    ###Calculates and sets necessary data and performs cell exclusions
    number_of_all_cells = len(smoothed_data[0])
    number_of_excluded_cells = len(excluded_cells)
    number_of_remaining_cells = number_of_all_cells - number_of_excluded_cells

    final_smoothed_data = np.zeros((len(smoothed_data), number_of_remaining_cells), float)
    final_binarized_data = np.zeros((len(binarized_data), number_of_remaining_cells), int)
    final_pos = np.zeros((number_of_remaining_cells, 2), float)
    final_response_times = np.zeros(number_of_remaining_cells, float)

    all_cell_indexes = list(range(number_of_all_cells))
    remaining_cell_indexes = list(set(all_cell_indexes).difference(set(list(excluded_cells))))

    final_smoothed_data[:,:] = smoothed_data[:,remaining_cell_indexes]
    final_binarized_data[:,:] = binarized_data[:,remaining_cell_indexes]
    final_pos[:,:] = pos[remaining_cell_indexes,:]
    if response_times is not None:
        final_response_times[:] = response_times[remaining_cell_indexes]

    time = [i/SAMPLING for i in range(len(final_binarized_data))]
    
    fig = plt.figure(figsize=(PANEL_WIDTH, 1.5*PANEL_WIDTH))
    gs = gridspec.GridSpec(2, 1, height_ratios=[1, 4])
    ax1 = fig.add_subplot(gs[0])
    ax1.set_title('Mean-field Ca$^{2+}$ signal')
    ax1.plot(time, np.average(final_smoothed_data, axis=1), c='gray', linewidth=0.5)
    ax1.set_xticks([])
    
    ax2 = fig.add_subplot(gs[1])
    norm_traces = np.zeros(final_smoothed_data.shape, float)
    for i in range(len(final_pos)):
        vmin, vmax = np.amin(final_smoothed_data[:,i]), np.amax(final_smoothed_data[:,i])
        norm_traces[:,i] = (final_smoothed_data[:,i]-vmin)/(vmax-vmin)
        ax2.plot(time, norm_traces[:,i]+i*0.5, linewidth=0.3)
    ax2.set_xlabel('time (s)')
    ax2.set_ylabel('Cell signal $i$')
    plt.subplots_adjust(wspace=0.05, hspace=0.05)
    fig.savefig(f'preprocessing/{EXPERIMENT_NAME}/results/final_all_traces.png',
                dpi=600, bbox_inches='tight', pad_inches=0.01)
    plt.close(fig)

    ##Saves final data
    np.savetxt(f'preprocessing/{EXPERIMENT_NAME}/results/final_smoothed_traces.txt',
            final_smoothed_data, fmt='%.3lf')
    np.savetxt(f'preprocessing/{EXPERIMENT_NAME}/results/final_binarized_traces.txt',
            final_binarized_data, fmt='%d')
    np.savetxt(f'preprocessing/{EXPERIMENT_NAME}/results/final_coordinates.txt',
            final_pos, fmt='%.1lf')
    if response_times is not None:
        np.savetxt(f'preprocessing/{EXPERIMENT_NAME}/results/final_first_responder_times.txt',
                final_response_times, fmt='%.1lf')

    fig = binarized_plot(time, final_binarized_data, final_pos)
    fig.savefig(f'preprocessing/{EXPERIMENT_NAME}/results/final_raster_plot.png',
                dpi=200,bbox_inches = 'tight')
    plt.close(fig)

    np.savetxt(f'preprocessing/{EXPERIMENT_NAME}/excluded_cells.txt',
               excluded_cells, fmt='%d')

    if response_times is None:
        final_response_times = None

    # pylint: disable-next=C0301
    print(f'Finished. {len(excluded_cells)} cells were excluded and {len(final_pos)} cells are remaining.')
    print('WARNING: Set new time interval for further analysis!')
    return final_smoothed_data, final_binarized_data, final_pos, final_response_times
