"""
Graphic cell exclusion
"""
# pylint: disable=C0103, C0411
# pylint: disable=W0611, W0603, W0719
# pylint: disable=R0915, R0914

import os
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
from methods.plot_configurations import PANEL_HEIGHT, MEDIAN_PROPS, BOX_PROPS
from methods import plot_configurations

def pick_exclude_cells(CONFIG_DATA: dict,
                  smoothed_data: np.ndarray,
                  binerized_data: np.ndarray) -> list:
    """
    For excluding cells
    """
    matplotlib.use('TkAgg')

    current_cell = 0

    EXPERIMENT_NAME = CONFIG_DATA['EXPERIMENT_NAME']
    SAMPLING = CONFIG_DATA['SAMPLING']

    cell_num = len(smoothed_data[0])
    time = [i/SAMPLING for i in range(len(smoothed_data))]

    excluded_cells = []
    click_params = {
        'next_cell': None
    }
    if not os.path.exists(f'preprocessing/{EXPERIMENT_NAME}'):
        os.makedirs(f'preprocessing/{EXPERIMENT_NAME}')

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
                if len(excluded_cells)>0:
                    if cell-1==excluded_cells[-1]:
                        excluded_cells.pop()
                click_params['next_cell'] = cell-2
                plt.close()
        if str(event.key) == 'right':
            ###If the response time of this cell was not already set it sets the time to Nan
            ### and continous to the next cell
            ### else it just closes the figure and continous on.
            click_params['next_cell'] = cell
            plt.close()
        if str(event.key) in ['r', 'R']:
            ###Removes current cells (adds it to excluded_cells list)
            click_params['next_cell'] = cell
            excluded_cells.append(cell)
            plt.close()


    plt.rcParams['backend'] = 'TkAgg'
    plt.rcParams["figure.figsize"] = [10, 7]
    plt.rcParams["figure.autolayout"] = True

    while current_cell < cell_num:
        fig = plt.figure()
        fig.set_tight_layout(False)
        fig.canvas.mpl_connect('key_press_event', lambda event: on_press(event, current_cell))
        fig.suptitle(f'Cell {current_cell}')
        ax1 = fig.add_subplot(2,1,1)
        ax1.plot(time, smoothed_data[:,current_cell], linewidth=0.4, c='gray')
        ax1.plot(time, binerized_data[:,current_cell], linewidth=0.2, c='r')

        ax2 = fig.add_subplot(2,1,2)
        ax2.plot(time, smoothed_data[:,current_cell], linewidth=0.4, c='gray')
        ax2.plot(time, binerized_data[:,current_cell], linewidth=0.2, c='r')
        ax2.set_xlim(CONFIG_DATA['INTERVAL_START_TIME_SECONDS'], CONFIG_DATA['INTERVAL_END_TIME_SECONDS'])
        ax2.set_xlabel('time (s)')
        ax2.set_ylabel('Cell signal (a.u.)')
        plt.get_current_fig_manager().window.wm_geometry("+10+10") # move the window
        plt.show()
        current_cell = click_params['next_cell'] + 1
    plt.close()

    print('Cells excluded successfully.')
    return excluded_cells
