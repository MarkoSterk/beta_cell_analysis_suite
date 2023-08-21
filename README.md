# Beta cell activity analysis suite
Developed with python 3.11.1


## Provided sample data
We provide sample data in the folder "raw_data/" 

## Raw data input
The scripts require a folder with the raw data. You are free to select the name of this folder as well as the names of the two necessary raw data files (time series data and cell positions data). You just have to provide the names of the folder and raw data files in the configurations.txt file. Have a look at the "General experiment information" section for more detailed information.\

Raw data files shapes:\
* time series data <-- array of shape (MxN); M == number of data points (rows), N == number of cells (columns) (can have an additional first column with time data: N+1)
* cell positions data <-- array of shape (Nx2); where N is the number of cells. Columns represent the (x,y) coordinates of each cell

## Analysis and configurations
All analysis configurations reside in the "configurations.txt" file. **This file is created when you run the program, and the file is not already present. If the file is already present it is first validated and then loaded. If configuration fields are missing the file is swapped for default configurations.**\
You may change any of the configuration parameters as you see fit.
Have a look at the steps below for further information and options.

## Running analysis steps
**Non-python users can use the "BetaCellAnalysis.exe" executable file in the "dist/" folder for all analysis.**

The program will run in an endless loop until exited with the proper command.
You will be asked for the next step everytime an analysis step finishes. The configurations are updated
on-the-go (in case you make changes) so you don't have to exit and re-run the program for every step.

### Requirements
**Python users only!**
Developed and tested with Python 3.11.1.\
Should also work on older versions of python3 but is not tested.
Install all libraries in the "requirements.txt" file

All steps and instructions assume that you have python installed on your 
computer and that the command "python" points to this installation.

#### Use of virtual environment
I suggest the use of a virtual environment to make sure all steps work as intended.
Use 
```
python -m venv venv
```

