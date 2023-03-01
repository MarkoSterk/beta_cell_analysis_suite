"""
General configurations the analysis procedure
Please refer to the README.md file for further
information about specific parameters
"""

##Experiment parameters
SAMPLING = 10.0 #in Hz

##Select interval for analysis and visualizations
INTERVAL_START_TIME_SECONDS = 800.0
INTERVAL_END_TIME_SECONDS = 1800.0
####ANALYSIS PARAMETER SELECTION

##Filter preprocessing
##run "filt_traces.py"
FILTER_SELECTION = 'fft'
FIRST_COLUMN_TIME = True
LOW_FREQUENCY_CUTOFF = 0.03
HIGH_FREQUENCY_CUTOFF = 0.8

##Smoothing preprocessing
##run "smooth_traces.py"
SMOOTHING_POINTS = 4
SMOOTHING_REPEATS = 2

##Binarization preprocessing
##run "binarization.py"
AMP_FACT = 1.2
INTERPEAK_DISTANCE = 5
PEAK_WIDTH = 10
PROMINENCE = 0.35
REL_HEIGHT = 0.30

##Exclude cells preprocessing
##run "exclude_cells.py"
#Add number to EXCLUDE_CELLS list
#List can include the number 0
#Example: EXCLUDE_CELLS = [1,76,28,91]
EXCLUDE_CELLS = []

##Correlation and coactivity network analysis
##run "corr_ca_analysis.py"
ANALYSIS_TYPE = 'coactivity'
NETWORK_METHOD = 'fixed_kavg'
CONNECTIVITY_LEVEL = 8.0
