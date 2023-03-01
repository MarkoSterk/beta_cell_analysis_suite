"""
All general ploting configurations
"""
import matplotlib.pyplot as plt

####DON'T CHANGE
# Matplotlib configuration
#Font sizes for plots
SMALL_TEXT_SIZE = 6
MEDIUM_TEXT_SIZE = 6
BIGGER_TEXT_SIZE = 8

CONVERSION = 2.54 #from inches to cm
PANEL_WIDTH = 8.0/CONVERSION #8 cm panel width
PANEL_HEIGHT = 4.0/CONVERSION #4 cm panel height

MEDIAN_PROPS = {
    'color': 'black'
}

BOX_PROPS = {
    'color': 'black',
    'facecolor': 'dimgray'
}

################Matplotlib configurations#######################
plt.rc('font', size=SMALL_TEXT_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_TEXT_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_TEXT_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_TEXT_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_TEXT_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_TEXT_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_TEXT_SIZE)  # fontsize of the figure title
########################################################################
