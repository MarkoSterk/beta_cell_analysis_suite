"""
Entry point for the analysis
"""
# pylint: disable=W0702
from methods.islet import Islet
from methods.router import Router

islet = Islet()
router = Router()

routes = {
    1: islet.first_responder_analysis,
    2: islet.filter_traces,
    3: islet.smooth_traces,
    4: islet.binarize_traces,
    5: islet.exclude_traces,
    6: islet.corr_coact_analysis,
    7: islet.cell_activity_analysis,
    99: islet.save_configs_to_data,
    'load': islet.load_data,
    'bundle': islet.bundle_data
}

islet.load_configs()
router.register_routes(routes)
router.print_options()
while True:
    router.parse_input(input('Select analysis step [number/string]: '))
    islet.load_configs()
    router.route()
