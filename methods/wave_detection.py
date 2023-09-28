"""
Wave detection
"""
# pylint: disable=W0611
# pylint: disable=C0103
# pylint: disable=R0914
import os
import numpy as np
import pandas as pd
from scipy.spatial import distance
from scipy.stats import rankdata
import matplotlib.pyplot as plt
from helper_functions.utility_functions import print_progress_bar
from methods import plot_configurations
from methods.plot_configurations import PANEL_HEIGHT, MEDIAN_PROPS, BOX_PROPS

def wave_detection(CONFIG_DATA: dict, binarized_time_series: np.array, pos: np.array) -> np.array:
    """
    Performs wave detection
    """
    def cellular_neighbours(dist: np.array):
        """
        Finds cell indicies of neighbours
        """
        return np.where((dist<Dth) & (dist!=0))[0]

    # INTERVAL_START_TIME_SECONDS = CONFIG_DATA["INTERVAL_START_TIME_SECONDS"]
    # INTERVAL_END_TIME_SECONDS = CONFIG_DATA["INTERVAL_END_TIME_SECONDS"]
    sampling = CONFIG_DATA["SAMPLING"]
    EXPERIMENT_NAME = CONFIG_DATA["EXPERIMENT_NAME"]
    
    folder_path = f'results/{EXPERIMENT_NAME}/waves'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    FRAME_TH = int(CONFIG_DATA['WAVES']['TIME_TH_SECONDS']*sampling)
    Dth = CONFIG_DATA['WAVES']['DISTANCE_TH']

    # interval_start_time_frames = int(INTERVAL_START_TIME_SECONDS*sampling)
    # interval_end_time_frames = int(INTERVAL_END_TIME_SECONDS*sampling)
    pos = pos * CONFIG_DATA["COORDINATE_TRANSFORM"]
    distances = distance.cdist(pos, pos, 'euclidean')
    
    #Dth = np.average(distances) - np.std(distances)
    Dth = CONFIG_DATA["WAVES"]["DISTANCE_TH"]
    
    neighbours = [cellular_neighbours(distances[:,i]) for i in range(len(pos))]

    nonzero_lines = np.where(binarized_time_series==1)[0]
    active_cells_in_frames = {line: list(np.where(binarized_time_series[line,:]==1)[0]) for line in nonzero_lines}
    print('Wave detection analysis started...')
    event_nums = []
    act_sig = np.zeros(binarized_time_series.shape, int)
    max_event_number = 0
    for i, frame in enumerate(active_cells_in_frames):
        print_progress_bar(i+1, len(active_cells_in_frames.keys()), f'Analyzing frame {frame}')
        k = max_event_number + 1
        if i == 0:
            act_sig[frame, active_cells_in_frames[frame]] = [k+i for i in range(len(active_cells_in_frames[frame]))]

            for cell_i in active_cells_in_frames[frame]:
                for cell_j in list(set(neighbours[cell_i]).intersection(set(active_cells_in_frames[frame]))):
                    act_sig[frame, cell_i] = min(act_sig[frame, cell_i], act_sig[frame, cell_j])
                    act_sig[frame, cell_j] = act_sig[frame, cell_i]
        else:
            act_sig[frame, active_cells_in_frames[frame]] = [k+i if act_sig[frame-1,active_cells_in_frames[frame][j]]==0 else act_sig[frame-1,active_cells_in_frames[frame][j]] for j in range(len(active_cells_in_frames[frame]))]
            
            for cell_i in active_cells_in_frames[frame]:
                for cell_j in list(set(neighbours[cell_i]).intersection(set(active_cells_in_frames[frame]))):
                    if(act_sig[frame, cell_i]!=0 and act_sig[frame, cell_j]!=0
                       and act_sig[frame-1, cell_i]!=0 and np.sum(binarized_time_series[frame-FRAME_TH:frame+1,cell_i])<=FRAME_TH
                       and act_sig[frame-1,cell_j]==0 and cell_i!=cell_j):
                        act_sig[frame,cell_j]=act_sig[frame,cell_i]
                    elif(act_sig[frame,cell_i]!=0 and act_sig[frame,cell_j]!=0 and act_sig[frame-1,cell_i]==0 and act_sig[frame-1,cell_j]!=0
                         and np.sum(binarized_time_series[frame-FRAME_TH:frame+1,cell_j])<=FRAME_TH and cell_i!=cell_j):
                        act_sig[frame,cell_i]=act_sig[frame,cell_j]
                    elif(act_sig[frame,cell_i]!=0 and act_sig[frame,cell_j]!=0 and act_sig[frame-1,cell_i]==0
                         and act_sig[frame-1,cell_j]==0 and cell_i!=cell_j):
                        act_sig[frame,cell_i]=min(act_sig[frame,cell_i],act_sig[frame,cell_j])
                        act_sig[frame,cell_j]=act_sig[frame,cell_i]

        unique_new = np.unique(act_sig[frame,:])
        event_nums = list(set(event_nums).union(set(unique_new)))
        max_event_number = max(event_nums)
    all_event_numbers = np.unique(act_sig[act_sig!=0])
    for i, event_num in enumerate(all_event_numbers):
        act_sig[np.where(act_sig==event_num)] = i+1
    np.savetxt(f'{folder_path}/act_sig.txt', act_sig,fmt='%d')
    return act_sig

