import numpy as np

import matplotlib.pyplot as plt

from scipy.signal import butter, sosfiltfilt
from scipy.fftpack import rfft, irfft, fftfreq

class Filter(object):

    """docstring for Filter."""

    #def __init__(self, file, cell, fs=sampling):
    def __init__(self, signal, fs):

        #self.data = np.loadtxt(file).transpose()[cell]
        self.data = signal

        self.nyq = 0.5*fs

        self.time = np.arange(0, (np.size(self.data-1))/fs, 1/fs)


    def bandpass(self, lowcut, highcut, order=5):

        low = lowcut / self.nyq

        high = highcut / self.nyq

        sos = butter(order, [low, high], analog=False, btype='band', output='sos')

        y = sosfiltfilt(sos, self.data)

        return y



    def lowpass(self, cutoff, order=5):

        normal_cutoff = cutoff / self.nyq

        sos = butter(order, normal_cutoff, btype='low', analog=False, output='sos')

        y = sosfiltfilt(sos, self.data)

        return y



    def highpass(self, cutoff, order=1):

        normal_cutoff = cutoff / self.nyq

        sos = butter(order, normal_cutoff, btype='high', analog=False, output='sos')

        y = sosfiltfilt(sos, self.data)

        return y



    def plot(self, *args):

        plt.clf()

        plt.plot(self.time, self.data)

        for arg in args:

            plt.plot(self.time, arg)

        plt.show()


class FFTFilter:
    
    def __init__(self, signal, time):
        self.signal = signal
        self.time = time
        self.step = time[1] - time[0]
    
    def find_fftfreq(self):
        self.wt = fftfreq(self.signal.size, d = self.step)
    
    def rfft(self):
        self.f_signal = rfft(self.signal)

    def bandpass_filt(self, low, high):
        self.cut_f_signal = self.f_signal.copy()
        self.cut_f_signal[(self.wt<low)] = 0 
        self.cut_f_signal[(self.wt>high)] = 0
    
    def get_filtered_signal(self):
        return irfft(self.cut_f_signal)
