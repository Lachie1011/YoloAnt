"""
    startPage.py
"""

import os
import sys

from project import Project

from yoloAnt_ui import Ui_MainWindow

class StartPage():
    """
        Class to set up the functionality for the start page
    """
    def __init__(self, ui: Ui_MainWindow) -> None:
        """ init """
        self.ui = ui

        # Member variables
        self.project = None

        # Connecting signals and slots for the page
        self.__connectProjectButtons()
        self.__connectIconHoverFunc()

    def __connectProjectButtons(self) -> None:
        """ connects the create and open project buttons"""
        self.ui.createProjectBtn.clicked.connect(lambda: self.__handleProject(True))
        self.ui.openProjecBtn.clicked.connect(lambda: self.__handleProject(False))

    def __handleProject(self, createProject: bool) -> None:
        """ handles the flow of project operation"""
        if(createProject):
            # opens a new dialog to set up the project
            self.project = Project(True, "todo")
        else:
            # opens file explorer
            print(os.system('nautilus --select %s' % os.getcwd()))
            self.project = Project(False, "todo")

        # update navigation panel and switch dir
        self.ui.mlTabBtn.setChecked(False)
        self.ui.annotTabBtn.setChecked(False)
        self.ui.projectsTabBtn.setChecked(True)
        self.ui.stackedWidget.setCurrentIndex(2)

    def __connectIconHoverFunc(self) -> None:
        """ Connects the hover over functionality to icons """
        pass
