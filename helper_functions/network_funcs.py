"""
Network helper functions
"""
# pylint: disable=C0116
# pylint: disable=C0121
# pylint: disable=C0103
# pylint: disable=C0325
# pylint: disable=C0200

import random
import numpy as np
import networkx as nx
from networkx.generators.random_graphs import fast_gnp_random_graph
from helper_functions import community

def efficiency(G):
    avg = 0.0
    n = len(G)
    for i in range(len(G)):
        for j in range(i+1, len(G), 1):
            if nx.has_path(G, i, j) == True:
                avg += 1.0/nx.dijkstra_path_length(G, i, j)
    if n > 0.0:
        avg = avg*2.0/(n*(n-1))
    else:
        avg = avg/1.0
    return avg


def avg_deg(G):
    avg = 0
    n = len(G)
    for i in range(n):
        avg += G.degree(i)
    return (float(avg)/float(n))


def avg_cluss(G):
    clustering = nx.clustering(G)
    avg = 0.0
    n = len(G)
    for i in range(n):
        avg = avg+clustering[i]
    return (avg/float(n))


def max_struc(G):
    n = len(G)
    i = 0
    j = 0
    S_max = 0
    for i in range(n):
        S = 0
        for j in range(n):
            if nx.has_path(G, i, j):
                S += 1.0
        if S_max < S:
            S_max = S
    return S_max


def commstructure(G):
    skupnost = np.zeros(len(G), int)
    if G.number_of_edges() > 0:
        partition = community.best_partition(G)
        Q = community.modularity(partition, G)
    else:
        partition = np.zeros([len(G)], float)
        Q = 0.0
    cc_d = 1
    for i in range(len(G)):
        partition[i] = partition[i]+1
    for i in range(len(G)):
        if G.degree(i) < 1:
            partition[i] = 0
        skupnost[i] = partition[i]
    a = sorted(skupnost)
    test = 0
    test_c = 0
    vrednost = {}
    for i in range(len(a)):
        if int(a[i] > 0) and int(a[i]) != test:
            test = int(a[i])
            vrednost[test_c] = int(a[i])
            test_c += 1
    test_c += 1

    for i in range(len(a)):
        for j in range(len(vrednost)):
            if vrednost[j] == skupnost[i]:
                skupnost[i] = j+1
    maxmax = max(skupnost)
    return (maxmax, Q, skupnost)


def fixed_kavg_conn_mat(R: np.ndarray, k_avg: float, step_th: float = 0.0001,
                tries_th: int = 10000, tolerance: float = 0.20) -> np.ndarray:
    """
    Calculates network with fixed average node degree
    """
    conn_mat = np.zeros((len(R), len(R)), int)
    conn_th = np.average(R)

    for i in range(len(R)):
        R[i,i]=1.0

    tries = 0
    while tries < tries_th:
        conn_mat[:,:] = 0
        conn_mat[np.where((R > conn_th) & (R < 1.0))] = 1
        avg = np.sum(conn_mat)/len(R)

        if (avg < (1.0-tolerance)*k_avg):
            conn_th = conn_th-step_th
        elif (avg > (1.0+tolerance)*k_avg):
            conn_th = conn_th+step_th
        else:
            return conn_mat

        tries += 1

    raise BaseException(f"""Could not construct network with desired Kvg={k_avg}.
                    Last threshold is {conn_th}.""")


def fixed_rth_conn_mat(R: np.ndarray, Rth: float) -> np.ndarray:
    """
    Calculates fixed correlation threshold connectivity matrix
    """
    conn_mat = np.zeros(R.shape, int)
    for i in range(len(R)):
        for j in range(i):
            if R[i,j]>Rth:
                conn_mat[i,j] = 1
                conn_mat[j,i] = 1

    return conn_mat

def connection_lengths(G: nx.Graph, pos: np.ndarray) -> np.ndarray:
    lengths = []
    for i in range(len(G)):
        for j in range(i):
            if G.has_edge(i,j):
                distance = np.sqrt((pos[i,0]-pos[j,0])**2+(pos[i,1]-pos[j,1])**2)
                lengths.append(distance)
    return lengths

def get_graph_connections(graph: nx.Graph, undirected=True) -> list:
    """
    Extracts all connections from graph and returns list of tuples [(i,j)]
    """
    edges = []
    cell_num = len(graph)
    for i in range(cell_num):
        for j in range(i):
            if graph.has_edge(i,j):
                edges.append((i,j))
                if undirected:
                    edges.append((j,i))
    return edges


def small_world_coefficient(G: nx.Graph) -> float:
    avg_k = avg_deg(G)

    p=(len(G)*avg_k)/(len(G)*(len(G)-1))
    random_G = fast_gnp_random_graph(len(G), p)

    random_clust = avg_cluss(random_G)
    graph_clust = avg_cluss(G)

    graph_efficiency = efficiency(G)
    random_efficiency = efficiency(random_G)
    #print(graph_efficiency, random_efficiency)
    try:
        graph_avg_length = 1.0/graph_efficiency
    except ZeroDivisionError:
        graph_avg_length = 10.0
    try:
        random_avg_length = 1.0/random_efficiency
    except ZeroDivisionError:
        random_avg_length = 10.0
    SW = 0.0
    try:
        SW = (graph_clust/random_clust)/(graph_avg_length/random_avg_length)
    except ZeroDivisionError:
        SW = 0.0
    return SW


def construct_graph_from_conn_mat(cmat: np.ndarray) -> nx.Graph:
    """
    Creates a graph from a binarized connectivity matrix 
    """
    cell_num = len(cmat)
    G = nx.Graph()
    for i in range(cell_num):
        G.add_node(i)

    for i in range(cell_num):
        for j in range(i):
            if i!=j and cmat[i,j]==1:
                G.add_edge(i,j)

    return G


def calculate_hindex(G: nx.Graph, n: int) -> int:
    """
    Calculates the Hirsher-index of node n in graph G
    """
    sorted_neighbor_degrees = sorted((G.degree(v) for v in G.neighbors(n)), reverse=True)
    h = 0
    for i in range(1, len(sorted_neighbor_degrees)+1):
        if sorted_neighbor_degrees[i-1] < i:
            break
        h = i

    return h
