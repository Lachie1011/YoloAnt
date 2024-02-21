"""
    projectPage.py
"""

import sys

from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QListWidget, QSizePolicy, QVBoxLayout, QSpacerItem, QGraphicsDropShadowEffect, QHBoxLayout
from PyQt6.QtGui import QCursor, QFont, QColor, QIcon
from pyqtgraph import PlotWidget, plot

import pyqtgraph as pg

from yoloAnt_ui import Ui_MainWindow
from utils.switch import Switch
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

        dropshadowEffect = QGraphicsDropShadowEffect()
        dropshadowEffect.setBlurRadius(10)
        color = QColor(self.app.theme.colours['app.dropshadow'])
        dropshadowEffect.setColor(color)
        dropshadowEffect.setOffset(0,2)

        self.ui.descriptionFrame.setGraphicsEffect(dropshadowEffect)
        self.ui.descriptionFrame.setStyleSheet("QFrame{"
                                               "border-radius: 5px;"
                                               f"background-color: {self.app.theme.colours['panel.background']};}}")    

        dropshadowEffect2 = QGraphicsDropShadowEffect()
        dropshadowEffect2.setBlurRadius(10)
        color = QColor(self.app.theme.colours['app.dropshadow'])
        dropshadowEffect2.setColor(color)
        dropshadowEffect2.setOffset(0,2)

        self.ui.mlInfoFrame.setGraphicsEffect(dropshadowEffect2)
        self.ui.mlInfoFrame.setStyleSheet("QFrame{"
                                          "border-radius: 5px;"
                                          f"background-color: {self.app.theme.colours['panel.background']};}}")       

        dropshadowEffect3 = QGraphicsDropShadowEffect()
        dropshadowEffect3.setBlurRadius(10)
        color = QColor(self.app.theme.colours['app.dropshadow'])
        dropshadowEffect3.setColor(color)
        dropshadowEffect3.setOffset(0,2)
        self.ui.datasetHealthFrame.setGraphicsEffect(dropshadowEffect3)                                                                         
        self.ui.datasetHealthFrame.setStyleSheet("QFrame{"
                                                 "border-radius: 5px;"
                                                 f"background-color: {self.app.theme.colours['panel.background']};}}")  

        dropshadowEffect4 = QGraphicsDropShadowEffect()
        dropshadowEffect4.setBlurRadius(10)
        color = QColor(self.app.theme.colours['app.dropshadow'])
        dropshadowEffect4.setColor(color)
        dropshadowEffect4.setOffset(0,2)
        self.ui.classInfoFrame.setGraphicsEffect(dropshadowEffect4)                                                     
        self.ui.classInfoFrame.setStyleSheet("QFrame{"
                                             "border-radius: 5px;"
                                             f"background-color: {self.app.theme.colours['panel.background']};}}")

        self.ui.projectNameLbl.setStyleSheet("QLabel{"
                                             f"font: 75 bold 16pt {self.app.fontTypeHeader};"
                                             f"color: {self.app.theme.colours['font.header']};}}") 

        self.ui.mlFrameLbl.setStyleSheet("QLabel{"
                                         f"font: 75 bold 16pt {self.app.fontTypeHeader};"
                                         f"color: {self.app.theme.colours['font.header']};}}") 

        self.ui.mAPLbl.setStyleSheet("QLabel{"
                                         f"font: 75 12pt {self.app.fontTypeTitle};"
                                         f"color: {self.app.theme.colours['font.regular']};}}") 

        self.ui.precisionLbl.setStyleSheet("QLabel{"
                                         f"font: 75 12pt {self.app.fontTypeTitle};"
                                         f"color: {self.app.theme.colours['font.regular']};}}") 

        self.ui.recallLbl.setStyleSheet("QLabel{"
                                         f"font: 75 12pt {self.app.fontTypeTitle};"
                                         f"color: {self.app.theme.colours['font.regular']};}}") 

        self.ui.mAPValueLbl.setStyleSheet("QLabel{"
                                         f"font: 75 bold 14pt {self.app.fontTypeTitle};"
                                         f"color: {self.app.theme.colours['font.header']};}}") 

        self.ui.precisionValueLbl.setStyleSheet("QLabel{"
                                         f"font: 75 bold 14pt {self.app.fontTypeTitle};"
                                         f"color: {self.app.theme.colours['font.header']};}}") 

        self.ui.recallValueLbl.setStyleSheet("QLabel{"
                                         f"font: 75 bold 14pt {self.app.fontTypeTitle};"
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

        self.ui.mdlSelLbl.setStyleSheet("QLabel{"
                                        f"font: 75 13pt {self.app.fontTypeTitle};"
                                        f"color: {self.app.theme.colours['font.header']};}}")

        self.ui.colourHeaderLbl.setStyleSheet("QLabel{"
                                              f"font: 75 13pt {self.app.fontTypeTitle};"
                                              f"color: {self.app.theme.colours['font.regular']};}}")

        self.ui.classNameLbl.setStyleSheet("QLabel{"
                                           f"font: 75 13pt {self.app.fontTypeTitle};"
                                           f"color: {self.app.theme.colours['font.regular']};}}")

        self.ui.classBalanceHeaderLbl.setStyleSheet("QLabel{"
                                                    f"font: 75 13pt {self.app.fontTypeTitle};"
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

        self.ui.addDatasetHealthWidgetBtn.setStyleSheet("QPushButton{"
                                          f"background-color: {self.app.theme.colours['buttonFilled.background']};"
                                          f"border : 1px solid {self.app.theme.colours['buttonFilled.background']};"
                                          "border-radius: 10px;}"
                                          "QPushButton::hover{"
                                          f"background-color: {self.app.theme.colours['buttonFilled.hover']};"
                                          f"border : 1px solid {self.app.theme.colours['buttonFilled.hover']};}}")
        self.ui.addDatasetHealthWidgetBtn.setIcon(QIcon("icons/icons8-plus-button-24.png"))

        self.classEditSwitchBtn = Switch()
        self.classEditSwitchLayout = QHBoxLayout()
        self.classEditSwitchLayout.addWidget(self.classEditSwitchBtn)
        self.classEditSwitchLayout.setContentsMargins(0,0,0,0)
        self.ui.classInfoEditFrame.setLayout(self.classEditSwitchLayout)

        self.datasetHealthEditSwitchBtn = Switch()
        self.datasetHealthEditSwitchLayout = QHBoxLayout()
        self.datasetHealthEditSwitchLayout.addWidget(self.datasetHealthEditSwitchBtn)
        self.datasetHealthEditSwitchLayout.setContentsMargins(0,0,0,0)
        self.ui.datasetHealthEditFrame.setLayout(self.datasetHealthEditSwitchLayout)

        self.projectDescriptionEditSwitchBtn = Switch()
        self.projectDescriptionEditSwitchLayout = QHBoxLayout()
        self.projectDescriptionEditSwitchLayout.addWidget(self.projectDescriptionEditSwitchBtn)
        self.projectDescriptionEditSwitchLayout.setContentsMargins(0,0,0,0)
        self.ui.projectDescriptionEditFrame.setLayout(self.projectDescriptionEditSwitchLayout)

        self.ui.mlModelComboBox.setStyleSheet("QComboBox{"
                                              f"font: 75 12pt {self.app.fontTypeRegular};"
                                              "border-radius: 5px;"
                                              f"background-color: {self.app.theme.colours['panel.sunken']};}}"
                                              "QComboBox::drop-down:button{"
                                              f"background-color: {self.app.theme.colours['panel.sunken']};"
                                              "border-radius: 5px}"
                                              "QComboBox::drop-down{"
                                              f"color: {self.app.theme.colours['panel.sunken']};}}"
                                              "QComboBox::down-arrow{"
                                              "image: url(icons/icons8-drop-down-arrow-10.png)}")

        self.ui.projectImageLbl.setStyleSheet("QLabel{"
                                              f"background-color: {self.app.theme.colours['panel.sunken']};}}")


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



        


