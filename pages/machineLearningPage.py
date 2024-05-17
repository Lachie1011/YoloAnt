"""
    machineLearningPage.py
"""

import pyqtgraph as pg

from model import Model
from dialogs.createModelDialog import CreateModelDialog
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

        self.__setupStyleSheet()

        # Initially set up machine learning page with readonly set to True
        self.__setEditMode(self.readOnly)

        # Connecting signals and slots
        self.ui.editPageBtn.toggled.connect(lambda toggled: self.__setEditMode(not toggled)) 
        self.ui.createModelBtn.clicked.connect(self.__openNewModelDialog)
  
    def __setEditMode(self, toggled):
        """ Connects the edit button to editable widgets """ 
        self.ui.batchLineEdit.setReadOnly(toggled)
        self.ui.deviceLineEdit.setReadOnly(toggled)
        self.ui.epochLineEdit.setReadOnly(toggled)
        self.ui.imageSizeLineEdit.setReadOnly(toggled)
        self.ui.modelTypeLineEdit.setReadOnly(toggled)
        self.ui.modelNameLineEdit.setReadOnly(toggled)
        self.ui.workersLineEdit.setReadOnly(toggled)

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

