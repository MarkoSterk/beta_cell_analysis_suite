"""
Binarization function using amplitude increase and slope
for determination of the onset of oscillations

Author: Marko Gosak
"""
# pylint: disable=C0103
# pylint: disable=R0914, R0912, R0915, R1702

import os
import numpy as np
import matplotlib.pyplot as plt
from helper_functions.ploting_funcs import binarized_plot
from helper_functions.utility_functions import print_progress_bar


def signal_binarization(CONFIG_DATA: dict, data: np.ndarray, pos: np.ndarray) -> np.ndarray:
    """
    Performs time series binarization based
    on amplitude increase and slope of oscillations
    """
    EXPERIMENT_NAME = CONFIG_DATA['EXPERIMENT_NAME']
    sampling = CONFIG_DATA['SAMPLING']
    PB = int(CONFIG_DATA['BINARIZATION']['SLOPE_METHOD']['OSCILLATION_DURATION'])
    act_slope = CONFIG_DATA['BINARIZATION']['SLOPE_METHOD']['ACTIVATION_SLOPE']
    amp_faktor = CONFIG_DATA['BINARIZATION']['SLOPE_METHOD']['AMPLITUDE_FACTOR']
    start_time_seconds = CONFIG_DATA['INTERVAL_START_TIME_SECONDS']
    end_time_seconds = CONFIG_DATA['INTERVAL_END_TIME_SECONDS']

    if not os.path.exists(f'preprocessing/{EXPERIMENT_NAME}/binarized_traces'):
        os.makedirs(f'preprocessing/{EXPERIMENT_NAME}/binarized_traces')

    ts_length, cell_num = data.shape

    time = [i/sampling for i in range(ts_length)]
    #data = data-np.mean(data)
    for i in range(cell_num):
        data[:,i] = data[:,i] - np.mean(data[:,i])

    cut_out = int(round(0.05*ts_length))
    # calculates the time series STD without the first and last 5% of the time series
    varsig = [np.std(data[cut_out:-cut_out, i])
              for i in range(cell_num)]

    def slope_calc(series: np.ndarray) -> list:
        """
        Calculates slope vs time for ts
        """
        offset = int(PB/3.0)
        slope_ts = []
        for i in range(ts_length-PB-2):
            slope_ts.append(
                (((series[i+offset-1]+series[i+offset]+series[i+offset+1])/3.0)-series[i])
            )
        return slope_ts

    derser2 = [slope_calc(data[:, i]) for i in range(cell_num)]
    varderser2 = [np.std(derser2[i]) for i in range(cell_num)]

    binsig = np.zeros((ts_length, cell_num), int)
    nnact = np.zeros(cell_num, int)
    tact = []
    for rep in range(cell_num):
        print_progress_bar(rep+1, cell_num, f'Calculating oscillation parameters for cell {rep} ')
        tact.append([])
        for i in range(int(5*PB), ts_length-PB-2, 1):
            slp = np.zeros(5)
            for ii in range(5):
                slp[ii] = (((data[i-2+ii][rep]+data[i-1+ii][rep]+data[i+ii][rep] +
                           data[i+1+ii][rep]+data[i+2+ii][rep])/5.0)-data[i+ii][rep])

            ims = slp.argmax()
            slp2 = (((data[i+int(PB/3.0)-1][rep]+data[i+int(PB/3.0)]
                    [rep]+data[i+int(PB/3.0)+1][rep])/3.0)-data[i][rep])

            ok0 = 0  # preverja odvod
            if slp2 > act_slope*varderser2[rep]:
                ok0 = 1
            ok1 = 0  # preverja, ce so v nadaljevanju dovolj visoki
            for p in range(PB):
                if data[i+p][rep] > amp_faktor*varsig[rep]:
                    ok1 += 1

            if ((ok0 > 0) and (ok1 > 2)):
                ok2 = 1  # preverje blizino prejsnjega
                if nnact[rep] < 1:
                    ok2 = 1
                else:
                    for iii in range(int(1.25*PB)):
                        if np.abs(tact[rep][nnact[rep]-1]-(i+iii)) < PB:
                            ok2 = 0
                            break
                if ok2 > 0:
                    nnact[rep] += 1
                    tact[rep].append(i+int(PB/10.0)+ims)

    maxser = []
    tmax = []
    minser = []
    tmin = []
    for rep in range(cell_num):
        maxser.append([])
        tmax.append([])
        maxser[rep] = np.zeros(len(tact[rep]))-10000
        for kk in range(len(tact[rep])):
            tmax[rep].append(tact[rep][kk])
        for ii in range(nnact[rep]):
            # print rep,ii
            for i in range((tact[rep][ii]+1), (tact[rep][ii]+int(1.5*PB)), 1):
                if i < len(data)-2*PB:
                    if data[i][rep] > maxser[rep][ii]:
                        maxser[rep][ii] = data[i][rep]
                        tmax[rep][ii] = i
        minser.append([])
        tmin.append([])
        minser[rep] = np.zeros(len(tmax[rep]))+10000
        for kk in range(len(tmax[rep])):
            tmin[rep].append(tmax[rep][kk])
        for ii in range(nnact[rep]):
            for i in range((tmax[rep][ii]+1), (tmax[rep][ii]+int(2*PB)), 1):
                if i < len(data)-2*PB:
                    if data[i][rep] < minser[rep][ii]:
                        minser[rep][ii] = data[i][rep]
                        tmin[rep][ii] = i

    tfin = []
    for rep in range(cell_num):
        tfin.append([])
        for kk in range(len(tmax[rep])):
            tfin[rep].append(tmax[rep][kk])
        for ii in range(nnact[rep]):
            for i in range((tmax[rep][ii]+1), (tmin[rep][ii]), 1):
                if data[i][rep] < ((0.5*maxser[rep][ii]+0.5*minser[rep][ii])):
                    tfin[rep][ii] = i
                    break

    for rep in range(cell_num):
        ii = 0
        nobin = 0
        for i in range(ts_length-PB-2):
            # print rep,i,ii,tact[rep][ii],len(tact[rep])
            if ( (tact[rep][ii]<=i<=tfin[rep][ii]) and (nobin==0) ):
                binsig[i][rep]=1
            if ((i>tmin[rep][ii]) and (ii<len(tact[rep])-1) ):
                ii+=1
            if ( (i>tact[rep][ii]) and (ii==(len(tact[rep]))) ):
                nobin=1

    for rep in range(cell_num):
        data[:, rep] = (data[:, rep]-min(data[:, rep])) / \
            (max(data[:, rep])-min(data[:, rep]))

    for i in range(cell_num):
        print_progress_bar(i+1, cell_num, f'Ploting binarized time series {i} ')
        fig, (ax1, ax2) = plt.subplots(2, 1)
        ax1.set_title(f'Cell {i}')
        ax1.plot(time, data[:, i], c='dimgray', linewidth=0.5)
        ax1.plot(time, binsig[:, i], c='red', linewidth=0.2)
        ax1.set_ylabel('Signal (a.u.)')

        ax2.plot(time, data[:, i], c='dimgray', linewidth=0.5)
        ax2.plot(time, binsig[:, i], c='red', linewidth=0.2)
        ax2.axhline(amp_faktor*varsig[i]+np.mean(data[:,i]), c='blue', linewidth=0.2)
        ax2.set_xlabel('time (s)')
        ax2.set_ylabel('Binarized signal')
        ax2.set_xlim(start_time_seconds, end_time_seconds)

        plt.subplots_adjust(hspace=0.15)
        fig.savefig(f'preprocessing/{EXPERIMENT_NAME}/binarized_traces/binarized_traces_{i}.png',
                    dpi=200, bbox_inches='tight', pad_inches=0.01)
        plt.close(fig)

    np.savetxt(f'preprocessing/{EXPERIMENT_NAME}/binarized_traces.txt', binsig, fmt='%d')
    fig = binarized_plot(time, binsig, pos)
    fig.savefig(f'preprocessing/{EXPERIMENT_NAME}/raster_plot.png', dpi=200, bbox_inches='tight')
    plt.close(fig)
    return binsig
