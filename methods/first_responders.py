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
from methods.plot_configurations import PANEL_HEIGHT, MEDIAN_PROPS, BOX_PROPS
from methods import plot_configurations

current_cell = 0

def first_responder_data(CONFIG_DATA: dict, data: np.array):
    """
    For determining first responder cells
    """
    global current_cell
    EXPERIMENT_NAME = CONFIG_DATA['EXPERIMENT_NAME']
    FIRST_COLUMN_TIME = CONFIG_DATA['FIRST_COLUMN_TIME']
    SAMPLING = CONFIG_DATA['SAMPLING']

    if FIRST_COLUMN_TIME:
        data = data[:,1:40]
    
    cell_num = len(data[0])
    time = [i/SAMPLING for i in range(len(data))]
    show_time = time[int(0.5*len(time))]

    response_times = np.zeros(cell_num, float)

    if not os.path.exists(f'preprocessing/{EXPERIMENT_NAME}/first_responders'):
        os.makedirs(f'preprocessing/{EXPERIMENT_NAME}/first_responders')

    def on_click(event):
        """
        on-click event handler
        """
        if event.inaxes == ax:
            if event.button==plt.MouseButton.RIGHT:
                response_times[current_cell]=event.xdata
                plt.close()

    def on_press(event):
        """
        On-press event handler
        """
        global current_cell
        if str(event.key) == 'escape':
            ###Exits the whole thing
            sys.exit()
        if str(event.key) == 'left':
            ###If the current cell is not the first (0)
            ###the cell counter is turned back. It gets turned back by 2
            ###because it gets increased again by one in the main while
            ### loop after the figure closes
            if current_cell > 0:
                current_cell-=2
                plt.close()
        if str(event.key) == 'right':
            ###Sets response time of current cell to NaN if it wasn't set before
            if response_times[current_cell] == 0.0:
                response_times[current_cell]=np.nan
        if str(event.key) in ['r', 'R']:
            ###Sets a previously clicked cell back to NaN
            response_times[current_cell] = np.nan
            plt.close()


    plt.rcParams['backend'] = 'TkAgg'
    plt.rcParams["figure.figsize"] = [8, 6]
    plt.rcParams["figure.autolayout"] = True

    while current_cell < cell_num:
        fig = plt.figure()
        fig.canvas.mpl_connect('button_release_event', on_click)
        fig.canvas.mpl_connect('key_press_event', on_press)
        ax = fig.add_subplot(1,1,1)
        fig.suptitle(f'Cell {current_cell}')
        ax.plot(time, data[:,current_cell], linewidth=0.4, c='gray')
        ax.set_xlim(0,show_time)
        plt.show()
        current_cell+=1
    plt.close()
    np.savetxt(f'preprocessing/{EXPERIMENT_NAME}/first_responders/first_responder_times.txt',
               response_times, fmt='%.2lf')
    fig=plt.figure(figsize=(PANEL_HEIGHT, PANEL_HEIGHT))
    ax=fig.add_subplot(1,1,1)
    ax.boxplot(response_times,
               showfliers=False, patch_artist=True,
               medianprops=MEDIAN_PROPS, boxprops=BOX_PROPS)
    ax.set_xticks([])
    ax.set_xlabel('')
    ax.set_ylabel('Response time (s)')

    #pylint: disable-next=C0301
    fig.savefig(f'preprocessing/{EXPERIMENT_NAME}/first_responders/first_responder_times_boxplot.png',
                dpi=300, bbox_inches='tight')
    plt.close(fig)
