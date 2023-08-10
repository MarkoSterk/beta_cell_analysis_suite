"""
Utility function for the scripts
"""
# pylint: disable=R0913
import os
import json
import numpy as np
from copy import deepcopy

SAMPLE_CONFIG_DATA = {
    "EXPERIMENT_NAME": "2023_01_03_GLC9_MS_SER1",
    "SAMPLING": 10.0,
    "COORDINATE_TRANSFORM": 1.0,
    "RAW_DATA_FOLDER": "raw_data",
    "RAW_DATA_NAME": "data.txt",
    "RAW_POSITIONS_NAME": "koordinate.txt",
    "INTERVAL_START_TIME_SECONDS": 800.0,
    "INTERVAL_END_TIME_SECONDS": 1300.0,
    "FILTER_SELECTION": "fft",
    "FIRST_COLUMN_TIME": True,
    "LOW_FREQUENCY_CUTOFF": 0.03,
    "HIGH_FREQUENCY_CUTOFF": 1.1,
    "SMOOTHING_POINTS": 4,
    "SMOOTHING_REPEATS": 2,
    "BINARIZATION": {
        "USE": "SLOPE_METHOD",
        "SLOPE_METHOD": {
            "OSCILLATION_DURATION": 10,
            "ACTIVATION_SLOPE": 1.0,
            "AMPLITUDE_FACTOR": 1.0
        },
        "PROMINENCE_METHOD": {
            "AMP_FACT": 1.35,
            "INTERPEAK_DISTANCE": 10,
            "PEAK_WIDTH": 10,
            "PROMINENCE": 0.35,
            "REL_HEIGHT": 0.5
        }
    },
    "ANALYSIS_TYPE": "correlation",
    "NETWORK_METHOD": "fixed_kavg",
    "CONNECTIVITY_LEVEL": 8.0,
    "FIXED_KAVG_TOLERANCE": 0.1,
    "WAVES": {
        "TIME_TH_SECONDS": 0.5,
        "DISTANCE_TH": 30,
        "REL_SIZE_THRESHOLD": 0.45
    }
}
# pylint: disable-next=C0103


def validate_config_data(config_data: dict) -> bool:
    """
    Checks if provided configuration data has all necessary fields
    """
    sample_primary_fields = set(SAMPLE_CONFIG_DATA)
    provided_primary_fields = set(config_data)
    if sample_primary_fields != provided_primary_fields:
        return False

    sample_binarization_sub_fields = set(SAMPLE_CONFIG_DATA['BINARIZATION'])
    provided_binarization_sub_fields = set(
        config_data['BINARIZATION']) if 'BINARIZATION' in config_data else set([])
    if sample_binarization_sub_fields != provided_binarization_sub_fields:
        return False

    sample_slope_method_fields = set(
        SAMPLE_CONFIG_DATA['BINARIZATION']['SLOPE_METHOD']
    )
    provided_slope_method_fields = set(
        config_data['BINARIZATION']['SLOPE_METHOD']) if 'SLOPE_METHOD' in config_data['BINARIZATION'] else set([])
    if sample_slope_method_fields != provided_slope_method_fields:
        return False
    
    sample_prominence_method_fields = set(
        SAMPLE_CONFIG_DATA['BINARIZATION']['PROMINENCE_METHOD']
    )
    provided_prominence_method_fields = set(
        config_data['BINARIZATION']['PROMINENCE_METHOD']) if 'PROMINENCE_METHOD' in config_data['BINARIZATION'] else set([])
    if sample_prominence_method_fields != provided_prominence_method_fields:
        return False

    sample_wave_method_fields = set(
        SAMPLE_CONFIG_DATA["WAVES"]
    )
    provided_wave_method_fields = set(
        config_data["WAVES"] if "WAVES" in config_data else []
    )
    if sample_wave_method_fields != provided_wave_method_fields:
        return False

    return True


def create_sample_config() -> dict:
    """
    Creates a sample config file for the analysis
    """
    with open('configurations.txt', 'w', encoding='utf-8') as file:
        json.dump(SAMPLE_CONFIG_DATA, file, indent=4)

    return SAMPLE_CONFIG_DATA


def save_config_data(config_data: dict):
    """
    Saves all config data to file
    """
    if not os.path.exists(f'results/{config_data["EXPERIMENT_NAME"]}'):
        os.makedirs(f'results/{config_data["EXPERIMENT_NAME"]}')

    with open(f'results/{config_data["EXPERIMENT_NAME"]}/configurations.txt',
              'w', encoding='utf-8') as file:
        json.dump(config_data, file, indent=2)


def load_existing_data(config_data: dict):
    """
    Loads all existing data from the project folders
    """
    data_collection = {}
    data_list = ['filtered_traces',
                 'smoothed_traces', 'binarized_traces', 'first_responder_times',
                 'final_smoothed_traces', 'final_binarized_traces', 'final_coordinates',
                 'final_first_responder_times']
    loaded_data = []
    for data_name in data_list:
        data = None
        path = ''
        try:
            if data_name.startswith('final'):
                path = 'results/'
            # pylint: disable-next=C0301
            data = np.loadtxt(
                f'preprocessing/{config_data["EXPERIMENT_NAME"]}/{path}{data_name}.txt')
            loaded_data.append(
                f'preprocessing/{config_data["EXPERIMENT_NAME"]}/{path}{data_name}.txt - LOADED'
            )
        except FileNotFoundError:
            pass
        data_collection[data_name] = deepcopy(data)

    return data_collection, loaded_data

# Print iterations progress


def print_progress_bar(iteration: int, total: int, prefix: str = '', suffix: str = '',
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
    percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                     (iteration / float(total)))
    filled_length = int(length * iteration // total)
    load_bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{load_bar}| {percent}% {suffix}', end=print_end)
    # Print New Line on Complete
    if iteration == total:
        print('\n')


##try-except "watcher" function
def catch_error():
    """
    Catches all expected and unexpected errors in the app.
    """
    def decorate(func):
        def applicator(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as err:
                print(f"Unexpected error encountered in step {func.__name__.upper()}")
                print(f"ERROR MESSAGE: {err}")
                print("\n")
                return None
        return applicator
    return decorate
