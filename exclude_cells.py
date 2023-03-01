"""
Excludes all selected traces from the data set
"""
# pylint: disable=C0103
import os
import numpy as np
import matplotlib.pyplot as plt
from helper_functions.ploting_funcs import binarized_plot
from configurations import SAMPLING, EXCLUDE_CELLS

##Loads all necessary data
smoothed_data = np.loadtxt('preprocessing/smoothed_traces.txt')
binarized_data = np.loadtxt('preprocessing/binarized_traces.txt', dtype=int)
pos = np.loadtxt('raw_data/koordinate.txt')
excluded_cells = EXCLUDE_CELLS

###Calculates and sets necessary data and performs cell exclusions
number_of_all_cells = len(smoothed_data[0])
number_of_excluded_cells = len(excluded_cells)
number_of_remaining_cells = number_of_all_cells - number_of_excluded_cells

final_smoothed_data = np.zeros((len(smoothed_data), number_of_remaining_cells), float)
final_binarized_data = np.zeros((len(binarized_data), number_of_remaining_cells), int)
final_pos = np.zeros((number_of_remaining_cells, 2), float)

all_cell_indexes = list(range(number_of_all_cells))
remaining_cell_indexes = list(set(all_cell_indexes).difference(set(list(excluded_cells))))

final_smoothed_data[:,:] = smoothed_data[:,remaining_cell_indexes]
final_binarized_data[:,:] = binarized_data[:,remaining_cell_indexes]
final_pos[:,:] = pos[remaining_cell_indexes,:]

time = [i/SAMPLING for i in range(len(final_binarized_data))]

##Checks (and creates) folder structure
if not os.path.exists('preprocessing/results'):
    os.makedirs('preprocessing/results')

##Saves final data
np.savetxt('preprocessing/results/final_smoothed_data.txt', final_smoothed_data, fmt='%.3lf')
np.savetxt('preprocessing/results/final_binarized_data.txt', final_binarized_data, fmt='%d')
np.savetxt('preprocessing/results/final_coordinates.txt', final_pos, fmt='%.1lf')

fig = binarized_plot(time, final_binarized_data)
fig.savefig('preprocessing/results/final_raster_plot.png',dpi=200,bbox_inches = 'tight')
plt.close(fig)
