"""
    projectPage.py
"""

import sys

from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QListWidget, QSizePolicy, QVBoxLayout, QSpacerItem
from PyQt6.QtGui import QCursor 
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

from yoloAnt_ui import Ui_MainWindow
from customWidgets.customQObjects import CustomClassQListWidget
from customWidgets.projectClassListItemWidget import ProjectClassListItemWidget
from dialogs.createClassDialog import CreateClassDialog

class ProjectPage():
    """
        Class to set up the functionality for the project page
    """
    def __init__(self, app) -> None:
        # TODO: fix up app type to yoloant app involes add futyure annotations and some if typing
        self.app = app
        self.ui = app.ui

        self.__createClassList()
        self.__connectButtonHover()

        self.numOfClasses = 30

        # Connect signals and slots
        self.ui.addClassBtn.clicked.connect(lambda: self.__instantiateCreateClassDialog())

    def __populateFields(self) -> None:
        """ Populates the fields for the project page from the project.yaml """
        self.ui.projectNameLbl.setText(self.app.project.name)
        self.ui.projectDescriptionEdit.setText(self.app.project.description)
        self.ui.datasetPathLbl.setText(self.app.project.dataset)

    def loadPage(self) -> None:
        """ Loads all information and functionality """
        self.__populateFields()
        self.__createPlot()

    def __createPlot(self) -> None: 
        """ Creates a plot """
        # Updating plot stlying
        self.ui.graphWidget.setBackground((65, 66, 64))
        self.ui.graphWidget.setStyleSheet("border : 1px solid; border-color: rgb(65, 66, 64);")
    
        # TODO: placeholder plot atm
        xData = [1,2,3,4,5,6,7,8,9,10]
        yData = [30,32,34,32,33,31,29,32,35,45]

        # plot data: x, y values
        pen = pg.mkPen(color=(255,255,200), width=2)
        self.ui.graphWidget.plotItem.getAxis('left').setPen(pen)
        self.ui.graphWidget.plotItem.getAxis('bottom').setPen(pen)
        self.ui.graphWidget.plot(xData, yData, pen=pen)

    def __createClassList(self) -> None:
        """ Creates the class list """

        self.classListWidget = CustomClassQListWidget()
        self.classListWidget.setObjectName("classListProjectPageWidget")
        self.veritcalSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.classListLayout = QVBoxLayout()
        self.classListLayout.addWidget(self.classListWidget)
        self.classListLayout.addItem(self.veritcalSpacer)
        self.ui.classListFrame.setLayout(self.classListLayout)

    def __connectButtonHover(self) -> None:
        """ 
            Installs the hover event filter onto the project page buttons.
        """
    
        # Applying hover events and cursor change to Navigation Buttons
        self.ui.addClassBtn.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.ui.addClassBtn.setStyleSheet("QPushButton{"
                                          "background-color: rgb(85, 87, 83);"
                                          "border : 1px solid;"
                                          "border-radius: 10px;"
                                          "border-color:  rgb(85, 87, 83);"
                                          "font: 75 bold 12pt 'Gotham Rounded';}"
                                          "QPushButton::hover{background-color : rgb(105, 105, 105);"
                                          "border : 1px solid rgb(105, 105, 105);}")



    def __instantiateCreateClassDialog(self) -> None:
        """ Instanciates the create class dialog """
        self.createClassDialog = CreateClassDialog(self.classListWidget, self.numOfClasses)



        


