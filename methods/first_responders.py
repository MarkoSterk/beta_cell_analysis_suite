"""
First responder cell identification
"""
# pylint: disable=C0103, C0411
# pylint: disable=W0611, W0603, W0719
# pylint: disable=R0915, R0914

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
from methods.plot_configurations import PANEL_HEIGHT, MEDIAN_PROPS, BOX_PROPS
from methods import plot_configurations


def first_responder_data(CONFIG_DATA: dict, data: np.ndarray):
    """
    For determining first responder cells
    """
    current_cell = 0
    EXPERIMENT_NAME = CONFIG_DATA['EXPERIMENT_NAME']
    SAMPLING = CONFIG_DATA['SAMPLING']

    norm_data = np.zeros(data.shape, float)
    cell_num = len(data[0])
    for i in range(cell_num):
        vmin, vmax = np.amin(data[:,i]), np.amax(data[:,i])
        norm_data[:,i] = (data[:,i]-vmin)/(vmax-vmin)
    time = [i/SAMPLING for i in range(len(data))]
    show_time_start = CONFIG_DATA['INTERVAL_START_TIME_SECONDS']
    show_time_end = CONFIG_DATA['INTERVAL_END_TIME_SECONDS']

    response_times = np.zeros(cell_num, float)
    
    click_params = {
        'next_cell': None
    }

    if not os.path.exists(f'preprocessing/{EXPERIMENT_NAME}'):
        os.makedirs(f'preprocessing/{EXPERIMENT_NAME}')

    def on_click(event, cell):
        """
        on-click event handler
        """
        if event.inaxes == ax:
            if event.button==plt.MouseButton.RIGHT:
                response_times[cell]=event.xdata
                click_params['next_cell'] = cell
                plt.close()

    def on_press(event, cell):
        """
        On-press event handler
        """
        if str(event.key) == 'escape':
            ###Exits the whole thing
            sys.exit()
        if str(event.key) == 'left':
            ###If the current cell is not the first (0)
            ###the cell counter is turned back. It gets turned back by 2
            ###because it gets increased again by one in the main while
            ### loop after the figure closes
            if cell > 0:
                click_params['next_cell'] = cell-2
                plt.close()
        if str(event.key) == 'right':
            ###If the response time of this cell was not already set it sets the time to Nan
            ### and continous to the next cell
            ### else it just closes the figure and continous on.
            if response_times[cell] == 0.0:
                response_times[cell] = np.nan
            click_params['next_cell'] = cell
            plt.close()
        if str(event.key) in ['r', 'R']:
            ###Sets response time to NaN
            response_times[cell] = np.nan
            click_params['next_cell'] = cell
            plt.close()


    plt.rcParams['backend'] = 'TkAgg'
    plt.rcParams["figure.figsize"] = [10, 7]
    plt.rcParams["figure.autolayout"] = True

    while current_cell < cell_num:
        fig = plt.figure()
        fig.set_tight_layout(False)
        fig.canvas.mpl_connect('button_release_event', lambda event: on_click(event, current_cell))
        fig.canvas.mpl_connect('key_press_event', lambda event: on_press(event, current_cell))
        ax = fig.add_subplot(1,1,1)
        # pylint: disable-next=W0612
        cursor = Cursor(ax, horizOn=True, vertOn=True, color='green', linewidth=1.0, useblit=True)
        fig.suptitle(f'Cell {current_cell}')
        ax.plot(time, norm_data[:,current_cell], linewidth=0.4, c='gray')
        ax.set_xlim(show_time_start, show_time_end)
        ax.set_xlabel('time (s)')
        ax.set_ylabel('Cell signal (a.u.)')
        ax.set_ylim(-0.1, 1.1)
        plt.get_current_fig_manager().window.wm_geometry("+10+10") # move the window
        plt.show()
        current_cell = click_params['next_cell'] + 1
    plt.close()
    np.savetxt(f'preprocessing/{EXPERIMENT_NAME}/first_responder_times.txt',
               response_times, fmt='%.2lf')

    valid_times = response_times[~np.isnan(response_times)]
    fig=plt.figure(figsize=(PANEL_HEIGHT, PANEL_HEIGHT))
    ax=fig.add_subplot(1,1,1)
    ax.boxplot([valid_times],
               showfliers=False, patch_artist=True,
               medianprops=MEDIAN_PROPS, boxprops=BOX_PROPS)
    ax.set_xticks([])
    ax.set_xlabel('')
    ax.set_ylabel('Response time (s)')

    #pylint: disable-next=C0301
    fig.savefig(f'preprocessing/{EXPERIMENT_NAME}/first_responder_times_boxplot.png',
                dpi=300, bbox_inches='tight')
    plt.close(fig)

    print('First responder analysis finished successfully.')
    return response_times
