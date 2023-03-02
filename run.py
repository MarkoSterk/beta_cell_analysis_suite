"""
Entry point for the analysis
"""

from methods.filt_traces import filter_data
from methods.smooth_traces import smooth_data
from methods.binarization import binarize_data
from methods.exclude_cells import exclude_data
from methods.corr_ca_analysis import corr_ca_analysis_data
from methods.cell_parameter_analysis import cell_activity_data

print("""
Available analysis steps are:
1: Time series filtration
2: Time series smoothing
3: Time series binarization
4: Excluding of cells and time series
5: Correlation/coactivity analysis
6: Cell activity parameter analysis
""")
analysis_step = input('Select analysis step [1-6]: ')

try:
    analysis_step = int(analysis_step)
except:
    # pylint: disable-next=W0719, W0707
    raise BaseException('You did not enter a valid number.')

if analysis_step == 1:
    filter_data()
elif analysis_step == 2:
    smooth_data()
elif analysis_step == 3:
    binarize_data()
elif analysis_step == 4:
    exclude_data()
elif analysis_step == 5:
    corr_ca_analysis_data()
elif analysis_step == 6:
    cell_activity_data()
else:
    print('Please select a valid analysis step.')
