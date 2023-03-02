"""
Entry point for the analysis
"""
# pylint: disable=W0702
import json
from methods.filt_traces import filter_data
from methods.smooth_traces import smooth_data
from methods.binarization import binarize_data
from methods.exclude_cells import exclude_data
from methods.corr_ca_analysis import corr_ca_analysis_data
from methods.cell_parameter_analysis import cell_activity_data
from helper_functions.utility_functions import save_config_data, create_sample_config

def run_all_steps(configurations):
    """
    Runs all available analysis methods in sequence except those
    in the EXCLUDE_METHODS list
    Excluded methods:
    0: run_all_methods (obviously)
    100: create_sample_config
    """
    # pylint: disable-next=C0103
    EXCLUDE_METHODS = [0, 100]
    for key, method in methods.items():
        if key not in EXCLUDE_METHODS: ##doesn't run the run_all_steps method again!
            method(configurations)

print("""
Available analysis steps are:
1: Time series filtration
2: Time series smoothing
3: Time series binarization
4: Excluding of cells and time series
5: Correlation/coactivity analysis
6: Cell activity parameter analysis
99: Save configuration data
100: Create sample config data
0: Run all of the above
exit: exists the program
""")
analysis_step = input('Select analysis step [number]: ')

try:
    analysis_step = int(analysis_step)
except:
    if analysis_step == 'exit':
        print('Program exited successfully.')
    else:
        # pylint: disable-next=W0719, W0707
        raise BaseException('You did not enter a valid number.')

##Loads config data from file
CONFIG_DATA = None
try:
    with open('configurations.txt', encoding='utf-8') as f:
        CONFIG_DATA = f.read()
    CONFIG_DATA = json.loads(CONFIG_DATA)
except:
    # pylint: disable-next=W0719, W0707
    raise BaseException('Configurations file not found. Use method 100 to create sample file.')

methods = {
    0: run_all_steps,
    1: filter_data,
    2: smooth_data,
    3: binarize_data,
    4: exclude_data,
    5: corr_ca_analysis_data,
    6: cell_activity_data,
    99: save_config_data,
    100: create_sample_config
}

if analysis_step in methods:
    methods[analysis_step](CONFIG_DATA)
elif analysis_step == 'exit':
    pass
else:
    print('Please select a valid analysis method.')