def wave_characterization(CONFIG_DATA: dict, act_sig: np.array):
    """
    Characterizes waves according to threshold size
    """
    print('Characterizing detected waves...')
    EXPERIMENT_NAME = CONFIG_DATA["EXPERIMENT_NAME"]
    SIZE_TH = CONFIG_DATA["WAVES"]["REL_SIZE_THRESHOLD"]
    events = [int(e) for e in np.unique(act_sig[act_sig!=0])]
    cell_num = len(act_sig[0])
    folder_path = f'results/{EXPERIMENT_NAME}/waves'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    characteristics = np.zeros((0, 6), float)
    file = open(f'{folder_path}/events_parameters.txt', 'w', encoding='utf-8')
    print('start_frame end_frame duration event_number act_cell_num rel_act_cell_num', file=file)

    for kkk, event in enumerate(events):
        frames, cells = np.where(act_sig==event)
        act_cell_num = len(np.unique(cells))
        start_frame = np.amin(frames)
        end_frame = np.amax(frames)
        duration = end_frame - start_frame
        if(act_cell_num/cell_num > SIZE_TH):
            print(start_frame, end_frame, duration, kkk+1, act_cell_num, act_cell_num/cell_num, file=file)
            characteristics = np.vstack((characteristics, np.array([start_frame, end_frame, duration, event, act_cell_num, act_cell_num/cell_num])))
    file.close()
    return characteristics

def wave_raster_plot(CONFIG_DATA: dict, act_sig: np.array, characteristics: np.array) -> np.ndarray:
    """
    Computes and plots waves rasterplot
    """
    print('Creating wave raster plot...')
    EXPERIMENT_NAME = CONFIG_DATA["EXPERIMENT_NAME"]
    folder_path = f'results/{EXPERIMENT_NAME}/waves'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    sampling = CONFIG_DATA["SAMPLING"]
    rast_plot = []
    for kkk in range(len(characteristics)):
        start_time = int(characteristics[kkk,0])
        end_time = int(characteristics[kkk,1])
        event_num = int(characteristics[kkk,3])
        rnd_num = np.random.randint(1, 600)
        used = []
        for i in range(start_time, end_time+1, 1):
            for j in range(len(act_sig[0])):
                if act_sig[i,j]==event_num and j not in used:
                    rast_plot.append((((i)/sampling), ((i-start_time)/sampling), 0, j, event_num, rnd_num, characteristics[kkk,4]))
                    used.append(j)

    rast_plot = np.array(rast_plot, float)
    all_event_numbers = np.unique(rast_plot[:,4])
    for event_num in all_event_numbers:
        act_times = rast_plot[np.where(rast_plot[:,4]==event_num)][:,1] #act_delays
        ranks = rankdata(act_times, 'min')
        rast_plot[np.where(rast_plot[:,4]==event_num)[0],2] = ranks
        
    file = open(f'{folder_path}/raster_plot.txt', 'w', encoding='utf-8')
    print('start_time act_delay act_rank cell event_num rnd_event_num rel_event_size', file=file)
    for i in range(len(rast_plot)):
        print(rast_plot[i,0], rast_plot[i,1], rast_plot[i,2], int(rast_plot[i,3]), rast_plot[i,4], rast_plot[i,5], rast_plot[i,6], file=file)
    file.close()

    cmap=plt.cm.get_cmap('jet_r')
    vmin=np.amin(rast_plot[:,5])
    vmax=np.amax(rast_plot[:,5])

    fig=plt.figure(figsize=(8,4))
    ax=fig.add_subplot(111)
    ax.scatter(rast_plot[:,0], rast_plot[:,3], s=0.5, c=rast_plot[:,5],
               marker='o', vmin=vmin, vmax=vmax, cmap=cmap)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Cell $i$')
    fig.savefig(f'{folder_path}/raster_plot.png', dpi=600, bbox_inches = 'tight', pad_inches=0.02)
    plt.close(fig)

    return rast_plot

def cells_in_waves_analysis(CONFIG_DATA: dict, rast_plot: np.ndarray, pos: np.ndarray):
    """
    Analysis of cell roles in waves.
    """
    print("Calculating cell parameters in waves")
    EXPERIMENT_NAME = CONFIG_DATA["EXPERIMENT_NAME"]
    folder_path = f'results/{EXPERIMENT_NAME}/waves'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    #start_time act_delay act_rank cell event_num rnd_event_num rel_event_size
    cell_num = len(pos)
    num_of_events = np.unique(rast_plot[:,4])

    #creates array (N,3) array for results:
    # avg. act. rank, init. parameter, rel. participation number of cells
    results = np.zeros((cell_num, 3), float)

    #calculates results
    for i in range(cell_num):
        ##relative number of participations of cell
        results[i,2] = len(rast_plot[np.where(rast_plot[:,3]==i)][:,3])/len(num_of_events)

        ##average activation rank of cell
        results[i,0] = np.nanmean(rast_plot[np.where(rast_plot[:,3]==i)][:,2])

    initiator_perc_cutoff = [10] ##percentile cut-off for determination of initiator cells

    for event in num_of_events:
        event_data = rast_plot[np.where(rast_plot[:,4]==event)]
        perc = np.percentile(event_data[:,2], initiator_perc_cutoff)
        initiator_cells = np.array(event_data[np.where(event_data[:,2]<=perc[0])][:,3], int)
        results[initiator_cells,1]+=1.0
    #Precisions of output file (results array)
    precision = {
        'AvgRank': 2,
        'InitParameter': 0,
        'RelParticipation': 2
    }
    results = pd.DataFrame(results, columns=list(precision.keys()))
    for col, value in precision.items():
        results[col] = results[col].round(value)
    results.to_csv(f'{folder_path}/cell_wave_parameters.txt',
                   sep=' ', index=False)
