"""
Base class for Islet data
"""
from typing import Union
import zipfile
import json
import os
import numpy as np
from methods.filt_traces import filter_data
from methods.smooth_traces import smooth_data
from methods.binarization import binarize_data
from methods.bin_traces_old import signal_binarization
from methods.exclude_cells import exclude_data
from methods.corr_ca_analysis import corr_ca_analysis_data
from methods.cell_parameter_analysis import cell_activity_data
from methods.first_responders import first_responder_data
from methods.wave_detection import wave_detection, wave_characterization, wave_raster_plot
from helper_functions.utility_functions import (save_config_data, create_sample_config,
                                                load_existing_data, validate_config_data)

# pylint: disable-next=R0902
class Islet:
    """
    Class containing all methods and data for Islet analysis
    """

    perform_preprocess_steps_first_error: str = """
    Please perform filtration, smoothing and binarization and cell exclusion steps first!
    """
    raw_data_missing_error: str = """
    Please load raw data first! Use the 'load' command.
    """
    raw_data_not_found_error: str = """
    Raw data not found. Please check folder and configurations.
    """
    raw_data_columns_clash_error: str = """
        Number of columns and number of coordinates doesnt match. Please check if first column is or is not time.
    """
    
    raw_data_loaded_successfully: str = """
        Raw data loaded successfully.
    """

    def __init__(self):
        self.raw_data: np.array = None
        self.positions: np.array = None
        self.configs: Union[None, dict] = None

        self.filtered_traces: np.array = None
        self.smoothed_traces: np.array = None
        self.binarized_traces: np.array = None
        self.first_responder_times: np.array = None
        self.final_smoothed_traces: np.array = None
        self.final_binarized_traces: np.array = None
        self.final_coordinates: np.array = None
        self.final_first_responder_times: np.array = None
        self.wave_act_sig: np.array = None
        self.wave_characteristics: np.array = None
        self.wave_raster_plot: np.array = None

    def load_configs(self):
        """
        Loads/reloads config data
        """
        try:
            with open('configurations.txt', encoding='utf-8') as file:
                config_data = file.read()
                config_data = json.loads(config_data)
                if validate_config_data(config_data):
                    self.configs = config_data
                else:
                    print('Configurations file had missing fields and was replaced with default!')
                    self.create_and_load_sample_config_data()
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
        if self.raw_data is not None:
            self.filtered_traces = filter_data(self.configs,
                                            self.raw_data,
                                            self.positions)
        else:
            print(self.raw_data_missing_error)

    def smooth_traces(self):
        """
        Calls smoothing function with current configs
        """
        if self.filtered_traces is not None:
            self.smoothed_traces = smooth_data(self.configs,
                                               self.filtered_traces)
        else:
            print('Please perform the filtration step first!')

    def binarize_traces(self):
        """
        Calls binarization function
        """
        #Availale methods for binarization
        methods = {
            'SLOPE_METHOD': signal_binarization,
            'PROMINENCE_METHOD': binarize_data
        }
        #Selected method for binarization
        selected_method = self.configs['BINARIZATION']['USE']
        if self.smoothed_traces is not None:
            if selected_method in methods:
                self.binarized_traces = methods[selected_method](self.configs,
                                                            self.smoothed_traces)
            else:
                print('Please select a valid binarization method')
        else:
            print('Please perform the smoothing step first!')

    def exclude_traces(self):
        """
        Calls exclude function
        """

        if self.binarized_traces is not None and self.smoothed_traces is not None:
            # pylint: disable-next=C0301
            final_smoothed_data, final_binarized_data, final_pos, final_resp_times = exclude_data(self.configs,
                                                                self.smoothed_traces,
                                                                self.binarized_traces,
                                                                self.positions, self.first_responder_times)

            self.final_smoothed_traces = final_smoothed_data
            self.final_binarized_traces = final_binarized_data
            self.final_coordinates = final_pos
            self.final_first_responder_times = final_resp_times

        else:
            print(self.perform_preprocess_steps_first_error)

    def corr_coact_analysis(self):
        """
        Calls corr/coact network analysis
        """
        if self.final_binarized_traces is not None and self.final_smoothed_traces is not None:
            time_series = self.final_binarized_traces if self.configs[
                'ANALYSIS_TYPE'] == 'coactivity' else self.final_smoothed_traces
            corr_ca_analysis_data(self.configs, time_series, self.final_coordinates)
        else:
            print(self.perform_preprocess_steps_first_error)

    def cell_activity_analysis(self):
        """
        Calls call activity parameter data analysis
        """
        if self.final_binarized_traces is not None:
            cell_activity_data(self.configs, self.final_binarized_traces)
        else:
            print(self.perform_preprocess_steps_first_error)

    def first_responder_analysis(self):
        """
        Calls first responder analysis
        """
        if self.raw_data is not None:
            self.first_responder_times = first_responder_data(self.configs, self.raw_data)
        else:
            print(self.raw_data_missing_error)

    def wave_anaylsis(self):
        """
        Performs wave detection analysis
        """
        if self.final_binarized_traces is not None:
            self.wave_act_sig = wave_detection(self.configs, self.final_binarized_traces, self.final_coordinates)
        else:
            print(self.perform_preprocess_steps_first_error)
        
        if self.wave_act_sig is not None:
            self.wave_characteristics = wave_characterization(self.configs, self.wave_act_sig)
        else:
            print('Please perform wave detection step first.')
        
        if self.wave_characteristics is not None:
            self.wave_raster_plot = wave_raster_plot(self.configs, self.wave_act_sig, self.wave_characteristics)
        else:
            print('Please perform wave detection step first.')

    def reset_app(self):
        """
        Resets the app for new analysis
        """
        self.raw_data = None
        self.positions = None

        self.filtered_traces = None
        self.smoothed_traces = None
        self.binarized_traces = None
        self.first_responder_times = None
        self.final_smoothed_traces = None
        self.final_binarized_traces = None
        self.final_coordinates = None
        self.final_first_responder_times = None
        self.wave_act_sig = None
        self.wave_characteristics = None
        self.wave_raster_plot = None

    def load_data(self):
        """
        Loads raw data from existing raw data folder

        Calls load existing data function
        Loads any existing data from the folder structure
        """
        self.reset_app()
        try:
            raw_data_path = os.path.join(self.configs["RAW_DATA_FOLDER"],
                                         self.configs["RAW_DATA_NAME"])

            raw_data = np.loadtxt(raw_data_path)

            if self.configs['FIRST_COLUMN_TIME']:
                raw_data = raw_data[:,1:]

            raw_positions_path = os.path.join(self.configs["RAW_DATA_FOLDER"],
                                              self.configs["RAW_POSITIONS_NAME"])

            self.positions = np.loadtxt(raw_positions_path)
            if len(self.positions) != len(raw_data[0]):
                #pylint: disable=C0301
                print(self.raw_data_columns_clash_error)
            else:
                self.positions = self.positions * self.configs["COORDINATE_TRANSFORM"]
                self.raw_data = raw_data
                print(self.raw_data_loaded_successfully)
        except FileNotFoundError:
            print(self.raw_data_not_found_error)

        data, loaded_data = load_existing_data(self.configs)
        for key, value in data.items():
            setattr(self, key, value)
        preprocess_data_msg = '\n'.join(loaded_data)
        print(preprocess_data_msg)
        print('\n')

    def bundle_data(self):
        """
        Creates a .zip bundle with all preprocessing results and final results available
        """

        with zipfile.ZipFile(
            f'results/{self.configs["EXPERIMENT_NAME"]}/results_bundle.zip', 'w'
            ) as file:
            preprocessing_data_list = ['final_smoothed_traces.txt',
                                       'final_binarized_traces.txt',
                                        'final_coordinates.txt',
                                        'final_response_times.txt']
            for data_name in preprocessing_data_list:
                try:
                    # pylint: disable-next=C0301
                    file.write(f'preprocessing/{self.configs["EXPERIMENT_NAME"]}/results/{data_name}',
                                data_name)
                except FileNotFoundError:
                    pass

            final_results_data_list = ['configuration.txt',
                                       'cellular_activity_parameters.txt',
                                       'average_islet_activity_parameters.txt',
                                       'cell_parameters_box_plots.png']
            for data_name in final_results_data_list:
                try:
                    file.write(f'results/{self.configs["EXPERIMENT_NAME"]}/{data_name}',
                            data_name)
                except FileNotFoundError:
                    pass
