"""
    projectPage.py
"""

import cv2
import sys

from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QListWidget, QSizePolicy, QVBoxLayout, QSpacerItem, QGraphicsDropShadowEffect, QHBoxLayout, QFileDialog
from PyQt6.QtGui import QCursor, QFont, QColor, QIcon
from pyqtgraph import PlotWidget, plot

import pyqtgraph as pg

from yoloAnt_ui import Ui_MainWindow

from mlClass import MLClass
from custom_widgets.customBaseObjects.customClassQListWidget import CustomClassQListWidget
from custom_widgets.customBaseObjects.customPanelQLineEdit import CustomPanelQLineEdit
from custom_widgets.customBaseObjects.customPanelQTextEdit import CustomPanelQTextEdit
from custom_widgets.projectClassListItemWidget import ProjectClassListItemWidget
from custom_widgets.projectImagePushButton import ProjectImagePushButton
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
        self.readOnly = True

        # Connect signals and slots
        self.ui.addClassBtn.clicked.connect(lambda: self.__instantiateCreateClassDialog())
        self.ui.editPageBtn.toggled.connect(lambda toggled: self.setEditMode(toggled))
        self.projectImageBtn.clicked.connect(lambda: self.__updateProjectIcon())

        # Connect tracked editable widgets
        self.__connectTrackedEditableWidgets()

    def __populateWidgets(self) -> None:
        """ Populates the fields for the project page from the project.yaml """
        self.projectNameLineEdit.setText(self.app.project.name)
        self.projectDescriptionEdit.setText(self.app.project.description)
        if self.app.project.imageIconPath:
            self.__setProjectIcon(self.app.project.imageIconPath)
        self.__updateClassList()
        
    def __updateClassList(self) -> None:
        self.classListWidget.clear()
        for mlClass in self.app.project.classesDataset:
            classListItem = ProjectClassListItemWidget(mlClass.className,
                                                       0,
                                                       0,
                                                       mlClass.classColour,
                                                       self.app.theme.colours,
                                                       self.app.fontTypeRegular,
                                                       self.app.fontTypeHeader)
            self.classListWidget.addItemToListWidget(classListItem)

    def loadPage(self) -> None:
        """ Loads all information and functionality """
        if self.app.project:
            self.__populateWidgets()
            self.__createPlot()

    def __updateProjectIcon(self) -> None:
        """ Updates the projects icon """
        if self.readOnly:
            return
        # ERROR: For some reason when trying to use the native dialog - it hangs the app - tf??
        # Something to do with threading and the COM connection maybe?? 
        iconPath = QFileDialog.getOpenFileName(self.app, caption="Select Project Icon", options=QFileDialog.Option.DontUseNativeDialog) 
        self.__setProjectIcon(iconPath[0])

    def __setProjectIcon(self, iconPath) -> None:
        """ Sets the projects icon """
        if (iconPath is not None):
            image = cv2.imread(iconPath)
            if image is not None:
                self.projectImageBtn.setIcon(QtGui.QIcon(iconPath))
                self.projectImageBtn.setIconSize(QtCore.QSize(140,140))
                self.app.project.imageIconPath = iconPath

    def __connectTrackedEditableWidgets(self) -> None:
        """ Connects tracked editable widgets """
        self.projectNameLineEdit.editingFinished.connect(self.__updateProjectName)
        self.projectDescriptionEdit.editingFinished.connect(self.__updateProjectDescription)

    def __updateProjectName(self) -> None:
        """ Updates the project name """
        # Note this only updates the project yaml and in app, the project dir still remains the setObjectName
        if self.app.project:
            self.app.project.name = self.projectNameLineEdit.text()

    def __updateProjectDescription(self) -> None:
        """ Updates the project's description """
        if self.app.project:
            self.app.project.description = self.projectDescriptionEdit.toPlainText()

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
        self.createClassDialog = CreateClassDialog(self.app.theme.colours, self.app.fontTypeRegular, self.app.fontTypeHeader)
        self.createClassDialog.exec()
        if self.createClassDialog.isValid:
            mlClass = MLClass(self.createClassDialog.className, self.createClassDialog.selectedColour)
            self.app.project.classesDataset.append(mlClass) 
            self.__populateWidgets()

    def setEditMode(self, toggled) -> None:
        """ Enables edit mode for the project page """
        self.readOnly = not self.readOnly
        self.projectNameLineEdit.setEditMode(toggled)
        self.projectDescriptionEdit.setEditMode(toggled)
        self.projectImageBtn.setEditMode(toggled)
        self.classListWidget.setEditMode(toggled)

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
        self.projectNameLineEdit = CustomPanelQLineEdit(self.app.theme.colours, f"font: 75 bold 16pt {self.app.fontTypeRegular};")
        self.projectNameLineEdit.setText('Project Name')
        self.projectNameLayout = QHBoxLayout()
        self.projectNameLayout.addWidget(self.projectNameLineEdit)
        self.projectNameLayout.setContentsMargins(0,0,0,0)
        self.ui.projectNameTextFrame.setLayout(self.projectNameLayout)

        self.projectDescriptionEdit = CustomPanelQTextEdit(self.app.theme.colours, self.app.fontTypeRegular)
        self.projectDescriptionEdit.setText('Project description here.')
        self.projectDescriptionEditLayout = QHBoxLayout()
        self.projectDescriptionEditLayout.addWidget(self.projectDescriptionEdit)
        self.projectDescriptionEditLayout.setContentsMargins(0,0,0,0)
        self.ui.projectDescriptionEditFrame.setLayout(self.projectDescriptionEditLayout)

        self.projectImageBtn = ProjectImagePushButton(self.app.theme.colours)
        self.projectImageLayout = QVBoxLayout()
        self.projectImageLayout.addWidget(self.projectImageBtn)
        self.projectImageLayout.setContentsMargins(0,0,0,0)
        self.ui.projectImageBtnFrame.setLayout(self.projectImageLayout)

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

