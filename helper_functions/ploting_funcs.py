"""
Helper functions for ploting data
"""
# pylint: disable=C0103
# pylint: disable=W0611

from typing import List
from matplotlib import colors
import numpy as np
import matplotlib.pyplot as plt
import plot_configurations

def binarized_plot(time: np.ndarray, binarized_signal: np.ndarray,
                   x_label: str = 'time (s)', y_label: str = 'cell i',
                   color_list: List[str] = None) -> plt.figure:
    """
    Creates binarized plot figure
    """

    if not color_list:
        color_list = ['white', 'red','black']

    cmap = colors.ListedColormap(color_list)
    bounds=[0,1,2]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.pcolormesh(time,np.arange(len(binarized_signal[0])),
                  np.transpose(binarized_signal),cmap=cmap,norm=norm)
    ax.set_xlim(0,np.amax(time))
    ax.set_ylim(0,len(binarized_signal[0]))
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    return fig
