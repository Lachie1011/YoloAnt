"""
    projectPage.py
"""

import sys

from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QListWidget, QSizePolicy, QVBoxLayout, QSpacerItem
from PyQt6.QtGui import QCursor, QFont
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

        # Setup theme colour palette
        self.__setupPagePalette()

        # Setup style sheet of page
        self.__setupStyleSheet()
        
        # Create class list
        self.__createClassList()

        self.numOfClasses = 30

        # Connect signals and slots
        self.ui.addClassBtn.clicked.connect(lambda: self.__instantiateCreateClassDialog())

    def __setupPagePalette(self) -> None:
        self.ui.descriptionFrame.setStyleSheet(self.ui.descriptionFrame.styleSheet() +
                                               f"background: {self.app.theme.colours['panel.background']};")       
        self.ui.mlInfoFrame.setStyleSheet(self.ui.mlInfoFrame.styleSheet() + 
                                          f"background: {self.app.theme.colours['panel.background']};")                                      
        self.ui.datasetHealthFrame.setStyleSheet(self.ui.datasetHealthFrame.styleSheet() +
                                             f"background: {self.app.theme.colours['panel.background']};")  
        self.ui.classInfoFrame.setStyleSheet(self.ui.classInfoFrame.styleSheet() + 
                                                   f"background: {self.app.theme.colours['panel.background']};")
                                                
        self.ui.projectNameLbl.setStyleSheet("QLabel{"
                                             f"font: 75 bold 16pt {self.app.fontTypeHeader};"
                                             f"color: {self.app.theme.colours['font.header']};}}") 

        self.ui.mlFrameLbl.setStyleSheet("QLabel{"
                                         f"font: 75 bold 16pt {self.app.fontTypeHeader};"
                                         f"color: {self.app.theme.colours['font.header']};}}") 

        self.ui.healthLbl.setStyleSheet("QLabel{"
                                        f"font: 75 bold 16pt {self.app.fontTypeHeader};"
                                        f"color: {self.app.theme.colours['font.header']};}}") 

        self.ui.classInfoFrameLbl.setStyleSheet("QLabel{"
                                                f"font: 75 bold 16pt {self.app.fontTypeHeader};"
                                                f"color: {self.app.theme.colours['font.header']};}}")

        self.ui.projectDescriptionEdit.setStyleSheet("QTextEdit{"
                                                     f"font: 75 11pt {self.app.fontTypeRegular};"
                                                     f"color: {self.app.theme.colours['font.regular']};}}")

        self.ui.colourHeaderLbl.setStyleSheet("QLabel{"
                                              f"font: 75 12pt {self.app.fontTypeTitle};"
                                              f"color: {self.app.theme.colours['font.regular']};}}")

        self.ui.classNameLbl.setStyleSheet("QLabel{"
                                           f"font: 75 12pt {self.app.fontTypeTitle};"
                                           f"color: {self.app.theme.colours['font.regular']};}}")

        self.ui.classBalanceHeaderLbl.setStyleSheet("QLabel{"
                                                    f"font: 75 12pt {self.app.fontTypeTitle};"
                                                    f"color: {self.app.theme.colours['font.regular']};}}")

        self.ui.classInfoBar.setStyleSheet(self.ui.classInfoBar.styleSheet() +
                                           f"background: {self.app.theme.colours['panel.foreground']}")

    def __setupStyleSheet(self) -> None: 
        """ Sets the style sheet for the page """
        self.ui.addClassBtn.setStyleSheet("QPushButton{"
                                          f"background-color: {self.app.theme.colours['buttonFilled.background']};"
                                          f"border : 1px solid {self.app.theme.colours['buttonFilled.background']};"
                                          "border-radius: 10px;"
                                          f"font: 75 bold 12pt {self.app.fontTypeTitle};}}"
                                          "QPushButton::hover{"
                                          f"background-color: {self.app.theme.colours['buttonFilled.hover']};"
                                          f"border : 1px solid {self.app.theme.colours['buttonFilled.hover']};}}")


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

        self.classListWidget = CustomClassQListWidget(self.app.theme.colours, False)
        self.classListWidget.setObjectName("classListProjectPageWidget")
        self.veritcalSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.classListLayout = QVBoxLayout()
        self.classListLayout.addWidget(self.classListWidget)
        self.classListLayout.addItem(self.veritcalSpacer)
        self.ui.classListFrame.setLayout(self.classListLayout)

    def __instantiateCreateClassDialog(self) -> None:
        """ Instanciates the create class dialog """
        self.createClassDialog = CreateClassDialog(self.classListWidget, self.numOfClasses, self.app.theme.colours, self.app.fontTypeRegular, self.app.fontTypeHeader)



        


