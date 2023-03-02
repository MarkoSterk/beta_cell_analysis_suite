# Beta cell activity analysis suite
Developed with python 3.11.1

## Requirements
Python 3.11.1.
Should also work on older versions of python3 but is not tested.
Install all libraries in the "requirements.txt" file

All steps and instructions assume that you have python installed on your 
computer and that the command "python" points to this installation.

### Use of virtual environment
I suggest the use of a virtual environment.
Use 
```
python -m venv venv
```

to create a virtual environment in your project folder.

Activate the virtual environment with:
Windows:
```
venv/Scripts/activate
```

Linux:
```
source venv/bin/activate
```

Install all dependancies in the virtual environment with:
```
pip install -r requirements.txt
```

This step requires the file "requirements.txt" in the current working directory.

### Provided sample data
We provide sample data in the folder "raw_data/" 

### Raw data input
The scripts require a folder called "raw_data" in the root folder
of your analysis project. 
Required files are:

* data.txt <-- array of shape (MxN); M == number of data points, N == number of cells

* koordinate.txt <-- array of shape (Nx2); where N is the number of cells. Columns represent the (x,y) coordinates of cells

## Analysis and configurations
All analysis configurations reside in the "configurations.py" file.
You may change any of the configuration parameters as you see fit.
Have a look at the steps below for further information and options.

### Running analysis steps
Any analysis step can be run with the command:
```
python run.py    or    python -m run
```

After running the command you will be prompted to select the specific step.

Available analysis steps are:
* 1: Time series filtration
* 2: Time series smoothing
* 3: Time series binarization
* 4: Excluding of cells and time series
* 5: Correlation/coactivity analysis
* 6: Cell activity parameter analysis

Just input the correct number.

### Output folder structure
Any output folders and files are created on-the-go if not already present. No action is required on your part.

### General experiment information
* EXPERIMENT_NAME - name of the experiment. Can be any string without whitespaces or special charecters
* SAMPLING - the data sampling rate in Hz (float or integer number)
Example:
EXPERIMENT_NAME = '2023_01_03_GLC9_MS_SER_1'
SAMPLING = 10.0

Output data is generated in the "preprocessing/" and "results" folders in subfolders with the provided experiment name.

### General analysis configurations
* INTERVAL_START_TIME_SECONDS - the start time (in seconds) of the intervals for visualization and analysis. This parameter is required for the filtration, smoothing, binarization and network analysis steps. You can change this parameter from one analysis step to the other
* INTERVAL_END_TIME_SECONDS - the same as INTERVAL_START_TIME_SECONDS but for the end of the interval
Examples:
INTERVAL_START_TIME_SECONDS = 800.0
INTERVAL_END_TIME_SECONDS = 1300

### Filtration step configurations
* FILTER_SELECTION - "fft" or "analog". Usually "fft" is the better option.
* FIRST_COLUMN_TIME - True or False. If the first column in you raw "data.txt" file represents time
* LOW_FREQUENCY_CUTOFF - a number larger then 0. Represents the low frequency threshold for the band-pass filter
* HIGH_FREQUENCY_CUTOFF - a number larger then LOW_FREQUENCY_CUTOFF. Represents the high frequency threshold for the band-padd filter
Examples:
LOW_FREQUENCY_CUTOFF = 0.03
HIGH_FREQUENCY_CUTOFF = 1.2

Output of this analysis is saved in the folder "preprocessing/{EXPERIMENT_NAME}/" and subfolder "filt_traces/"

### Smoothing step configurations
* SMOOTHING_POINTS - the number of points to average over when smoothing (integer number)
* SMOOTHING_REPEATS - number of times the smoothing is repeated (integer number)
Examples:
SMOOTHING_POINTS = 5
SMOOTHING_REPEATS = 2

Output of this analysis is saved in the folder "preprocessing/{EXPERIMENT_NAME}/" and subfolder "smoothed_traces"

### Binarization step configurations
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

Output of this analysis is saved in the folder "preprocessing/{EXPERIMENT_NAME}/" and subfolder "binarized_traces"

### Exclude cells step configurations
Add numbers (integers) into the "EXCLUDE_CELLS" list.
Beware that you don't repeat the same number!
Example:
EXCLUDE_CELLS = [0,8,92,17,94]

Output of this analysis is saved in the folder "preprocessing/{EXPERIMENT_NAME}/" and subfolder "results"

The output if this script is used for further cell/network analysis.

