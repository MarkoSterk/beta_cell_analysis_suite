"""
Functions for calculating different cell parameters
"""

import numpy as np

def find_clusters(cell_array, trigger_val: int = 1, stopind_inclusive: bool = True):
    """
    Finds clusters of values in provided array based on trigger value.
    Trigger value is by default set to 1 (for binarized activity arrays) when
    searching for activity (1)
    """
    # Setup "sentients" on either sides to make sure we have setup
    # "ramps" to catch the start and stop for the edges of activity
    # (left-most and right-most activity edge) respectively
    y_ext = np.r_[False,cell_array==trigger_val, False]

    # Get indices of shifts, which represent the start and stop indices
    idx = np.flatnonzero(y_ext[:-1] != y_ext[1:])

    # Lengths of activity if needed
    lens = idx[1::2] - idx[:-1:2]

    # Using a stepsize of 2 would get us start and stop indices for each island
    return list(zip(idx[:-1:2], idx[1::2]-int(stopind_inclusive))), lens