or, if you use conda:
```
conda create --name venv
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

Conda (Windows):
```
conda activate venv
```

Conda users also run:
```
conda install -n venv pip
```

Install all dependancies in the virtual environment with pip:
```
pip install -r requirements.txt
```

This step requires the file "requirements.txt" in the current working directory.
Any analysis step can be run with the command:
```
python run.py    or    python -m run
```

After running the command you will be prompted to select the specific step.

##### Available analysis steps:
* 1: First responder analysis
* 2: Time series filtration
* 3: Time series smoothing
* 4: Time series binarization
* 5: Excluding of cells and time series
* 6: Correlation/coactivity analysis
* 7: Cell activity parameter analysis
* 0: Run all of the above steps
* 99: Save current configuration data to experiment folder
* exit: Exit the program
* options: Prints available options
* bundle: Creates zip bundle of all available preprocessing and results data
* load: Loads any existing data (raw and preprocessed) from the folder structure with provided configurations - RUN FIRST

Just input the correct number/string or exit.

The program will run in an endless loop until exited with the proper command.
You will be asked for the next step everytime a step finishes. The configurations are updated
on-the-go (in case you make changes) so you don't have to exit and re-run the program for every step.

## Output folder structure
Any output folders and files are created on-the-go if not already present. No action is required on your part.

## General experiment information
* EXPERIMENT_NAME - name of the experiment. Can be any string without whitespaces or special charecters
* SAMPLING - the data sampling rate in Hz (float or integer number)
* COORDINATE_TRANSFORM - transformation of pixel coordinates to micrometer coordinates. Means number of microns/pixel
* RAW_DATA_FOLDER - folder name in which raw data resides
* RAW_DATA_NAME - name of the raw data time series file (including extension!)
* RAW_POSITIONS_NAME - name of the raw data positions file (including extension!)
\
Example:\
EXPERIMENT_NAME = '2023_01_03_GLC9_MS_SER_1'\
COORDINATE_TRANSFORM = 0.9 <-- 1 px = 0.9 um\
SAMPLING = 10.0\
RAW_DATA_FOLDER = 'raw_data'\
RAW_DATA_NAME = 'data.txt'\
RAW_POSITIONS_NAME = 'koordinate.txt'

Output data is generated in the "preprocessing/" and "results/" folders in subfolders with the provided experiment name.

## General analysis configurations
* INTERVAL_START_TIME_SECONDS - the start time (in seconds) of the intervals for visualization and analysis. This parameter is required for the filtration, smoothing, binarization and network analysis steps. You can change this parameter from one analysis step to the other
* INTERVAL_END_TIME_SECONDS - the same as INTERVAL_START_TIME_SECONDS but for the end of the interval\
\
Examples:\
INTERVAL_START_TIME_SECONDS = 800.0\
INTERVAL_END_TIME_SECONDS = 1300

## First responder step configurations
No configurations are required aside from general experiment information.\
Time series of each cell is plotted and displayed on the screen. The user has to click on the
plot in the place where the cell has first responded to stimulation.

Accepted clicks/commands are:
* Right click - gets the time of response from the x coordinate of the click event. Saves that as the response time for the current cell.
* Right arrow - skips cell/goes to the next cell. The response time of the skipped cell is set to NaN (not a number)
* Left arrow - returns to previous cell and lets you reselect the response time
* r (the letter r) - sets response time to NaN (not a number). Applies also if the response time was previously set.
* esc - escape key exits the analysis (and closes program)

Output of this analysis is saved in the folder "preprocessing/{EXPERIMENT_NAME}/first_responders".

## Filtration step configurations
* FILTER_SELECTION - "fft" or "analog". Usually "fft" is the better option.
* FIRST_COLUMN_TIME - True or False. If the first column in you raw "data.txt" file represents time
* LOW_FREQUENCY_CUTOFF - a number larger then 0. Represents the low frequency threshold for the band-pass filter
* HIGH_FREQUENCY_CUTOFF - a number larger then LOW_FREQUENCY_CUTOFF. Represents the high frequency threshold for the band-padd filter
\
Examples:\
LOW_FREQUENCY_CUTOFF = 0.03\
HIGH_FREQUENCY_CUTOFF = 1.2

Output of this analysis is saved in the folder "preprocessing/{EXPERIMENT_NAME}/" and subfolder "filt_traces/"

## Smoothing step configurations
* SMOOTHING_POINTS - the number of points to average over when smoothing (integer number)
* SMOOTHING_REPEATS - number of times the smoothing is repeated (integer number)\
\
Examples:\
SMOOTHING_POINTS = 5\
SMOOTHING_REPEATS = 2

Output of this analysis is saved in the folder "preprocessing/{EXPERIMENT_NAME}/" and subfolder "smoothed_traces"

## Binarization step configurations
There are TWO binarization options available. The procedures differ but the end result is similar of the correct configuration parameters are set.\

The first method is called "SLOPE_METHOD":\
It calculates the amplitude and slope increases of the time series to calulate oscillation onsets. Parameters for this procedure are:
* OSCILLATION_DURATION - the expected duration of the oscillation (in samples) (integer number)
* ACTIVATION_SLOPE - a float number usually in the range od 0.5 - 1.5. Represents the slope of the time series at oscillation onsets.
* AMPLITUDE_FACTOR - a float number usually in the range of 0.5-1.5. Represents the (relative) amplitude increase of the time series for an oscillation to be considered.

The second method is called "PROMINENCE_METHOD":\
This procedure uses the SciPy library. Specifically it uses the
find_peaks method (https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html) and peak_widths method (https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.peak_widths.html). For a more detailed 
* AMP_FACT - the relative rise above the average signal to be considered as a peak
* INTERPEAK_DISTANCE - the expected distance between two peaks (in samples) (integer number)
* PEAK_WIDTH - the expected peak width (in samples) (integer number)
* PROMINENCE - check the find_peaks documentation
* REL_HEIGHT - check the find_peaks documentation\
\
Configuration example:
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
}
The above configurations make use of the "SLOPE_METHOD" method. If you want to use the "PROMINENCE_METHOD" method just change the "USE" parameter to "PROMINENCE_METHOD". Set the appropriate parameters in the "SLOPE_METHOD" or "PROMINENCE_METHOD" fields.

**If you re-run this procedure and change the method the output will override the previous output.**

Output of this analysis is saved in the folder "preprocessing/{EXPERIMENT_NAME}/" and subfolder "binarized_traces".
The "raster_plot.png" figure has the cells on the y axis ordered according to their distance from the
origin (0,0).

## Exclude cells step configurations
In this step you can either exclude time series/cells visually or from an existing .txt file with cell indecies.
In the former case, the time series are plotet between the provided "INTERVAL_START_TIME_SECONDS" and "INTERVAL_END_TIME_SECONDS" time points. You can pan across the plot with the panning tool.
After visual inspection you can do/click/select:

* right arraw: keeps the current cell
* r or R: removes the current cells
* left arrow: goes back to the previous cell (removes cell index from the exclusion list if it was already in it)
* esc: exits entire app

The excluded cells are added to the excluded_cells.txt file in the preprocessing/{EXPERIMENT_NAME}/results folder.

If you choose to exclude cells from an existing file you have to put the file in the same folder as it would otherwise be created in ("preprocessing/{EXPERIMENT_NAME}") with the name "excluded_cells.txt". The file is loaded and only the sorted list of unique elements is used in the exclusion process. Therefore, if you are analyzing the same recording in different intervals, you can simply copy the excluded cells list of each interval into a single file and the program will create the final list of unique cell indecies that were excluded.

Output files of this step is saved in the folder "preprocessing/{EXPERIMENT_NAME}/" and subfolder "results".
The "final_raster_plot.png" figure has the cells on the y axis ordered according to their distance from the
origin (0,0).

**ATTENTION**
**This step is required (EVEN IF NO CELLS ARE EXCLUDED) and requires that all previous steps are completed.**
**Exception to this requirement is the first responder analysis which is not required.**

The output if this script is used for further cell/network analysis.

## Correlation and coactivity network step configurations
* ANALYSIS_TYPE - "correlation" or "coactivity". Select either one as the time series similarity measure
* NETWORK_METHOD - "fixed_kavg" or "fixed_rth". Select either one as the network construction method. fixed_kavg == constructs a network with a fixed average node degree.  fixed_rth == constructs a network with simple correlation/coactivity lever thresholding.
* CONNECTIVITY_LEVEL - Set this value to something larger then 0 if you selected the "fixed_kavg" method. The constructed network will have this average node degree. - Set this value to between 0 and 1 if you selected the "fixed_rth" method.
* FIXED_KAVG_TOLERANCE - relative tolerance when establishing connection in the "fixed_kavg" method graph.\
\
Examples "fixed_kavg":\
ANALYSIS_TYPE = 'coactivity'\
NETWORK_METHOD = 'fixed_kavg'\
CONNECTIVITY_LEVEL = 8.0\
FIXED_KAVG_TOLERANCE = 0.1\
\
With the above CONNECTIVITY_LEVEL and FIXED_KAVG_TOLERANCE the highest expected average node degree of the network
will be 8.8\
\
Examples "fixed_rth":\
ANALYSIS_TYPE = 'coactivity'\
NETWORK_METHOD = 'fixed_rth'\
CONNECTIVITY_LEVEL = 0.75\
FIXED_KAVG_TOLERANCE = not needed\
\
Output of this analysis is saved in the folder "results/{EXPERIMENT_NAME}/" and subfolder "correlation_analysis/" or "coactivity_analysis/" and further subfolder "fixed_rth/" or "fixed_kavg/" based on the type of parameters you choose.


## Cell parameter analysis step
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

## Wave detection analysis
This analysis step requires a sampling rate of at least 5 Hz. Works best with 10 Hz or above.
The wave detection analysis step detects waves in the binarized cellular signals (final_binarized_traces).

Input parameters are:
* TIME_TH_SECONDS - temporal delay between oscillation onsets between cells in the same wave.
* DISTANCE_TH - spatial distance between two cells in the same wave
* REL_SIZE_THRESHOLD - relative size of detected waves to be considered in the analysis

The delay threshold is the temporal delay between oscillation onsets of two cells between which the wave is propagating. 
The value of this parameter depends on the type of dynamics. For fast calcium oscillations in beta cells with a sampling rate of 10 Hz a good value is 0.5 s.
The distance threshold is the physical distance between two cells between which the wave propagates. It depends on the spatial distribution of the cells. A good value is: D = avg(distance) - X * std(distance), where D is the threshold value,
distance is the distance matrix for all cells and X is a fraction. BEWARE that the set value must take into account the conversion between pixels and micrometers if the COORDINATE_TRANSFORM parameter is set.
The relative size threshold is the minimum (relative) size of waves that are considered in the analysis and outputed in the files. Small waves are usually not worth it. A good value is around 0.45 (45% relative size)

OUTPUT of this analysis set are:
* act_signal.txt - same shape as the binarized signal with numbers denoting the wave to which each cell belongs in a given time frame
* events_parameters.txt - event/wave parameters: start/end frame, duration and (rel)size
* raster_plot.txt - the raster plot for all detected waves. 
* raster_plot.png - visualized raster plot for all detected waves.

All output files are stored in the "results/{EXPERIMENT_NAME}/waves" folder.

## 99: Save current configuration data to experiment folder
This step saves the current data to the results folder of the analysis. This can be useful to compare or share configurations.

## exit: Exit the program
This options exits the program.

## options: Prints available options
This option prints all available options to the screen (again)

## bundle: Creates .zip bundle of all available preprocessing and results data
This options creates a bundle (results/{EXPERIMENT_NAME}/results_bundle.zip) with all available preprocessing and results data.
The bundle is saved in the results folder of the current experiment data ('results/{EXPERIMENT_NAME}/results_bundle.zip')
Can be usefull for storage and transportation or sending via the internet.

## References
The procedures in this suite were previously used in the following research articles:
1. Marko Šterk, Jurij Dolenšek, Maša Skelin Klemen, Lidija Križančić Bombek, Eva Paradiž Leitgeb, Jasmina Kerčmar, Matjaž Perc, Marjan Slak Rupnik, Andraž Stožer, Marko Gosak, 2023. *Functional characteristics of hub and wave initiator cells in beta cell networks*. Biophysical Journal 122, 1-18. DOI: https://www.cell.com/biophysj/pdf/S0006-3495(23)00088-7.pdf

2. Andraž Stožer, Marko Šterk, Eva Paradiž Leitgeb, Rene Markovič, Maša Skelin Klemen, Cara E Ellis, Lidija Križancic Bombek, Jurij Dolensek, Patrick E Macdonald, Marko Gosak, 2022. *From Isles of Königsberg to Islets of Langerhans: Examining the Function of the Endocrine Pancreas through Network Science*. Frontiers in Endocrinology 13, 922640. DOI: 10.3389/fendo.2022.922640

3. Marko Šterk, Lidija Križančić Bombek, Maša Skelin Klemen, Marjan Slak Rupnik, Marko Marhl, Andraž Stožer, Marko Gosak, 2021. *NMDA receptor inhibition increases, synchronizes, and stabilizes the collective pancreatic beta cell activity: Insights through multilayer network analysis*. PLoS Computational Biology 17(5), e1009002. DOI: https://doi.org/10.1371/journal.pcbi.1009002

4. Marko Šterk, Jurij Dolenšek, Lidija Križančić Bombek, Rene Markovič, Darko Zakelšek, Matjaž Perc, Viljem Pohorec, Andraž Stožer, Marko Gosak, 2021. *Assessing the origin and velocity of Ca2+ waves in three-dimensional tissue: Insights from a mathematical model and confocal imaging in mouse pancreas tissue slices*. Communications in Nonlinear Science and Numerical Simulation 93, 105498. DOI: https://doi.org/10.1016/j.cnsns.2020.105495

### Citation
If you use this analysis suite for any publication please cite this work