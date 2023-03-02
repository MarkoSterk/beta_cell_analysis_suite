"""
Utility function for the scripts
"""
# pylint: disable=R0913
import os
import json

def create_sample_config():
    """
    Creates a sample config file for the analysis
    """
    sample_config_data = {
        "EXPERIMENT_NAME": "2023_01_03_GLC9_MS_SER1",
        "SAMPLING": 10.0,
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

    with open('configurations.txt', 'w', encoding='utf-8') as file:
        json.dump(sample_config_data, file, indent=4)


def save_config_data(CONFIG_DATA: dict):
    """
    Saves all config data to file
    """
    if not os.path.exists(f'results/{CONFIG_DATA["EXPERIMENT_NAME"]}'):
        os.makedirs(f'results/{CONFIG_DATA["EXPERIMENT_NAME"]}')

    with open(f'results/{CONFIG_DATA["EXPERIMENT_NAME"]}/configuration.txt',
              'w', encoding='utf-8') as file:
        json.dump(CONFIG_DATA, file, indent=4)

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
