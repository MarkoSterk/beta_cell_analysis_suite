"""
Module for coactivity calculation
"""

import numpy as np

def coactivity(binsig: np.ndarray) -> np.ndarray:
    """
    Calculates coactivity of cells based on binarized cellular activity
    """
    cell_num = len(binsig[0])

    ca_mat=np.zeros((cell_num,cell_num),float)
    for i in range(cell_num):
        ca_mat[i,i] = 1.0
        for ii in range(i):
            nact1 = np.sum(binsig[:,i])
            nact2 = np.sum(binsig[:,ii])
            nact = len(binsig[np.where((binsig[:,ii]==1) & (binsig[:,i]==1))])
            if (nact1>0 and nact2>0):
                ca_mat[i][ii]=nact/np.sqrt(nact1*nact2)
                ca_mat[ii][i]=ca_mat[i][ii]
    return ca_mat