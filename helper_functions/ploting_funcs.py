"""
Helper functions for ploting data
"""
# pylint: disable=C0103
# pylint: disable=W0611

from typing import List
from matplotlib import colors
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import rankdata
import methods.plot_configurations as plot_configurations

def binarized_plot(time: np.ndarray, binarized_signal: np.ndarray, pos: np.ndarray,
                   x_label: str = 'time (s)', y_label: str = 'distance from origin/cell i',
                   color_list: List[str] = None) -> plt.figure:
    """
    Creates binarized plot figure
    """
    distance_from_origin = np.array([np.sqrt((pos[i,0])**2+(pos[i,1])**2) for i in range(len(pos))])
    distance_ranks = rankdata(distance_from_origin, method = 'ordinal') - 1
    ranked_bin_signal = np.zeros(binarized_signal.shape, int)
    for i, rank in enumerate(distance_ranks):
        ranked_bin_signal[:,i] = binarized_signal[:,rank]

    if not color_list:
        color_list = ['white', 'red','black']

    cmap = colors.ListedColormap(color_list)
    bounds=[0,1,2]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.pcolormesh(time,np.arange(len(ranked_bin_signal[0])),
                  np.transpose(ranked_bin_signal),cmap=cmap,norm=norm)
    ax.set_xlim(0,np.amax(time))
    ax.set_ylim(0,len(ranked_bin_signal[0]))
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    return fig
