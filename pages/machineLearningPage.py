"""
    machineLearningPage.py
"""

import pyqtgraph as pg
from PyQt6.QtWidgets import QGraphicsDropShadowEffect, QHBoxLayout, QLabel
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QSizePolicy

from model import Model
from dialogs.createModelDialog import CreateModelDialog
from customWidgets.customBaseObjects.customUserInputQLineEdit import CustomUserInputQLineEdit
from customWidgets.customBaseObjects.customQComboBox import CustomQComboBox
from yoloAnt_ui import Ui_MainWindow

class MachineLearningPage():
    """
        Class to set up the functionality for the machineLearning page
    """
    def __init__(self, app) -> None:
        # TODO: fix up app type to yoloant app involes add futyure annotations and some if typing
        self.app = app
        self.ui = app.ui

        self.readOnly = True
        self.model = None

        # Initially set up machine learning page with readonly set to True
        self.__setEditMode(self.readOnly)

        # Connecting signals and slots
        self.ui.editPageBtn.toggled.connect(lambda toggled: self.__setEditMode(not toggled)) 
        # self.ui.createModelBtn.clicked.connect(self.__openNewModelDialog)
  
        self.__setupPagePalette()
        self.__setupStyleSheet()

        # for now just load the page at start TODO: this will have to change based on selected model
        #self.loadPage()

    def __setEditMode(self, toggled):
        """ Connects the edit button to editable widgets """ 
        # self.ui.deviceLineEdit.setReadOnly(toggled)
        # self.ui.imageSizeLineEdit.setReadOnly(toggled)
        # self.ui.modelTypeLineEdit.setReadOnly(toggled)

    def __openNewModelDialog(self) -> None:
        """ Creates a new model """
        self.createModelDialog = CreateModelDialog(self.app.theme.colours, self.app.fontTypeRegular, self.app.fontTypeHeader)
        self.createModelDialog.exec()

        if self.createModelDialog.result() == 1:
            model = Model(self.createModelDialog.modelName)
            # Add model to runtime list 
            self.loadPage(model)

    def __resetPage(self) -> None:
        """ Resets page back to init state """
        # Reset user input fields
        self.ui.batchLineEdit.setText("")
        self.ui.deviceLineEdit.setText("")
        self.ui.epochLineEdit.setText("")
        self.ui.imageSizeLineEdit.setText("")
        self.ui.modelTypeLineEdit.setText("")
        self.ui.modelNameLineEdit.setText("")
        self.ui.workersLineEdit.setText("")
        
        # TODO: Reset stacked widgets

        # Update attributes panel

    def loadPage(self, model) -> None:
        """ Loads all information and functionality """
        self.__resetPage()
        self.__populateAttributesPanel()  # is overwritten by a trained model
        if model is None:
            # If no model, keep current state
            if self.model:
                self.__populateFields(self.model)
            return
        
        self.model = model
        self.__populateFields(self.model)
    
    def __populateFields(self, model) -> None:
        """ Populates fields from an existing model """
        self.ui.stateLineEdit.setText(model.state.value)
        self.ui.modelNameLineEdit.setText(model.modelName)

    def __populateAttributesPanel(self) -> None:
        """ Populates the attributes panel"""
        annotatedImagesCount = 0  # Probably should do this better - but a TODO
        for image in self.app.project.annotationDataset:
            if image.annotated:
                annotatedImagesCount = annotatedImagesCount + 1
        self.ui.annotatedImagesLineEdit.setText(str(annotatedImagesCount))

    def __createPlots(self) -> None: 
        """ Creates a plot and populates the two plots on the trained ML page """
    
        # TODO: placeholder plot atm
        xData = [1,2,3,4,5,6,7,8,9,10]
        yData = [30,32,34,32,33,31,29,32,35,45]

        pen = pg.mkPen(color=(255,255,200), width=2)
    
        # Updating accuracy plot
        self.ui.accuracyPlotWidget.setBackground((65, 66, 64))
        self.ui.accuracyPlotWidget.setStyleSheet("border : 1px solid; border-color: rgb(65, 66, 64);")
    
        # plot data: x, y values
        self.ui.accuracyPlotWidget.plotItem.getAxis('left').setPen(pen)
        self.ui.accuracyPlotWidget.plotItem.getAxis('bottom').setPen(pen)
        self.ui.accuracyPlotWidget.plot(xData, yData, pen=pen)

        # Updating loss plot
        self.ui.lossPlotWidget.setBackground((65, 66, 64))
        self.ui.lossPlotWidget.setStyleSheet("border : 1px solid; border-color: rgb(65, 66, 64);")
    
        # plot data: x, y values
        self.ui.lossPlotWidget.plotItem.getAxis('left').setPen(pen)
        self.ui.lossPlotWidget.plotItem.getAxis('bottom').setPen(pen)
        self.ui.lossPlotWidget.plot(xData, yData, pen=pen)

    def __setupPagePalette(self) -> None:
        dropshadowEffect = QGraphicsDropShadowEffect()
        dropshadowEffect.setBlurRadius(10)
        color = QColor(self.app.theme.colours['app.dropshadow'])
        dropshadowEffect.setColor(color)
        dropshadowEffect.setOffset(0,2)

        self.ui.ConsoleOverallFrame.setGraphicsEffect(dropshadowEffect)
        self.ui.ConsoleOverallFrame.setStyleSheet("QFrame{"
                                                  "border-radius: 5px;"
                                                  f"background-color: {self.app.theme.colours['panel.background']};}}")    

        dropshadowEffect2 = QGraphicsDropShadowEffect()
        dropshadowEffect2.setBlurRadius(10)
        color = QColor(self.app.theme.colours['app.dropshadow'])
        dropshadowEffect2.setColor(color)
        dropshadowEffect2.setOffset(0,2)

        self.ui.MlInfoFrame.setGraphicsEffect(dropshadowEffect2)
        self.ui.MlInfoFrame.setStyleSheet("QFrame{"
                                          "border-radius: 5px;"
                                          f"background-color: {self.app.theme.colours['panel.background']};}}")            

    def __setupStyleSheet(self) -> None:
        """ Sets the style sheet for the page"""
        # self.ui.createModelBtn.setStyleSheet("QPushButton{"
        #                                   f"background-color: {self.app.theme.colours['buttonFilled.background']};"
        #                                   f"border : 1px solid {self.app.theme.colours['buttonFilled.background']};"
        #                                   "border-radius: 5px;"
        #                                   f"font: 75 bold 12pt {self.app.fontTypeTitle};}}"
        #                                   "QPushButton::hover{"
        #                                   f"background-color: {self.app.theme.colours['buttonFilled.hover']};"
        #                                   f"border : 1px solid {self.app.theme.colours['buttonFilled.hover']};}}")

        self.stateInfoLabel = QLabel()
        self.stateInfoLabel.setText('Not Trained')
        self.stateInfoLabel.setStyleSheet("QLabel{"
                                          f"color: {self.app.theme.colours['font.regular']};"
                                          f"font: 75 bold 12pt {self.app.fontTypeRegular};}}")
        self.stateInfoLayout = QHBoxLayout()
        self.stateInfoLayout.addWidget(self.stateInfoLabel)
        self.stateInfoLayout.setContentsMargins(0,0,0,0)
        self.ui.stateInfoFrame.setLayout(self.stateInfoLayout)

        self.imagesAnnoInfoLabel = QLabel()
        self.imagesAnnoInfoLabel.setText('100')
        self.imagesAnnoInfoLabel.setStyleSheet("QLabel{"
                                          f"color: {self.app.theme.colours['font.regular']};"
                                          f"font: 75 bold 12pt {self.app.fontTypeRegular};}}")
        self.imagesAnnoInfoLayout = QHBoxLayout()
        self.imagesAnnoInfoLayout.addWidget(self.imagesAnnoInfoLabel)
        self.imagesAnnoInfoLayout.setContentsMargins(0,0,0,0)
        self.ui.imagesAnnoInfoFrame.setLayout(self.imagesAnnoInfoLayout)


        self.classImbalInforLabel = QLabel()
        self.classImbalInforLabel.setText('Not Balanced')
        self.classImbalInforLabel.setStyleSheet("QLabel{"
                                          f"color: {self.app.theme.colours['font.regular']};"
                                          f"font: 75 bold 12pt {self.app.fontTypeRegular};}}")
        self.classImbalInforLayout = QHBoxLayout()
        self.classImbalInforLayout.addWidget(self.classImbalInforLabel)
        self.classImbalInforLayout.setContentsMargins(0,0,0,0)
        self.ui.classImbalInforFrame.setLayout(self.classImbalInforLayout)

        self.modelNameComboBox = CustomQComboBox(self.app.theme.colours, self.app.fontTypeRegular)
        self.modelNameComboBox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.modelNameComboLayout = QHBoxLayout()
        self.modelNameComboLayout.addWidget(self.modelNameComboBox)
        self.modelNameComboLayout.setContentsMargins(0,0,0,0)
        self.ui.modelNameComboFrame.setLayout(self.modelNameComboLayout)

        self.modelTypeComboBox = CustomQComboBox(self.app.theme.colours, self.app.fontTypeRegular)
        self.modelTypeComboBox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.modelTypeLayout = QHBoxLayout()
        self.modelTypeLayout.addWidget(self.modelTypeComboBox)
        self.modelTypeLayout.setContentsMargins(0,0,0,0)
        self.ui.modelTypeComboFrame.setLayout(self.modelTypeLayout)

        self.deviceComboBox = CustomQComboBox(self.app.theme.colours, self.app.fontTypeRegular)
        self.deviceComboBox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.deviceLayout = QHBoxLayout()
        self.deviceLayout.addWidget(self.deviceComboBox)
        self.deviceLayout.setContentsMargins(0,0,0,0)
        self.ui.deviceComboFrame.setLayout(self.deviceLayout)

        self.modelNameLineEdit = CustomUserInputQLineEdit(self.app.theme.colours, self.app.fontTypeRegular)
        self.modelNameLineEdit.setText('Project-V1-Test')
        self.modelNameLayout = QHBoxLayout()
        self.modelNameLayout.addWidget(self.modelNameLineEdit)
        self.modelNameLayout.setContentsMargins(0,0,0,0)
        self.ui.modelNameInputFrame.setLayout(self.modelNameLayout)
        self.modelNameLineEdit.editingFinished.connect(lambda: self.modelNameLineEdit.clearFocus())

        self.epochsLineEdit = CustomUserInputQLineEdit(self.app.theme.colours, self.app.fontTypeRegular)
        self.epochsLineEdit.setText('100')
        self.epochsLayout = QHBoxLayout()
        self.epochsLayout.addWidget(self.epochsLineEdit)
        self.epochsLayout.setContentsMargins(0,0,0,0)
        self.ui.epochsInputFrame.setLayout(self.epochsLayout)
        self.epochsLineEdit.editingFinished.connect(lambda: self.epochsLineEdit.clearFocus())

        self.batchsizeLineEdit = CustomUserInputQLineEdit(self.app.theme.colours, self.app.fontTypeRegular)
        self.batchsizeLineEdit.setText('64')
        self.batchsizeLayout = QHBoxLayout()
        self.batchsizeLayout.addWidget(self.batchsizeLineEdit)
        self.batchsizeLayout.setContentsMargins(0,0,0,0)
        self.ui.batchsizeInputFrame.setLayout(self.batchsizeLayout)
        self.batchsizeLineEdit.editingFinished.connect(lambda: self.batchsizeLineEdit.clearFocus())

        self.workersLineEdit = CustomUserInputQLineEdit(self.app.theme.colours, self.app.fontTypeRegular)
        self.workersLineEdit.setText('64')
        self.workersLayout = QHBoxLayout()
        self.workersLayout.addWidget(self.workersLineEdit)
        self.workersLayout.setContentsMargins(0,0,0,0)
        self.ui.workersInputFrame.setLayout(self.workersLayout)
        self.workersLineEdit.editingFinished.connect(lambda: self.workersLineEdit.clearFocus())

        self.widthLineEdit = CustomUserInputQLineEdit(self.app.theme.colours, self.app.fontTypeRegular)
        self.widthLineEdit.setPlaceholderText('width')
        self.widthLayout = QHBoxLayout()
        self.widthLayout.addWidget(self.widthLineEdit)
        self.widthLayout.setContentsMargins(0,0,0,0)
        self.ui.widthInputFrame.setLayout(self.widthLayout)
        self.widthLineEdit.editingFinished.connect(lambda: self.widthLineEdit.clearFocus())

        self.heightLineEdit = CustomUserInputQLineEdit(self.app.theme.colours, self.app.fontTypeRegular)
        self.heightLineEdit.setPlaceholderText('height')
        self.heightLayout = QHBoxLayout()
        self.heightLayout.addWidget(self.heightLineEdit)
        self.heightLayout.setContentsMargins(0,0,0,0)
        self.ui.heightInputFrame.setLayout(self.heightLayout)
        self.heightLineEdit.editingFinished.connect(lambda: self.heightLineEdit.clearFocus())

        self.ui.trainBtn.setStyleSheet("QPushButton{"
                                       f"background-color: {self.app.theme.colours['buttonFilled.background']};"
                                       f"border : 1px solid {self.app.theme.colours['buttonFilled.background']};"
                                       "border-radius: 10px;"
                                       f"font: 75 bold 12pt {self.app.fontTypeTitle};}}"
                                       "QPushButton::hover{"
                                       f"background-color: {self.app.theme.colours['buttonFilled.hover']};"
                                       f"border : 1px solid {self.app.theme.colours['buttonFilled.hover']};}}")