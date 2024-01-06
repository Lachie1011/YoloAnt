"""
    projectPage.py
"""

import sys

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtGui import QCursor
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

from yoloAnt_ui import Ui_MainWindow
from events.hoverEvent import BackgroundHoverEvent
from classManager import ClassManager

class ProjectPage():
    """
        Class to set up the functionality for the project page
    """
    def __init__(self, app) -> None:
        # TODO: fix up app type to yoloant app involes add futyure annotations and some if typing
        self.app = app
        self.ui = app.ui
        self.classManager = ClassManager(self)
        self.classManager.addClassToImbalanceList("Test", 10, 30, '0, 201, 52')
        self.classManager.addClassToImbalanceList("Test2", 13, 30, '0, 201, 52')
        self.classManager.addClassToImbalanceList("Test3", 18, 30, '0, 201, 52')
        self.classManager.addClassToImbalanceList("Test4", 1, 30, '0, 201, 52')
        self.__connectHover()

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

    def __connectHover(self) -> None:
        """ 
            Installs the hover event filter onto the project page buttons.
        """
    
        # Applying hover events and cursor change to Navigation Buttons
        self.ui.addClassBtn.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btnBackgroundHoverEvent = BackgroundHoverEvent(self.ui.addClassBtn, "105, 105, 105", "85, 87, 83")
        self.ui.addClassBtn.installEventFilter(self.btnBackgroundHoverEvent)

        self.ui.classListWidget.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.listItembackgroundHoverEvent = BackgroundHoverEvent(self.ui.addClassBtn, "65, 66, 64", "85, 87, 83")
        self.ui.classListWidget.installEventFilter(self.listItembackgroundHoverEvent)
