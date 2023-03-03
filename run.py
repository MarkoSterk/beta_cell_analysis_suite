"""
Entry point for the analysis
"""
# pylint: disable=W0702
from typing import Union
import sys
import numpy as np
from methods.islet import Islet

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

def run_all_steps():
    """
    Runs all available analysis methods in sequence except those
    in the EXCLUDE_METHODS list
    Excluded methods:
    0: run_all_methods (obviously)
    1: first responder analysis
    exit: exits program
    options: prints options
    """
    # pylint: disable-next=C0103
    EXCLUDE_METHODS = [0, 1, 'exit', 'options']
    for key, method in methods.items():
        if key not in EXCLUDE_METHODS: ##doesn't run the run_all_steps method again!
            method()

def print_options():
    """
    Print available options to screen
    """
    analysis_options = """
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
    print(analysis_options)

RAW_DATA = None
POSITIONS = None
try:
    RAW_DATA = np.loadtxt('raw_data/data.txt')
    POSITIONS = np.loadtxt('raw_data/koordinate.txt')
except FileNotFoundError:
    # pylint: disable-next=C0301
    print('Raw data not found. Please check if you provided all necessary data in the "raw_data" folder.')
    input('Press any key to exit program.')
    sys.exit()

islet = Islet(RAW_DATA, POSITIONS)


methods = {
    0: run_all_steps,
    1: islet.first_responder_analysis,
    2: islet.filter_traces,
    3: islet.smooth_traces,
    4: islet.binarize_traces,
    5: islet.exclude_traces,
    6: islet.corr_coact_analysis,
    7: islet.cell_activity_analysis,
    99: islet.save_configs_to_data,
    'options': print_options,
    'exit': sys.exit
}

print_options()

while True:
    analysis_step = parse_input(input('Select analysis step [number/string]: '))
    islet.load_configs()
    if analysis_step in methods:
        methods[analysis_step]()
    else:
        print('Please select a valid analysis method.')
