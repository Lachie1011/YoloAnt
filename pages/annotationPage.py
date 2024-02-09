"""
    annotationPage.py
"""

import sys
from enum import Enum

from PyQt6 import QtCore
from PyQt6.QtGui import QCursor, QIcon
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QLabel, QVBoxLayout

from yoloAnt_ui import Ui_MainWindow
from events.hoverEvent import HoverEvent
from events.resizeEvent import ResizeEvent
from utils.switch import Switch
from customWidgets.customQObjects import CustomClassQListWidget
from customWidgets.annoPageListWidgetItem import AnnoPageListWidgetItem
from assets.darkThemePalette import DarkThemePalette

class Tools(Enum):
    """ Enum to represent the annotation tools within the page"""
    mouseTool=0
    annotationTool=1


class AnnotationPage():
    """
        Class to set up the functionality for the annotation page
    """
    def __init__(self, app) -> None:
        # TODO: fix up app type to yoloant app involes add futyure annotations and some if typing
        self.app = app
        self.ui = app.ui
        self.__setupStyleSheet()
        self.__setupPagePalette()

        # Connecting signals and slots for the page
        self.__connectIconHover()
        self.__connectAnnotationToolButtons()


        self.__createClassSelectionList()

        annoPageListWidgetItem = AnnoPageListWidgetItem("Dog", (0, 201, 52)) 
        annoPageListWidgetItem2 = AnnoPageListWidgetItem("Cat", (0, 90, 255)) 
        annoPageListWidgetItem3 = AnnoPageListWidgetItem("Aeroplane", (255, 2, 60)) 
        annoPageListWidgetItem4 = AnnoPageListWidgetItem("Person-on-bicycle", (223, 100, 120)) 
        annoPageListWidgetItem5 = AnnoPageListWidgetItem("Can", (223, 100, 120)) 
        self.classSelectionListWidget.addItemToListWidget(annoPageListWidgetItem)
        self.classSelectionListWidget.addItemToListWidget(annoPageListWidgetItem2)
        self.classSelectionListWidget.addItemToListWidget(annoPageListWidgetItem3)
        self.classSelectionListWidget.addItemToListWidget(annoPageListWidgetItem4)
        self.classSelectionListWidget.addItemToListWidget(annoPageListWidgetItem5)

        # Connect signals and slots
        self.editSwitchBtn.toggled.connect(lambda toggled: self.__editableMode(toggled))
        self.ui.classSearchLineEdit.textChanged.connect(lambda newText: self.__searchForClass(newText))
        # Applying resize event for the image lbl TODO: revisit for image resizing
        # self.imageFrameResizeEvent = ResizeEvent(self.ui.imageFrame)
        # self.ui.imageFrame.installEventFilter(self.imageFrameResizeEvent)    

    def __setupPagePalette(self) -> None:
        self.ui.annotationToolsFrame.setStyleSheet(self.ui.annotationToolsFrame.styleSheet() + 
                                                   f'background: {DarkThemePalette.panelColour.value};')
        self.ui.classInfoFrame.setStyleSheet(self.ui.classInfoFrame.styleSheet() + 
                                             f'background: {DarkThemePalette.panelColour.value};')
        self.ui.imageFrame.setStyleSheet(self.ui.imageFrame.styleSheet() +
                                         f'background: {DarkThemePalette.backgroundSunkenColour.value};')                                             
        self.ui.imageInfoFrame.setStyleSheet(self.ui.imageInfoFrame.styleSheet() +
                                             f'background: {DarkThemePalette.panelColour.value};')  
        self.ui.classSelectAnnoPageFrame.setStyleSheet(self.ui.classSelectAnnoPageFrame.styleSheet() +
                                                       f'background: {DarkThemePalette.panelSunkenColour.value};')    
    def __setupStyleSheet(self) -> None:
        
        # Setting up edit switch
        self.editSwtichLbl = QLabel('Edit')
        self.editSwtichLbl.setStyleSheet("QLabel{"
                                          "color: rgb(255, 255, 255);}")
        self.editSwtichLbl.setFixedHeight(18)

        self.ui.classAddAnnoPageBtn.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.ui.classAddAnnoPageBtn.setStyleSheet("QPushButton{"
                                                  "background-color: #505050;"
                                                  "border-radius: 12px;"
                                                  "border: 1px solid #606060;}"
                                                  "QPushButton::hover{"
                                                  "background-color : rgb(105, 105, 105);"
                                                  "color: rgb(255, 255, 255);}")

        self.editSwitchBtn = Switch()

        self.editSwitchLayout = QHBoxLayout()
        self.editSwitchLayout.addWidget(self.editSwtichLbl)
        self.editSwitchLayout.addWidget(self.editSwitchBtn)
        self.editSwitchLayout.setContentsMargins(5,5,0,7)
        self.ui.editSwitchFrame.setLayout(self.editSwitchLayout)

        # Move text margins of LineEdit
        self.ui.classSearchLineEdit.editingFinished.connect(lambda: self.ui.classSearchLineEdit.clearFocus())
        self.ui.classSearchLineEdit.setTextMargins(5,0,5,0)

        # Status combobox style
        self.ui.statusComboBox.setStyleSheet("QComboBox{"
                                             "background-color: rgb(45, 45, 45);}"
                                             "QComboBox::drop-down:button{"
                                             "background-color: rgb(45, 45, 45);"
                                             "border-radius: 5px}"
                                             "QComboBox::drop-down{"
                                             "color: rgb(45, 45, 45);}"
                                             "QComboBox::down-arrow{"
                                             "image: url(icons/icons8-drop-down-arrow-10.png)}")



    def __createClassSelectionList(self) -> None:
        """ Creates the class list """
        self.classSelectionListWidget = CustomClassQListWidget()
        self.classSelectionListWidget.setObjectName("annoPageClassListWidget")
        self.classSelectionListWidget.setSpacing(3)
        self.classSelectionListLayout = QVBoxLayout()
        self.classSelectionListLayout.addWidget(self.classSelectionListWidget)
        self.classSelectionListLayout.setContentsMargins(3,3,3,3)
        self.ui.classSelectAnnoPageFrame.setLayout(self.classSelectionListLayout)

    def __connectIconHover(self) -> None:
        """ 
            Installs the hover event filter onto the image navigation buttons
            and the annotation tool buttons.
        """
        
        # Applying hover events and cursor change to Navigation Buttons
        self.ui.prevUnannoImageBtn.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.prevUnannoBtnHoverEvent = HoverEvent(self.ui.prevUnannoImageBtn, "icons/icons8-chevron-prev-30.png", "icons/icons8-chevron-prev-30-selected.png")
        self.ui.prevUnannoImageBtn.installEventFilter(self.prevUnannoBtnHoverEvent)

        self.ui.prevImageBtn.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.prevBtnHoverEvent = HoverEvent(self.ui.prevImageBtn, "icons/icons8-chevron-left-30.png", "icons/icons8-chevron-left-30-selected.png")
        self.ui.prevImageBtn.installEventFilter(self.prevBtnHoverEvent)

        self.ui.nextImageBtn.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.nextBtnHoverEvent = HoverEvent(self.ui.nextImageBtn, "icons/icons8-chevron-right-30.png", "icons/icons8-chevron-right-30-selected.png")
        self.ui.nextImageBtn.installEventFilter(self.nextBtnHoverEvent)

        self.ui.nextUnannoImageBtn.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.nextUnannoBtnHoverEvent = HoverEvent(self.ui.nextUnannoImageBtn, "icons/icons8-chevron-next-30.png", "icons/icons8-chevron--next-30-selected.png")
        self.ui.nextUnannoImageBtn.installEventFilter(self.nextUnannoBtnHoverEvent)
      
        # Applying hover events and cursor change to Tool Selection Buttons 
        self.ui.mouseToolBtn.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.mouseBtnHoverEvent = HoverEvent(self.ui.mouseToolBtn, "icons/cursor-inactive.png", "icons/cursor-active.png")
        self.ui.mouseToolBtn.installEventFilter(self.mouseBtnHoverEvent)

        self.ui.annotateToolBtn.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.annotateBtnHoverEvent = HoverEvent(self.ui.annotateToolBtn, "icons/bounding-inactive.png", "icons/bounding-active.png")
        self.ui.annotateToolBtn.installEventFilter(self.annotateBtnHoverEvent)
    
    def __connectAnnotationToolButtons(self) -> None:
        """ Connects the annotation buttons to update the mouse icon as well as checked state """
        self.ui.mouseToolBtn.clicked.connect(lambda: self.__connectAnnotationToolSelected(Tools.mouseTool))
        self.ui.annotateToolBtn.clicked.connect(lambda: self.__connectAnnotationToolSelected(Tools.annotationTool))

    def __connectAnnotationToolSelected(self, tool: Tools) -> None:
        """ Updates the mouse icon based on selected tool """
        if tool is Tools.mouseTool:
            # updating checked state
            self.ui.annotateToolBtn.setChecked(False)
            self.ui.annotateToolBtn.setIcon(QIcon("icons/bounding-inactive.png"))
            # update mouse icon
            # QApplication.setOverrideCursor(QtCore.Qt.CursorShape.ArrowCursor)
            QApplication.restoreOverrideCursor()

        if tool is Tools.annotationTool:
            # updating checked state
            self.ui.mouseToolBtn.setChecked(False)
            self.ui.mouseToolBtn.setIcon(QIcon("icons/cursor-inactive.png"))
            # update mouse icon
            QApplication.setOverrideCursor(QtCore.Qt.CursorShape.CrossCursor)

    def __editableMode(self, toggled: bool) -> None:
        """ Sets the class selection list widget into editable mode """
        for listItemIndex in range(0,self.classSelectionListWidget.count()):
            listItem = self.classSelectionListWidget.item(listItemIndex)
            widgetInItem = self.classSelectionListWidget.itemWidget(listItem)

            if toggled:
                widgetInItem.enableEdit()
            
            else:
                widgetInItem.disableEdit()

    def __searchForClass(self, newText: str) -> None:
        """ Searches and shows the classes that correspond to text """
        for listItemIndex in range(0,self.classSelectionListWidget.count()):
            listItem = self.classSelectionListWidget.item(listItemIndex)
            widgetInItem = self.classSelectionListWidget.itemWidget(listItem)
        
            if not newText:
                listItem.setHidden(False)

            elif newText.lower() not in widgetInItem.className.lower():
                listItem.setHidden(True)