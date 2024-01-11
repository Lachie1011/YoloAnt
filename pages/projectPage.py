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
from utils.classListWidget import ClassListWidget

class ProjectPage():
    """
        Class to set up the functionality for the project page
    """
    def __init__(self, app) -> None:
        # TODO: fix up app type to yoloant app involes add futyure annotations and some if typing
        self.app = app
        self.ui = app.ui

        self.__connectButtonHover()
        self.__connectClassList()

        self.classListWidget.addItemToListWidget("Test", 10, 30, '0, 201, 52')
        self.classListWidget.addItemToListWidget("Test2", 13, 30, '0, 201, 52')
        self.classListWidget.addItemToListWidget("Test3", 18, 30, '0, 201, 52')
        self.classListWidget.addItemToListWidget("Test4", 1, 30, '0, 201, 52')
        self.classListWidget.addItemToListWidget("Test5", 27, 30, '0, 201, 52')
        self.classListWidget.addItemToListWidget("Test6", 13, 30, '0, 201, 52')
        self.classListWidget.addItemToListWidget("Test7", 18, 30, '0, 201, 52')
        self.classListWidget.addItemToListWidget("Test8", 6, 30, '0, 201, 52')
        self.classListWidget.addItemToListWidget("Test9", 10, 30, '0, 201, 52')
        self.classListWidget.addItemToListWidget("Test10", 13, 30, '0, 201, 52')
        self.classListWidget.addItemToListWidget("Test11", 18, 30, '0, 201, 52')
        self.classListWidget.addItemToListWidget("Test12", 4, 30, '0, 201, 52')
        self.classListWidget.addItemToListWidget("Test13", 10, 30, '0, 201, 52')
        self.classListWidget.addItemToListWidget("Test14", 13, 30, '0, 201, 52')
        self.classListWidget.addItemToListWidget("Test15", 18, 30, '0, 201, 52')
        self.classListWidget.addItemToListWidget("Test16", 4, 30, '0, 201, 52')




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

    def __connectButtonHover(self) -> None:
        """ 
            Installs the hover event filter onto the project page buttons.
        """
    
        # Applying hover events and cursor change to Navigation Buttons
        self.ui.addClassBtn.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.ui.addClassBtn.setStyleSheet("QPushButton{background-color: rgb(85, 87, 83);"
                                          "border : 1px solid;"
                                          "border-radius: 10px;"
                                          "border-color:  rgb(85, 87, 83);"
                                          "font: 75 bold 12pt 'Gotham Rounded';}"
                                          "QPushButton::hover{background-color : rgb(105, 105, 105);"
                                          "border : 1px solid rgb(105, 105, 105);}")

    def __connectClassList(self) -> None:
        self.classListWidget = ClassListWidget()
        self.classListWidget.setObjectName("classListProjectPageWidget")
        self.veritcalSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.classListLayout = QVBoxLayout()
        self.classListLayout.addWidget(self.classListWidget)
        self.classListLayout.addItem(self.veritcalSpacer)
        self.ui.classListFrame.setLayout(self.classListLayout)


        