### Correlation and coactivity network step configurations
* ANALYSIS_TYPE - "correlation" or "coactivity". Select either one as the time series similarity measure
* NETWORK_METHOD - "fixed_kavg" or "fixed_rth". Select either one as the network construction method. fixed_kavg == constructs a network with a fixed average node degree.  fixed_rth == constructs a network with simple correlation/coactivity lever thresholding.
* CONNECTIVITY_LEVEL - Set this value to something larger then 0 if you selected the "fixed_kavg" method. The constructed network will have this average node degree. - Set this value to between 0 and 1 if you selected the "fixed_rth" method.
* FIXED_KAVG_TOLERANCE - relative tolerance when establishing connection in the "fixed_kavg" method graph. 

Examples "fixed_kavg":
ANALYSIS_TYPE = 'coactivity'
NETWORK_METHOD = 'fixed_kavg'
CONNECTIVITY_LEVEL = 8.0
FIXED_KAVG_TOLERANCE = 0.1

With the above CONNECTIVITY_LEVEL and FIXED_KAVG_TOLERANCE the highest expected average node degree of the network
will be 8.8

Examples "fixed_rth":
ANALYSIS_TYPE = 'coactivity'
NETWORK_METHOD = 'fixed_rth'
CONNECTIVITY_LEVEL = 0.75
FIXED_KAVG_TOLERANCE = not needed

Output of this analysis is saved in the folder "results/{EXPERIMENT_NAME}/" and subfolder "correlation_analysis/" or "coactivity_analysis/" and further subfolder "fixed_rth/" or "fixed_kavg/" based on the type of parameters you choose.


### Cell parameter analysis step
The cell analysis parameter step takes the binarized time series data and calculated islet average and
single cell activity parameters.

The cell specific parameters are:
* Relative active time (the time a cells spends in the ON-phase ie 1)
* Average oscillation duration (the average length of oscillations)
* Average oscillation frequency (the frequency of oscillation)
* Interoscillation interval variability (the variability of the intervals between oscillations)

Islet average parameters are:
* Average of all of the above cell specific parameters
* The standard deviations of the above parameters


Output of this analysis is saved in the "results/{EXPERIMENT_NAME}/" folder in files:
"average_islet_activity_parameters.txt", "cellular_activity_parameters.txt" and "cell_parameters_box_plots.png".


## References
The procedures in this suite were previously used in the following research articles:
1. Marko Šterk, Jurij Dolenšek, Maša Skelin Klemen, Lidija Križančić Bombek, Eva Paradiž Leitgeb, Jasmina Kerčmar, Matjaž Perc, Marjan Slak Rupnik, Andraž Stožer, Marko Gosak, 2023. *Functional characteristics of hub and wave initiator cells in beta cell networks*. Biophysical Journal 122, 1-18. DOI: https://www.cell.com/biophysj/pdf/S0006-3495(23)00088-7.pdf

2. Andraž Stožer, Marko Šterk, Eva Paradiž Leitgeb, Rene Markovič, Maša Skelin Klemen, Cara E Ellis, Lidija Križancic Bombek, Jurij Dolensek, Patrick E Macdonald, Marko Gosak, 2022. *From Isles of Königsberg to Islets of Langerhans: Examining the Function of the Endocrine Pancreas through Network Science*. Frontiers in Endocrinology 13, 922640. DOI: 10.3389/fendo.2022.922640

3. Marko Šterk, Lidija Križančić Bombek, Maša Skelin Klemen, Marjan Slak Rupnik, Marko Marhl, Andraž Stožer, Marko Gosak, 2021. *NMDA receptor inhibition increases, synchronizes, and stabilizes the collective pancreatic beta cell activity: Insights through multilayer network analysis*. PLoS Computational Biology 17(5), e1009002. DOI: https://doi.org/10.1371/journal.pcbi.1009002

4. Marko Šterk, Jurij Dolenšek, Lidija Križančić Bombek, Rene Markovič, Darko Zakelšek, Matjaž Perc, Viljem Pohorec, Andraž Stožer, Marko Gosak, 2021. *Assessing the origin and velocity of Ca2+ waves in three-dimensional tissue: Insights from a mathematical model and confocal imaging in mouse pancreas tissue slices*. Communications in Nonlinear Science and Numerical Simulation 93, 105498. DOI: https://doi.org/10.1016/j.cnsns.2020.105495

## Citation
If you use this analysis suite for any publication please cite this work