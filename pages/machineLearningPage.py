"""
    machineLearningPage.py
"""

import torch
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
        self.loading = False

        self.__setupPagePalette()
        self.__setupStyleSheet()

        # Connecting signals and slots
        self.ui.editPageBtn.toggled.connect(lambda toggled: self.__setEditMode(not toggled)) 
        self.ui.createModelBtn.clicked.connect(self.__openNewModelDialog)
        self.modelNameComboBox.currentTextChanged.connect(lambda text: self.__updateLoadedModel(text))
        self.__connectEditableWidgets()

        # Initially set up machine learning page with readonly set to True
        self.__setEditMode(self.readOnly)

    def __updateLoadedModel(self, modelName):
        """ Loads a selected model from the combobox """
        if self.loading:
            return
        for model in self.app.project.modelDataset:
            if model.modelName == modelName:
                self.loadPage(model)
                return
        self.app.notificationManager.raiseNotification(f"Could not load model {modelName}")

    def __connectEditableWidgets(self) -> None:
        """ Connects all tracked editable widgets """
        self.batchsizeLineEdit.editingFinished.connect(self.__updateModelBatchSize)
        self.epochsLineEdit.editingFinished.connect(self.__updateModelEpochs)
        self.widthLineEdit.editingFinished.connect(self.__updateModelImageWidth)
        self.heightLineEdit.editingFinished.connect(self.__updateModelImageHeight)
        self.workersLineEdit.editingFinished.connect(self.__updateModelWorkers)
        self.deviceComboBox.currentTextChanged.connect(lambda text: self.__updateModelDevice(text))
        self.modelTypeComboBox.currentTextChanged.connect(lambda text: self.__updateModelModelType(text))

    def __updateModelBatchSize(self) -> None:
        """ Updates batchsize member on a model object """
        if not self.model or self.loading:
            return
        self.model.batchSize = self.batchsizeLineEdit.text()

    def __updateModelEpochs(self) -> None:
        """ Updates epochs member on a model object """
        if not self.model or self.loading:
            return
        self.model.epochs = self.epochsLineEdit.text()

    def __updateModelImageWidth(self) -> None:
        """ Updates image width member on a model object """
        if not self.model or self.loading:
            return
        self.model.dimensions[0] = self.widthLineEdit.text()

    def __updateModelImageHeight(self) -> None:
        """ Updates image height member on a model object """
        if not self.model or self.loading:
            return
        self.model.dimensions[1] = self.heightLineEdit.text()

    def __updateModelWorkers(self) -> None:
        """ Updates workers member on a model object """
        if not self.model or self.loading:
            return
        self.model.workers = self.workersLineEdit.text()

    def __updateModelModelType(self, modelType) -> None:
        """ Updates model type member on a model object """
        if not self.model or self.loading:
            return
        self.model.modelType = modelType

    def __updateModelDevice(self, device) -> None:
        """ Updates device member on a model object """
        if not self.model or self.loading:
            return
        self.model.device = device

    def __setEditMode(self, toggled):
        """ Connects the edit button to editable widgets """ 
        self.deviceComboBox.setDisabled(toggled)
        self.modelTypeComboBox.setDisabled(toggled)
        self.batchsizeLineEdit.setReadOnly(toggled)
        self.epochsLineEdit.setReadOnly(toggled)
        self.widthLineEdit.setReadOnly(toggled)
        self.heightLineEdit.setReadOnly(toggled)
        self.workersLineEdit.setReadOnly(toggled)

    def __openNewModelDialog(self) -> None:
        """ Creates a new model """
        self.createModelDialog = CreateModelDialog(self.app.theme.colours, self.app.fontTypeRegular, self.app.fontTypeHeader)
        self.createModelDialog.exec()

        #TODO: Some validity of a model must be checked, i.e. that a name of a model doesnt already exist

        if self.createModelDialog.result() == 1:
            model = Model(self.createModelDialog.modelName)
            # Update internally tracked model dataset
            self.app.project.modelDataset.append(model)
 
            # Reload page with model
            self.loadPage(model)

    def __resetPage(self) -> None:
        """ Resets page back to init state """
        # Reset user input fields
        self.batchsizeLineEdit.setText("")
        self.deviceComboBox.clear()
        self.epochsLineEdit.setText("")
        self.widthLineEdit.setText("")
        self.heightLineEdit.setText("")
        self.modelTypeComboBox.clear()
        self.workersLineEdit.setText("")
        self.ui.MLRightStackWidget.setCurrentIndex(0)
        # TODO: Reset stacked widgets

    def loadPage(self, model) -> None:
        """ Loads all information and functionality """
        self.loading = True
        if model:
            # When loading a new model, reset fields
            self.__resetPage()
            self.model = model
        
        if (not model) and (not self.model) :
            # Attempt to load an existing model
            self.__resetPage()
            if len(self.app.project.modelDataset) > 1:
                # Load last model in the list as this corresponds to the combobox
                self.model = self.app.project.modelDataset[0]

        # If no model loaded, reset page
        if not self.model:
            self.__resetPage()

        self.__populateAttributesPanel(self.model)
        self.__populateFields(self.model)
        self.loading = False

    def __populateFields(self, model) -> None:
        """ Populates fields from an existing model """
        self.__updateModelComboBox()
        self.__updateModelTypeComboBox()
        self.__updateDeviceComboBox()
        if model:
            self.stateInfoLabel.setText(model.state.value)
            self.batchsizeLineEdit.setText(model.batchSize)
            self.epochsLineEdit.setText(model.epochs)
            self.widthLineEdit.setText(str(model.dimensions[0]))
            self.heightLineEdit.setText(str(model.dimensions[1]))
            self.workersLineEdit.setText(model.workers)
            self.modelTypeComboBox.setCurrentText(model.modelType)
            self.deviceComboBox.setCurrentText(model.device)
 
    def __populateAttributesPanel(self, model) -> None:
        """ Populates the attributes panel"""
        annotatedImagesCount = 0  # Probably should do this better - but a TODO
        for image in self.app.project.annotationDataset:
            if image.annotated:
                annotatedImagesCount = annotatedImagesCount + 1
        self.imagesAnnoInfoLabel.setText(str(annotatedImagesCount))

    def __updateModelComboBox(self) -> None:
        """ Updates the model combobox """
        self.modelNameComboBox.clear()
        for model in self.app.project.modelDataset:
            self.modelNameComboBox.addItem(model.modelName)
        
        if self.model:
           self.modelNameComboBox.setCurrentText(self.model.modelName)
 
    def __updateDeviceComboBox(self) -> None:
        """ Updates the model combobox """
        self.deviceComboBox.clear()
        
        availableDevices = ["CPU"]  # CPU is always available
        # check available devices
        if torch.cuda.is_available():
            availableDevices.append(torch.device("cuda"))

        for device in availableDevices:
            self.deviceComboBox.addItem(device)

    def __updateModelTypeComboBox(self) -> None:
        """ Updates the model combobox """
        self.modelTypeComboBox.clear()

        availableModelTypes = ["YoloV7"]  #TODO: just leaving this hardcoded for the moment

        for modelType in availableModelTypes:
            self.modelTypeComboBox.addItem(modelType)

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
        self.ui.createModelBtn.setStyleSheet("QPushButton{"
                                             f"background-color: {self.app.theme.colours['buttonFilled.background']};"
                                             f"border : 1px solid {self.app.theme.colours['buttonFilled.background']};"
                                             "border-radius: 5px;"
                                             f"font: 75 bold 12pt {self.app.fontTypeTitle};}}"
                                             "QPushButton::hover{"
                                             f"background-color: {self.app.theme.colours['buttonFilled.hover']};"
                                             f"border : 1px solid {self.app.theme.colours['buttonFilled.hover']};}}")

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

        self.epochsLineEdit = CustomUserInputQLineEdit(self.app.theme.colours, self.app.fontTypeRegular)
        self.epochsLayout = QHBoxLayout()
        self.epochsLayout.addWidget(self.epochsLineEdit)
        self.epochsLayout.setContentsMargins(0,0,0,0)
        self.ui.epochsInputFrame.setLayout(self.epochsLayout)
        self.epochsLineEdit.editingFinished.connect(lambda: self.epochsLineEdit.clearFocus())

        self.batchsizeLineEdit = CustomUserInputQLineEdit(self.app.theme.colours, self.app.fontTypeRegular)
        self.batchsizeLayout = QHBoxLayout()
        self.batchsizeLayout.addWidget(self.batchsizeLineEdit)
        self.batchsizeLayout.setContentsMargins(0,0,0,0)
        self.ui.batchsizeInputFrame.setLayout(self.batchsizeLayout)
        self.batchsizeLineEdit.editingFinished.connect(lambda: self.batchsizeLineEdit.clearFocus())

        self.workersLineEdit = CustomUserInputQLineEdit(self.app.theme.colours, self.app.fontTypeRegular)
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
