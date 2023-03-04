"""
Router default/config options
"""

class RouterConfig:
    """
    Main config class for router
    """
    # Excluded methods for RUN_ALL:
    # 0: run_all_methods (obviously)
    # 1: first responder analysis
    # exit: exits program
    # init: loads raw data
    # options: prints options

    EXCLUDE_METHODS_RUN_ALL = [0, 1, 'exit', 'options', 'init']

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
            options: Prints available options,
            load: Loads any existing data (preprocessed)
            init: Loads raw data with provided configurations - RUN FIRST!
            """

    RESERVED_ROUTES = ['options', 'exit', 0]
    INVALID_METHOD_ERROR = 'Please select a valid method.'
