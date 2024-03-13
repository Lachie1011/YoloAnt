"""
    startPage.py
"""

import os
import sys

from project import Project
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QFileDialog
from yoloAnt_ui import Ui_MainWindow
from dialogs.createProjectDialog import CreateProjectDialog

class StartPage():
    """
        Class to set up the functionality for the start page
    """
    def __init__(self, app) -> None:
        """ init """
        # TODO: fix up app type to yoloant app involes add futyure annotations and some if typing
        self.app = app
        self.ui = app.ui

        # Member variables
        self.project = None

        # Setup stylesheet
        self.__setupPageStyleSheet()

        # Connecting signals and slots for the page
        self.__connectProjectButtons()
        self.__connectIconHover()

    def __connectProjectButtons(self) -> None:
        """ Connects the create and open project buttons"""
        self.ui.createProjectBtn.clicked.connect(lambda: self.__handleProject(True))
        self.ui.openProjecBtn.clicked.connect(lambda: self.__handleProject(False))

    def __handleProject(self, createProject: bool) -> None:
        """ Handles the flow of project operation"""
        self.project = Project()
        if(createProject):
            # opens a new dialog to set up the project
            createProjectDialog = CreateProjectDialog()
            createProjectDialog.exec()
            if createProjectDialog.result() == 1:
                self.project.createProject(createProjectDialog.projectName, createProjectDialog.imageDirectory)
                self.app.project = self.project
                # update navigation panel and switch dir TODO: create functions that wrap the navigation as below
                self.ui.mlTabBtn.setChecked(False)
                self.ui.annotTabBtn.setChecked(False)
                self.ui.projectsTabBtn.setChecked(True)
                self.ui.stackedWidget.setCurrentIndex(2)
                self.app.projectPage.loadPage()
        else:
            # opens file explorer
            projectDir = str(QFileDialog.getExistingDirectory(self.app, "Select Directory"))        
            if os.path.exists(projectDir + "/project.yaml"): 
                self.project.loadProject(projectDir)  # attempt to load project
                self.app.project = self.project
                # update navigation panel and switch dir TODO: create functions that wrap the navigation as below
                self.ui.mlTabBtn.setChecked(False)
                self.ui.annotTabBtn.setChecked(False)
                self.ui.projectsTabBtn.setChecked(True)
                self.ui.stackedWidget.setCurrentIndex(2)
                self.app.projectPage.loadPage()

    def __connectIconHover(self) -> None:
        """ Connects the hover over functionality to icons """
        # updating stylesheets initially
        
        self.ui.openProjecBtn.setStyleSheet("QPushButton::hover{"
                                            f"background-color : {self.app.theme.colours['app.hover']};"
                                            "border-radius: 20px;}")

        self.ui.createProjectBtn.setStyleSheet("QPushButton::hover{"
                                            f"background-color : {self.app.theme.colours['app.hover']};"
                                            "border-radius: 20px;}")

    def __setupPageStyleSheet(self) -> None:
        self.ui.annotationToolsFrame.setStyleSheet(self.ui.annotationToolsFrame.styleSheet() + 
                                                   f"background: {self.app.theme.colours['panel.background']};")
