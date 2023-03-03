"""
Base class for Islet data
"""
import json
from methods.filt_traces import filter_data
from methods.smooth_traces import smooth_data
from methods.binarization import binarize_data
from methods.exclude_cells import exclude_data
from methods.corr_ca_analysis import corr_ca_analysis_data
from methods.cell_parameter_analysis import cell_activity_data
from methods.first_responders import first_responder_data
from helper_functions.utility_functions import save_config_data, create_sample_config

class Islet:
    """
    Class containing all methods and data for Islet analysis
    """

    def __init__(self, raw_data, positions):
        self.raw_data = raw_data
        self.positions = positions
        self.configs = None
        self.input = None

        self.filtered_traces = None
        self.smoothed_traces = None
        self.binarized_traces = None
        self.final_smoothed_data = None
        self.final_binarized_data = None
        self.final_pos = None

    def load_configs(self):
        """
        Loads/reloads config data
        """
        try:
            with open('configurations.txt', encoding='utf-8') as file:
                config_data = file.read()
            self.configs = json.loads(config_data)
        except FileNotFoundError:
            self.create_and_load_sample_config_data()

    def create_and_load_sample_config_data(self):
        """
        Calls create sample config function
        """
        self.configs = create_sample_config()

    def save_configs_to_data(self):
        """
        Calls save config function
        """
        save_config_data(self.configs)

    def filter_traces(self):
        """
        Calls filter function with current configs
        """
        self.filtered_traces = filter_data(self.configs,
                                           self.raw_data,
                                           self.positions)

    def smooth_traces(self):
        """
        Calls smoothing function with current configs
        """
        self.smoothed_traces = smooth_data(self.configs, self.filtered_traces)

    def binarize_traces(self):
        """
        Calls binarization function
        """
        self.binarized_traces = binarize_data(
            self.configs, self.filtered_traces)

    def exclude_traces(self):
        """
        Calls exclude function
        """
        final_smoothed_data, final_binarized_data, final_pos = exclude_data(self.configs,
                                                                            self.smoothed_traces,
                                                                            self.binarized_traces,
                                                                            self.positions)

        self.final_smoothed_data = final_smoothed_data
        self.final_binarized_data = final_binarized_data
        self.final_pos = final_pos

    def corr_coact_analysis(self):
        """
        Calls corr/coact network analysis
        """
        time_series = self.final_binarized_data if self.configs[
            'ANALYSIS_TYPE'] == 'coactivity' else self.final_smoothed_data
        corr_ca_analysis_data(self.configs, time_series, self.final_pos)

    def cell_activity_analysis(self):
        """
        Calls call activity parameter data analysis
        """
        cell_activity_data(self.configs, self.final_binarized_data)

    def first_responder_analysis(self):
        """
        Calls first responder analysis
        """
        first_responder_data(self.configs, self.raw_data)
