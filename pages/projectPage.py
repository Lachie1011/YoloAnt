"""
    projectPage.py
"""

import sys
from yoloAnt_ui import Ui_MainWindow

class ProjectPage():
    """
        Class to set up the functionality for the project page
    """
    def __init__(self, app) -> None:
        # TODO: fix up app type to yoloant app involes add futyure annotations and some if typing
        self.app = app
        self.ui = app.ui

    def __populateFields(self) -> None:
        """ Populates the fields for the project page from the project.yaml """
        self.ui.projectNameLbl.setText(self.app.project.name)
        self.ui.projectDescriptionLbl.setText(self.app.project.description)
        self.ui.datasetPathTxt.setText(self.app.project.dataset)

    def loadPage(self) -> None:
        """ Loads all information and functionality """
        self.__populateFields()