"""
First responder cell identification
"""
# pylint: disable=C0103, C0411
# pylint: disable=W0719
# pylint: disable=W0611
# pylint: disable=R0915, R0914

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from methods.plot_configurations import PANEL_HEIGHT
from methods import plot_configurations
###Window size configurations


def first_responder_data(CONFIG_DATA: dict):
    """
    For determining first responder cells
    """
    EXPERIMENT_NAME = CONFIG_DATA['EXPERIMENT_NAME']
    FIRST_COLUMN_TIME = CONFIG_DATA['FIRST_COLUMN_TIME']
    SAMPLING = CONFIG_DATA['SAMPLING']

    if not os.path.exists(f'preprocessing/{EXPERIMENT_NAME}/first_responders'):
        os.makedirs(f'preprocessing/{EXPERIMENT_NAME}/first_responders')

    def on_click(event):
        """
        on-click event handler
        """
        if event.inaxes == ax:
            if event.button==plt.MouseButton.RIGHT:
                response_times[current_cell]=event.xdata
                plt.close(fig)

    def on_press(event):
        """
        On-press event handler
        """
        if str(event.key) == 'escape':
            sys.exit()
        if str(event.key) == 'left':
            if current_cell>=0:
                plt.close(fig)
        if str(event.key) == 'right':
            response_times[current_cell]=-1.0
            plt.close(fig)


    plt.rcParams['backend'] = 'TkAgg'
    plt.rcParams["figure.figsize"] = [8, 6]
    plt.rcParams["figure.autolayout"] = True

    data = np.loadtxt('raw_data/data.txt')
    if FIRST_COLUMN_TIME:
        data = data[:,1:]

    cell_num = len(data[0])
    time = [i/SAMPLING for i in range(len(data))]
    show_time = time[int(0.5*len(time))]

    response_times = np.zeros(cell_num, float)

    current_cell = 0
    for i in range(cell_num):
        current_cell = i
        fig = plt.figure()
        fig.canvas.mpl_connect('button_press_event', on_click)
        fig.canvas.mpl_connect('key_press_event', on_press)
        fig.canvas.manager.window.wm_geometry("+200+30")
        ax = fig.add_subplot(1,1,1)
        fig.suptitle(f'Cell {i}')
        ax.plot(time, data[:,i], linewidth=0.4, c='gray')
        ax.set_xlim(0,show_time)
        plt.show()

    np.savetxt(f'preprocessing/{EXPERIMENT_NAME}/first_responders/first_responder_times.txt',
               response_times, fmt='%.2lf')
    fig=plt.figure(figsize=(PANEL_HEIGHT, PANEL_HEIGHT))
    ax=fig.add_subplot(1,1,1)
    ax.boxplot(response_times, showfliers=False)
    ax.set_xticks([])
    ax.set_xlabel('')
    ax.set_ylabel('Response time (s)')

    fig.savefig(f'preprocessing/{EXPERIMENT_NAME}/first_responders/first_responder_times_boxplot.png',
                dpi=300, bbox_inches='tight')
    plt.close(fig)
