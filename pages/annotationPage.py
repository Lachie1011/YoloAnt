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

        # Connecting signals and slots for the page
        self.__connectIconHover()
        self.__connectAnnotationToolButtons()

        self.__createClassSelectionList()

        annoPageListWidgetItem = AnnoPageListWidgetItem("Dog", (0, 201, 52)) 
        annoPageListWidgetItem2 = AnnoPageListWidgetItem("Cat", (0, 90, 255)) 
        annoPageListWidgetItem3 = AnnoPageListWidgetItem("Aeroplane", (255, 2, 60)) 
        annoPageListWidgetItem4 = AnnoPageListWidgetItem("Person-on-bicycle", (223, 100, 120)) 
        self.classSelectionListWidget.addItemToListWidget(annoPageListWidgetItem)
        self.classSelectionListWidget.addItemToListWidget(annoPageListWidgetItem2)
        self.classSelectionListWidget.addItemToListWidget(annoPageListWidgetItem3)
        self.classSelectionListWidget.addItemToListWidget(annoPageListWidgetItem4)

        # Connect signals and slots
        self.editSwitchBtn.toggled.connect(lambda toggled: self.__editableMode(toggled))

        # Applying resize event for the image lbl TODO: revisit for image resizing
        # self.imageFrameResizeEvent = ResizeEvent(self.ui.imageFrame)
        # self.ui.imageFrame.installEventFilter(self.imageFrameResizeEvent)    

    def __setupStyleSheet(self) -> None:
        
        # Setting up edit switch
        # Edit label
        self.editSwtichLbl = QLabel('Edit')
        self.editSwtichLbl.setStyleSheet("QLabel{"
                                          "color: rgb(255, 255, 255);}")
        self.editSwtichLbl.setFixedHeight(18)

        self.ui.classAddAnnoPageBtn.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.ui.classAddAnnoPageBtn.setStyleSheet("QPushButton{"
                                                  "background-color: rgb(85, 87, 83);"
                                                  "border-radius: 8px;}"
                                                  "QPushButton::hover{"
                                                  "background-color : rgb(105, 105, 105);"
                                                  "color: rgb(255, 255, 255);}")

        # Edit switch Btn
        self.editSwitchBtn = Switch()

        self.editSwitchLayout = QHBoxLayout()
        self.editSwitchLayout.addWidget(self.editSwtichLbl)
        self.editSwitchLayout.addWidget(self.editSwitchBtn)
        self.editSwitchLayout.setContentsMargins(5,5,0,7)
        self.ui.editSwitchFrame.setLayout(self.editSwitchLayout)

        # Move text margins of LineEdit
        self.ui.classSearchLineEdit.setTextMargins(5,0,5,0)

    def __createClassSelectionList(self) -> None:
        """ Creates the class list """

        self.classSelectionListWidget = CustomClassQListWidget()
        self.classSelectionListWidget.setSpacing(2)
        self.classSelectionListWidget.setObjectName("annotationClassListWidget")
        self.classSelectionListLayout = QVBoxLayout()
        self.classSelectionListLayout.addWidget(self.classSelectionListWidget)
        self.classSelectionListLayout.setContentsMargins(0,0,0,0)
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

        for listItemIndex in range(0,self.classSelectionListWidget.count()):
            listItem = self.classSelectionListWidget.item(listItemIndex)
            widgetInItem = self.classSelectionListWidget.itemWidget(listItem)

            if toggled:
                widgetInItem.enableEdit()
            
            else:
                widgetInItem.disableEdit()
