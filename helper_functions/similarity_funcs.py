"""
Functions for similarity calculations
"""
import numpy as np

def jaccard_similarity(edges_i: list, edges_j: list) -> float:
    """
    Calculates jaccard similarity of two sets
    """
    set_i = set(edges_i)
    set_j = set(edges_j)
    return (len(set_i.intersection(set_j)))/(len(set_i.union(set_j)))


def degree_correlation(degree_i: list, degree_j: list) -> float:
    """
    Calculates degree correlation between networks
    """
    cell_num = len(degree_i)

    avg_degree_i = np.average(degree_i)
    std_degree_i = np.std(degree_i)

    avg_degree_j = np.average(degree_j)
    std_degree_j = np.std(degree_j)

    corr = 0.0
    for i in range(cell_num):
        corr += ((degree_i[i]-avg_degree_i)*(degree_j[i]-avg_degree_j))/(std_degree_i*std_degree_j)
    corr=corr/cell_num
    return corr
