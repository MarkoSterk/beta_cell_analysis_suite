# Beta cell activity analysis suite
Developed with python 3.11.1

## Requirements
Python 3.11.1
Install all libraries in the "requirements.txt" file

### Raw data input
The scripts require a folder called "raw_data" in the root folder
of your analysis project. 
Required files are:

* data.txt <-- array of shape (MxN); M == number of data points, N == number of cells

* koordinate.txt <-- array of shape (Nx2); where N is the number of cells. Columns represent the (x,y) coordinates of cells

### Configurations
All analysis configurations reside in the "configurations.py" file.
You may change any of the configuration parameters as you see fit.

#### General experiment information
* SAMPLING - the data sampling rate in Hz (float or integer number)
Example:
SAMPLING = 10.0

#### General analysis configurations
* INTERVAL_START_TIME_SECONDS - the start time (in seconds) of the intervals for visualization and analysis. This parameter is required for the filtration, smoothing, binarization and network analysis steps. You can change the parameter from one analysis to the other
* INTERVAL_END_TIME_SECONDS - the same as INTERVAL_START_TIME_SECONDS but for the end of the interval
Examples:
INTERVAL_START_TIME_SECONDS = 800.0
INTERVAL_END_TIME_SECONDS = 1300

#### Filtration step configurations
* FILTER_SELECTION - "fft" or "analog". Usually "fft" is the better option.
* FIRST_COLUMN_TIME - True or False. If the first column in you raw "data.txt" file represents time
* LOW_FREQUENCY_CUTOFF - a number larger then 0. Represents the low frequency threshold for the band-pass filter
* HIGH_FREQUENCY_CUTOFF - a number larger then LOW_FREQUENCY_CUTOFF. Represents the high frequency threshold for the band-padd filter
Examples:
LOW_FREQUENCY_CUTOFF = 0.03
HIGH_FREQUENCY_CUTOFF = 1.2

#### Smoothing step configurations
* SMOOTHING_POINTS - the number of points to average over when smoothing (integer number)
* SMOOTHING_REPEATS - number of times the smoothing is repeated (integer number)
Examples:
SMOOTHING_POINTS = 5
SMOOTHING_REPEATS = 2

#### Binarization step configurations
The binarization procedure uses the SciPy library. Specifically it uses the
find_peaks method (https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html) and peak_widths method (https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.peak_widths.html). For a more detailed 
* AMP_FACT - the relative rise above the average signal to be considered as a peak
* INTERPEAK_DISTANCE - the expected distance between two peaks (in samples) (integer number)
* PEAK_WIDTH - the expected peak width (in samples) (integer number)
* PROMINENCE - check the find_peaks documentation
* REL_HEIGHT - check the find_peaks documentation
Examples:
AMP_FACT = 1.2
INTERPEAK_DISTANCE = 5
PEAK_WIDTH = 10
PROMINENCE = 0.35
REL_HEIGHT = 0.30

#### Exclude cells step configurations
Add numbers (integers) into the "EXCLUDE_CELLS" list.
Beware that you don't repeat the same number!
Example:
EXCLUDE_CELLS = [0,8,92,17,94]


#### Correlation and coactivity network step configurations
* ANALYSIS_TYPE - "correlation" or "coactivity". Select either one as the time series similarity measure
* NETWORK_METHOD - "fixed_kavg" or "fixed_rth". Select either one as the network construction method. fixed_kavg == constructs a network with a fixed average node degree.  fixed_rth == constructs a network with simple correlation/coactivity lever thresholding.
* CONNECTIVITY_LEVEL - Set this value to something larger then 0 if you selected the "fixed_kavg" method. The constructed network will have this average node degree. - Set this value to between 0 and 1 if you selected the "fixed_rth" method. 

Examples "fixed_kavg":
ANALYSIS_TYPE = 'coactivity'
NETWORK_METHOD = 'fixed_kavg'
CONNECTIVITY_LEVEL = 8.0

Examples "fixed_rth":
ANALYSIS_TYPE = 'coactivity'
NETWORK_METHOD = 'fixed_rth'
CONNECTIVITY_LEVEL = 0.75