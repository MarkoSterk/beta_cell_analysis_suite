"""
App router class
"""
import sys
from typing import Union
from methods.router_configs import RouterConfig

class Router(RouterConfig):
    """
    The main app router class
    """

    def __init__(self):
        self.routes = {
            'options': self.print_options,
            'exit': sys.exit,
            0: self.run_all_steps
        }
        self.input = None

    def register_routes(self, routes: dict):
        """
        Registers all routes to the router
        """
        for key, route in routes.items():
            if key not in self.RESERVED_ROUTES:
                self.routes[key] = route
            else:
                raise KeyError('Route tries to override existing or built-in route!')

    def parse_input(self, input_text: str) -> Union[str, int]:
        """
        Parses the provided input.
        Tries to convert to integer. If conversion fails it returns the original string
        """
        try:
            input_text = int(input_text)
        except ValueError:
            pass
        self.input = input_text

    def route(self):
        """
        Goes to next route
        """
        if self.input in self.routes:
            self.routes[self.input]()
        else:
            print(self.INVALID_METHOD_ERROR)

    def run_all_steps(self):
        """
        Runs all available analysis methods in sequence except those
        in the EXCLUDE_METHODS_RUN_ALL list
        """
        for key, method in self.routes.items():
            if key not in self.EXCLUDE_METHODS_RUN_ALL:
                method()

    def print_options(self):
        """
        Prints available options to screen
        """
        print(self.ANALYSIS_OPTIONS)
