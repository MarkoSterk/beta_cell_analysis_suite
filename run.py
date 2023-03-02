"""
Entry point for the analysis
"""
# pylint: disable=W0702
from typing import Union
import sys
import json
from methods.filt_traces import filter_data
from methods.smooth_traces import smooth_data
from methods.binarization import binarize_data
from methods.exclude_cells import exclude_data
from methods.corr_ca_analysis import corr_ca_analysis_data
from methods.cell_parameter_analysis import cell_activity_data
from methods.first_responders import first_responder_data
from helper_functions.utility_functions import save_config_data, create_sample_config

def parse_input(input_text: str) -> Union[str, int]:
    """
    Parses the provided input.
    Tries to convert to integer. If conversion fails it returns the original string
    """
    try:
        input_text = int(input_text)
    except:
        pass
    return input_text

def load_configs() -> dict:
    """
    Loads/reloads config data
    """
    with open('configurations.txt', encoding='utf-8') as f:
        config_data = f.read()
    config_data = json.loads(config_data)
    return config_data

def run_all_steps(configurations):
    """
    Runs all available analysis methods in sequence except those
    in the EXCLUDE_METHODS list
    Excluded methods:
    0: run_all_methods (obviously)
    100: create_sample_config
    """
    # pylint: disable-next=C0103
    EXCLUDE_METHODS = [0, 1, 'exit', 'options']
    for key, method in methods.items():
        if key not in EXCLUDE_METHODS: ##doesn't run the run_all_steps method again!
            method(configurations)

def print_options():
    """
    Print available options to screen
    """
    print(ANALYSIS_OPTIONS)

methods = {
    0: run_all_steps,
    1: first_responder_data,
    2: filter_data,
    3: smooth_data,
    4: binarize_data,
    5: exclude_data,
    6: corr_ca_analysis_data,
    7: cell_activity_data,
    99: save_config_data,
    'options': print_options,
    'exit': sys.exit
}

ANALYSIS_OPTIONS = """
Available analysis steps are:
1: First responder analysis
2: Time series filtration
3: Time series smoothing
4: Time series binarization
5: Excluding of cells and time series
6: Correlation/coactivity analysis
7: Cell activity parameter analysis
0: Run all of the above steps
99: Save current configuration data to experiment folder
exit: Exit the program
options: Prints available options
"""

print_options()

##Loads config data from file
CONFIG_DATA = None
try:
    ##Tries to load existing configurations
    CONFIG_DATA = load_configs()
except:
    ##Creates default configuration file and loads it
    create_sample_config()
    CONFIG_DATA = load_configs()


RUN_ANALYSIS = True
while RUN_ANALYSIS:
    analysis_step = parse_input(input('Select analysis step [number/string]: '))
    CONFIG_DATA = load_configs()
    if analysis_step in methods:
        if analysis_step in ['exit', 'options']:
            methods[analysis_step]()
        else:
            methods[analysis_step](CONFIG_DATA)
    else:
        print('Please select a valid analysis method.')
