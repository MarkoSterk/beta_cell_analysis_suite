"""
Correlation analysis of islet
"""
# pylint: disable=C0103
# pylint: disable=W0719
# pylint: disable=W0611
# pylint: disable=R0915, R0914

import os
import matplotlib
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from networkx.algorithms import clustering
from helper_functions.network_funcs import (fixed_kavg_conn_mat,
                                            fixed_rth_conn_mat,
                                            construct_graph_from_conn_mat,
                                            efficiency,
                                            avg_deg,
                                            avg_cluss,
                                            max_struc,
                                            small_world_coefficient,
                                            commstructure, calculate_hindex)
from helper_functions.coactivity import coactivity
from methods.plot_configurations import PANEL_WIDTH, PANEL_HEIGHT
from methods import plot_configurations

def corr_ca_analysis_data(CONFIG_DATA: dict, time_series: np.array, pos: np.array):
    """
    Performs the correlation/coactivity network analysis
    """
    SAMPLING = CONFIG_DATA["SAMPLING"]
    INTERVAL_START_TIME_SECONDS = CONFIG_DATA["INTERVAL_START_TIME_SECONDS"]
    INTERVAL_END_TIME_SECONDS = CONFIG_DATA["INTERVAL_END_TIME_SECONDS"]
    ANALYSIS_TYPE = CONFIG_DATA["ANALYSIS_TYPE"]
    NETWORK_METHOD = CONFIG_DATA["NETWORK_METHOD"]
    CONNECTIVITY_LEVEL = CONFIG_DATA["CONNECTIVITY_LEVEL"]
    FIXED_KAVG_TOLERANCE = CONFIG_DATA["FIXED_KAVG_TOLERANCE"]
    EXPERIMENT_NAME = CONFIG_DATA["EXPERIMENT_NAME"]
    ############################################
    ###### Settings#################
    analysis_type = ANALYSIS_TYPE
    interval_start_seconds: float = INTERVAL_START_TIME_SECONDS
    interval_end_seconds: float = INTERVAL_END_TIME_SECONDS

    #Select network construction method
    network_method = NETWORK_METHOD
    threshold_level = CONNECTIVITY_LEVEL

    ##############END OF SETTINGS#################
    ##############################################


    #############DON'T CHANGE ANYTHING
    ###Loads data
    # time_series = None
    # if analysis_type == 'correlation':
    #     time_series = np.loadtxt(f'preprocessing/{EXPERIMENT_NAME}/results/final_smoothed_data.txt')
    # elif analysis_type == 'coactivity':
    #     time_series = np.loadtxt(f'preprocessing/{EXPERIMENT_NAME}/results/final_binarized_data.txt'
    #                              )
    # else:
    #     raise BaseException('Please select a valid analysis type (analysis_type).')

    # pos = np.loadtxt(f'preprocessing/{EXPERIMENT_NAME}/results/final_coordinates.txt')

    ##Calculates necessary parameters/data
    interval_start_frames = int(interval_start_seconds*SAMPLING)
    interval_end_frames = int(interval_end_seconds*SAMPLING)
    cell_num = len(pos)
    ###Performs analysis

    ##Uses either correlation or coactivity method for time series similarity measure.
    corr_matrix = None
    if analysis_type == 'correlation':
        corr_matrix = np.corrcoef(time_series[interval_start_frames:interval_end_frames,:],
                            rowvar=False)
    elif analysis_type == 'coactivity':
        corr_matrix = coactivity(time_series)
    else:
        raise BaseException('Correlation/coactivity was not calculated. Check Analysis type (analysis_type).')

    if not os.path.exists(f'results/{EXPERIMENT_NAME}/{analysis_type}_analysis/{network_method}'):
        os.makedirs(f'results/{EXPERIMENT_NAME}/{analysis_type}_analysis/{network_method}')

    conn_mat = None
    conn_th = 0
    if network_method == 'fixed_rth':
        conn_mat = fixed_rth_conn_mat(corr_matrix, threshold_level)
        conn_th = threshold_level
    elif network_method == 'fixed_kavg':
        conn_mat, Rth = fixed_kavg_conn_mat(corr_matrix, threshold_level, tolerance=FIXED_KAVG_TOLERANCE)
        conn_th = Rth
    else:
        raise BaseException('Please select a valid network construction method (network_method).')

    G = construct_graph_from_conn_mat(conn_mat)
    avg_corr_label = 'avgCorr' if analysis_type == 'correlation' else 'avgCA'
    avg_corr = np.average(corr_matrix)
    avg_eff = efficiency(G)
    avg_k = avg_deg(G)
    avg_c = avg_cluss(G)
    s_max = max_struc(G)/cell_num
    sw_coef = small_world_coefficient(G)
    assortativity = nx.algorithms.degree_assortativity_coefficient(G)
    num_comm, Q, communities = commstructure(G)
    node_sizes = [np.sqrt(G.degree(i))+3.0 for i in range(cell_num)]
    node_colors = []
    cmap = cm.get_cmap('jet')
    for i in range(cell_num):
        if G.degree(i) == 0:
            node_colors.append('lightgray')
        else:
            # will return rgba, we take only first 3 so we get rgb
            rgb = cmap(communities[i]/np.amax(communities))[:3]
            color = matplotlib.colors.rgb2hex(rgb)
            node_colors.append(color)

    ###Saves average correlation network data
    # pylint: disable-next=C0301
    with open(f'results/{EXPERIMENT_NAME}/{analysis_type}_analysis/{network_method}/average_{analysis_type}_network_parameters.txt',
            'w', encoding='utf-8') as file:
        print(f'ConnTh {avg_corr_label} AvgEff AvgK AvgC Smax SwCoef Assort CommNum Q', file=file)
        # pylint: disable-next=C0301
        print(f'{conn_th:.3f} {avg_corr:.3f} {avg_eff:.3f} {avg_k:.3f} {avg_c:.3f} {s_max:.3f} {sw_coef:.3f} {assortativity:.3f} {num_comm/cell_num:.3f} {Q:.3f}',
            file=file)
    
    norm_pos = np.zeros(pos.shape, float)
    xmin, xmax = np.amin(pos[:,0]), np.amax(pos[:,0])
    ymin, ymax = np.amin(pos[:,1]), np.amax(pos[:,1])
    norm_pos[:,0] = (pos[:,0]-xmin)/(xmax-xmin)
    norm_pos[:,1] = (pos[:,1]-ymin)/(ymax-ymin)
    fig = plt.figure(figsize=(PANEL_WIDTH, PANEL_WIDTH))
    ax = fig.add_subplot(1,1,1)
    nx.draw(G, pos=norm_pos, node_size=node_sizes, node_color=node_colors,
            edge_color='dimgray', width=0.75, ax=ax)
    ax.text(-0.1, 1.3, f'ConnTh = {conn_th:.3f}')
    ax.text(-0.1, 1.2, f'{avg_corr_label} = {avg_corr:.3f}')
    ax.text(-0.1, 1.1, f'avgEff = {avg_eff:.3f}')
    
    ax.text(0.35, 1.3, f'avgK = {avg_k:.3f}')
    ax.text(0.35, 1.2, f'Cavg = {avg_c:.3f}')
    ax.text(0.35, 1.1, f'Smax = {s_max:.3f}')
    
    ax.text(0.8, 1.3, f'SW = {sw_coef:.3f}')
    ax.text(0.8, 1.2, f'Assort. = {assortativity:.3f}')
    ax.text(0.8, 1.1, f'Comm = {num_comm/cell_num:.3f}')
    ax.text(0.8, 1.0, f'Q = {Q:.3f}')
    
    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(-0.1, 1.1)
    # pylint: disable-next=C0301
    fig.savefig(f'results/{EXPERIMENT_NAME}/{analysis_type}_analysis/{network_method}/{analysis_type}_graph.png',
                dpi=600, bbox_inches='tight', pad_inches=0.01)
    plt.close(fig)

    clustering_i = clustering(G)
    closeness_centrality_i = nx.closeness_centrality(G)
    degree_centrality_i = nx.degree_centrality(G)
    betweeness_centrality_i = nx.betweenness_centrality(G)
    avg_nn_degree_i = nx.average_neighbor_degree(G)
    # pylint: disable-next=C0301
    with open(f'results/{EXPERIMENT_NAME}/{analysis_type}_analysis/{network_method}/{analysis_type}_network_cell_parameters.txt',
            'w', encoding='utf-8') as file:
        print('k rel_k C Hindex CloseCent DegCent BetwCent AvgNNDeg Comm', file=file)
        for i in range(cell_num):
            k_i = G.degree(i)
            rel_k_i = k_i/cell_num
            clust_i = clustering_i[i]
            hindex_i = calculate_hindex(G,i)
            cls_cent_i = closeness_centrality_i[i]
            k_cent_i = degree_centrality_i[i]
            btw_cent_i = betweeness_centrality_i[i]
            nn_deg_i = avg_nn_degree_i[i]
            comm_i = communities[i]
            # pylint: disable-next=C0301
            print(f'{k_i} {rel_k_i:.3f} {clust_i:.3f} {hindex_i} {cls_cent_i:.3f} {k_cent_i:.3f} {btw_cent_i:.3f} {nn_deg_i:.3f} {comm_i}',
                file=file)

    fig = plt.figure(figsize=(PANEL_WIDTH, PANEL_WIDTH))
    ax = fig.add_subplot(1,1,1)
    ax.imshow(corr_matrix, cmap=plt.get_cmap('jet'),
              vmin=np.amin(corr_matrix), vmax=np.amax(corr_matrix),
              origin='lower')
    ax.set_xlabel('Cell $i$')
    ax.set_ylabel('Cell $j$')
    ax.set_title(f'{analysis_type} matrix')
    # pylint: disable-next=C0301
    fig.savefig(f'results/{EXPERIMENT_NAME}/{analysis_type}_analysis/{network_method}/{analysis_type}_mat.png',
                dpi=600, bbox_inches='tight', pad_inches=0.01)
    plt.close(fig)

    fig = plt.figure(figsize=(PANEL_HEIGHT, PANEL_HEIGHT))
    ax = fig.add_subplot(1,1,1)
    sns.swarmplot(data=np.array([G.degree(kkk) for kkk in range(cell_num)]), orient = 'v', size=2, ax=ax)
    ax.set_xticks([])
    ax.set_title('Node degree distribution')
    fig.savefig(f'results/{EXPERIMENT_NAME}/{analysis_type}_analysis/{network_method}/swarmplot_degree_dist.png',
                dpi=600, bbox_inches='tight', pad_inches=0.01)
    plt.close(fig)

    # pylint: disable-next=C0301
    np.savetxt(f'results/{EXPERIMENT_NAME}/{analysis_type}_analysis/{network_method}/{analysis_type}_mat.txt',
               corr_matrix, fmt='%.3lf')
    # pylint: disable-next=C0301
    np.savetxt(f'results/{EXPERIMENT_NAME}/{analysis_type}_analysis/{network_method}/{analysis_type}_conn_mat.txt',
               conn_mat, fmt='%d')
    print(f'{analysis_type} analysis finished successfully.')
