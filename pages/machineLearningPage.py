"""
    machineLearningPage.py
"""

import sys
from yoloAnt_ui import Ui_MainWindow

class MachineLearningPage():
    """
        Class to set up the functionality for the machineLearning page
    """
    def __init__(self, app) -> None:
        # TODO: fix up app type to yoloant app involes add futyure annotations and some if typing
        self.app = app
        self.ui = app.ui