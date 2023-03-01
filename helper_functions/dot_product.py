"""
Dot product method for time series similarity calculation
Result is the same as coactivity
"""

import numpy as np

def vector_squared(vec: np.ndarray) -> np.ndarray:
    """
    calculates the square of a vector
    """
    return vec*vec

def components_sum(vec: np.ndarray) -> float:
    """
    Returns sum of components
    """
    return np.sum(vec)

def norm_vector(vec: np.ndarray) -> np.ndarray:
    """
    returns normalized vector
    """
    square_vec = vector_squared(vec)
    sum_of_square = components_sum(square_vec)
    vec_size = np.sqrt(sum_of_square)
    return vec/vec_size

def calculate_dot_product(data: np.ndarray) -> np.ndarray:
    """
    Calculates dot product for each time series pair
    """
    cell_num = len(data[0])
    sim_mat = np.zeros((cell_num, cell_num), float)
    for i in range(cell_num):
        sim_mat[i,i] = 1
        vec_1 = norm_vector(data[:,i])
        for j in range(i):
            vec_2 = norm_vector(data[:,j])
            sim_mat[i,j] = np.dot(vec_1, vec_2)
            sim_mat[j,i] = sim_mat[i,j]

    return sim_mat
