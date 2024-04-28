"""
    machineLearningPage.py
"""

import pyqtgraph as pg

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

        # Initially set up machine learning page with readonly set to True
        self.__setEditMode(self.readOnly)

        # Connecting signals and slots
        self.ui.editPageBtn.toggled.connect(lambda toggled: self.__setEditMode(not toggled)) 

        # for now just load the page at start TODO: this will have to change based on selected model
        self.load_page()
    
    def __setEditMode(self, toggled):
        """ Connects the edit button to editable widgets """ 
        self.ui.batchLineEdit.setReadOnly(toggled)
        self.ui.deviceLineEdit.setReadOnly(toggled)
        self.ui.epochLineEdit.setReadOnly(toggled)
        self.ui.imageSizeLineEdit.setReadOnly(toggled)
        self.ui.modelTypeLineEdit.setReadOnly(toggled)
        self.ui.modelNameLineEdit.setReadOnly(toggled)
        self.ui.workersLineEdit.setReadOnly(toggled)

    def load_page(self) -> None:
        """ Loads all information and functionality """
        self.__createPlots()

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

