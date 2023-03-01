"""
Helper functions for time series menipulations
"""
import numpy as np
import copy

def smooth_ts(time_series: np.ndarray, num_points: int, runs: int) -> np.ndarray:
    """
    Smooths provided time series (time_series)
    num_points: number of points to average over
    runs: number of smoothings to perform

    returns: numpy array of same shape as provided time_series
    """
    data = copy.deepcopy(time_series)
    left_points = int(num_points/2)
    right_points = num_points - left_points
    smoothed_signal = np.zeros(len(data), float)
    for _ in range(runs):
        for i in range(len(data)):
            avg = 0.0
            if i < left_points:
                avg = np.average(data[:i+right_points])
            if left_points <= i < (len(data)-right_points-1):
                avg = np.average(data[i-left_points:i+right_points])
            if i >= (len(data)-right_points-1):
                avg = np.average(data[i-left_points:])
            smoothed_signal[i] = avg
        data = copy.deepcopy(smoothed_signal)

    return smoothed_signal
