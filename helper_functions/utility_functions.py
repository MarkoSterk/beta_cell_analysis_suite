"""
Utility function for the scripts
"""
# pylint: disable=R0913
import os
import json
import numpy as np

SAMPLE_CONFIG_DATA = {
        "EXPERIMENT_NAME": "2023_01_03_GLC9_MS_SER1",
        "SAMPLING": 10.0,
        "RAW_DATA_FOLDER": "raw_data",
        "RAW_DATA_NAME": "data.txt",
        "RAW_POSITIONS_NAME": "koordinate.txt",
        "INTERVAL_START_TIME_SECONDS": 800.0,
        "INTERVAL_END_TIME_SECONDS": 1300.0,
        "FILTER_SELECTION": 'fft',
        "FIRST_COLUMN_TIME": True,
        "LOW_FREQUENCY_CUTOFF": 0.03,
        "HIGH_FREQUENCY_CUTOFF": 1.1,
        "SMOOTHING_POINTS": 4,
        "SMOOTHING_REPEATS": 2,
        "AMP_FACT": 1.35,
        "INTERPEAK_DISTANCE": 10,
        "PEAK_WIDTH": 10,
        "PROMINENCE": 0.35,
        "REL_HEIGHT": 0.5,
        "EXCLUDE_CELLS": [],
        "ANALYSIS_TYPE": 'correlation',
        "NETWORK_METHOD": 'fixed_kavg',
        "CONNECTIVITY_LEVEL": 8.0,
        "FIXED_KAVG_TOLERANCE": 0.1
}
# pylint: disable-next=C0103
def validate_config_data(CONFIG_DATA: dict) -> bool:
    """
    Checks if provided configuration data has all necessary fields
    """
    if set(SAMPLE_CONFIG_DATA) == set(CONFIG_DATA):
        return True
    return False


def create_sample_config() -> dict:
    """
    Creates a sample config file for the analysis
    """
    # sample_config_data = {
    #     "EXPERIMENT_NAME": "2023_01_03_GLC9_MS_SER1",
    #     "SAMPLING": 10.0,
    #     "RAW_DATA_FOLDER": "raw_data",
    #     "RAW_DATA_NAME": "data.txt",
    #     "RAW_POSITIONS_NAME": "koordinate.txt",
    #     "INTERVAL_START_TIME_SECONDS": 800.0,
    #     "INTERVAL_END_TIME_SECONDS": 1300.0,
    #     "FILTER_SELECTION": 'fft',
    #     "FIRST_COLUMN_TIME": True,
    #     "LOW_FREQUENCY_CUTOFF": 0.03,
    #     "HIGH_FREQUENCY_CUTOFF": 1.1,
    #     "SMOOTHING_POINTS": 4,
    #     "SMOOTHING_REPEATS": 2,
    #     "AMP_FACT": 1.35,
    #     "INTERPEAK_DISTANCE": 10,
    #     "PEAK_WIDTH": 10,
    #     "PROMINENCE": 0.35,
    #     "REL_HEIGHT": 0.5,
    #     "EXCLUDE_CELLS": [],
    #     "ANALYSIS_TYPE": 'correlation',
    #     "NETWORK_METHOD": 'fixed_kavg',
    #     "CONNECTIVITY_LEVEL": 8.0,
    #     "FIXED_KAVG_TOLERANCE": 0.1
    # }

    with open('configurations.txt', 'w', encoding='utf-8') as file:
        json.dump(SAMPLE_CONFIG_DATA, file, indent=4)

    return SAMPLE_CONFIG_DATA


def save_config_data(config_data: dict):
    """
    Saves all config data to file
    """
    if not os.path.exists(f'results/{config_data["EXPERIMENT_NAME"]}'):
        os.makedirs(f'results/{config_data["EXPERIMENT_NAME"]}')

    with open(f'results/{config_data["EXPERIMENT_NAME"]}/configuration.txt',
              'w', encoding='utf-8') as file:
        json.dump(config_data, file, indent=4)

def load_existing_data(config_data: dict):
    """
    Loads all existing data from the project folders
    """
    data_collection = {}
    data_list = ['filtered_traces',
    'smoothed_traces', 'binarized_traces', 'response_times',
    'final_smoothed_traces', 'final_binarized_traces', 'final_pos',
    'final_response_times']

    for data_name in data_list:
        data = None
        path = ''
        try:
            if data_name.startswith('final'):
                path = 'results/'
            # pylint: disable-next=C0301
            data = np.loadtxt(f'preprocessing/{config_data["EXPERIMENT_NAME"]}/{path}{data_name}.txt')
        except FileNotFoundError:
            pass
        data_collection[data_name] = data

    return data_collection

# Print iterations progress
def print_progress_bar (iteration: int, total: int, prefix: str = '', suffix: str = '',
                        decimals: int = 1, length: int = 100, fill: str = '█',
                        print_end: str = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        print_end    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    load_bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{load_bar}| {percent}% {suffix}', end = print_end)
    # Print New Line on Complete
    if iteration == total:
        print('\n')
