"""
    annotationPage.py
"""

import sys
from enum import Enum

from PyQt6 import QtCore
from PyQt6.QtGui import QCursor, QIcon, QColor
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QLabel, QVBoxLayout, QPushButton, QFrame, QGraphicsDropShadowEffect

from yoloAnt_ui import Ui_MainWindow
from events.hoverEvent import HoverEvent
from events.resizeEvent import ResizeEvent
from utils.switch import Switch
from customWidgets.customQObjects import CustomClassQListWidget, UserInputQLineEdit
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
        self.__setupPagePalette()

        # Connecting signals and slots for the page
        self.__connectIconHover()
        self.__connectAnnotationToolButtons()


        self.__createClassSelectionList()

        annoPageListWidgetItem = AnnoPageListWidgetItem("Dog", (0, 201, 52), self.app.theme.colours, self.app.fontTypeRegular, self.app.fontTypeTitle) 
        annoPageListWidgetItem2 = AnnoPageListWidgetItem("Cat", (0, 90, 255), self.app.theme.colours, self.app.fontTypeRegular, self.app.fontTypeTitle) 
        annoPageListWidgetItem3 = AnnoPageListWidgetItem("Aeroplane", (255, 2, 60), self.app.theme.colours, self.app.fontTypeRegular, self.app.fontTypeTitle) 
        annoPageListWidgetItem4 = AnnoPageListWidgetItem("Person-on-bicycle", (223, 100, 120), self.app.theme.colours, self.app.fontTypeRegular, self.app.fontTypeTitle) 
        annoPageListWidgetItem5 = AnnoPageListWidgetItem("Can", (223, 100, 120), self.app.theme.colours, self.app.fontTypeRegular, self.app.fontTypeTitle) 
        self.classSelectionListWidget.addItemToListWidget(annoPageListWidgetItem)
        self.classSelectionListWidget.addItemToListWidget(annoPageListWidgetItem2)
        self.classSelectionListWidget.addItemToListWidget(annoPageListWidgetItem3)
        self.classSelectionListWidget.addItemToListWidget(annoPageListWidgetItem4)
        self.classSelectionListWidget.addItemToListWidget(annoPageListWidgetItem5)

        # Connect signals and slots
        self.editSwitchBtn.toggled.connect(lambda toggled: self.classSelectionListWidget.enabledListEditMode(toggled))
        self.classSearchLineEdit.textChanged.connect(lambda newText: self.__searchForClass(newText))
        # Applying resize event for the image lbl TODO: revisit for image resizing
        # self.imageFrameResizeEvent = ResizeEvent(self.ui.imageFrame)
        # self.ui.imageFrame.installEventFilter(self.imageFrameResizeEvent)    

    def __setupPagePalette(self) -> None:
        """ Sets the colour palette for the page widgets """  
        self.ui.imageFrame.setStyleSheet(self.ui.imageFrame.styleSheet() +
                                         f"background: {self.app.theme.colours['app.sunken']};")   

        dropshadowEffect1 = QGraphicsDropShadowEffect()
        dropshadowEffect1.setBlurRadius(20)
        color = QColor(self.app.theme.colours['app.dropshadow'])
        dropshadowEffect1.setColor(color)
        dropshadowEffect1.setOffset(0,0)
        self.ui.classSelectionFrame.setGraphicsEffect(dropshadowEffect1)
        self.ui.classSelectionFrame.setStyleSheet(self.ui.classSelectionFrame.styleSheet() + 
                                             f"background: {self.app.theme.colours['panel.background']};")   

        dropshadowEffect = QGraphicsDropShadowEffect()
        dropshadowEffect.setBlurRadius(20)
        color = QColor(self.app.theme.colours['app.dropshadow'])
        dropshadowEffect.setColor(color)
        dropshadowEffect.setOffset(0,0)      
        self.ui.imageInfoFrame.setGraphicsEffect(dropshadowEffect)
        self.ui.imageInfoFrame.setStyleSheet(self.ui.imageInfoFrame.styleSheet() +
                                             f"background: {self.app.theme.colours['panel.background']};")  
        self.ui.annotationToolsFrame.setStyleSheet(self.ui.annotationToolsFrame.styleSheet() + 
                                                   f"background: {self.app.theme.colours['panel.background']};")
        self.ui.classSelectAnnoPageFrame.setStyleSheet(self.ui.classSelectAnnoPageFrame.styleSheet() +
                                                       f"background: {self.app.theme.colours['panel.sunken']};")    
    def __setupStyleSheet(self) -> None:
        """ Sets the style sheet for the page """
        # Place holder text for class search 
        self.classSearchLineEdit = UserInputQLineEdit(self.app.theme.colours, self.app.fontTypeRegular)
        self.classSearchLineEdit.setPlaceholderText('Search class...')
        # self.classSearchLineEdit.setFixedHeight(25)
        self.classSearchLineEdit.setMinimumSize(0, 25)
        self.classSearchLineEdit.setMaximumSize(170, 25)
        self.classSearchLineEdit.editingFinished.connect(lambda: self.classSearchLineEdit.clearFocus())
        self.classSearchLineEdit.setTextMargins(5,0,5,0)

        # Create class button
        self.classAddAnnoPageBtn = QPushButton()
        self.classAddAnnoPageBtn.setStyleSheet("QPushButton{"
                                               f"background-color: {self.app.theme.colours['buttonFilled.background']};"
                                               "border-radius: 12px;}"
                                               "QPushButton::hover{"
                                               f"background-color : {self.app.theme.colours['buttonFilled.hover']};"
                                               f"color: {self.app.theme.colours['font.regular']};}}")
        self.classAddAnnoPageBtn.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.classAddAnnoPageBtn.setText('+')
        self.classAddAnnoPageBtn.setFixedHeight(25)
        self.classAddAnnoPageBtn.setFixedWidth(25)

        self.classSearchAddFrameLayout = QHBoxLayout()
        self.classSearchAddFrameLayout.addWidget(self.classSearchLineEdit)
        self.classSearchAddFrameLayout.addWidget(self.classAddAnnoPageBtn)
        self.classSearchAddFrameLayout.setContentsMargins(0,0,0,0)
        self.classSearchAddFrame = QFrame()
        self.classSearchAddFrame.setLayout(self.classSearchAddFrameLayout)

        # Setting up edit switch
        self.editSwtichLbl = QLabel('Edit')
        self.editSwtichLbl.setStyleSheet("QLabel{"
                                         f"font: 75 12pt {self.app.fontTypeTitle};"
                                         f"color: {self.app.theme.colours['font.regular']};}}")
        self.editSwtichLbl.setFixedHeight(18)

        self.editSwitchBtn = Switch()

        self.editSwitchLayout = QHBoxLayout()
        self.editSwitchLayout.addWidget(self.editSwtichLbl)
        self.editSwitchLayout.addWidget(self.editSwitchBtn)
        self.editSwitchLayout.setContentsMargins(5,5,0,5)
        self.editSwitchFrame = QFrame()
        self.editSwitchFrame.setLayout(self.editSwitchLayout)

        self.classHeaderLayout = QHBoxLayout()
        self.classHeaderLayout.addWidget(self.classSearchAddFrame)
        self.classHeaderLayout.addWidget(self.editSwitchFrame)
        self.classHeaderLayout.setContentsMargins(0,0,0,0)
        self.classHeaderLayout.setSpacing(5)
        self.ui.classHeaderAnnoPageFrame.setLayout(self.classHeaderLayout)

        # Status combobox style
        self.ui.statusComboBox.setStyleSheet("QComboBox{"
                                             f"font: 75 12pt {self.app.fontTypeRegular};"
                                             f"background-color: {self.app.theme.colours['panel.sunken']};}}"
                                             "QComboBox::drop-down:button{"
                                             f"background-color: {self.app.theme.colours['panel.sunken']};"
                                             "border-radius: 5px}"
                                             "QComboBox::drop-down{"
                                             f"color: {self.app.theme.colours['panel.sunken']};}}"
                                             "QComboBox::down-arrow{"
                                             "image: url(icons/icons8-drop-down-arrow-10.png)}")

    def __createClassSelectionList(self) -> None:
        """ Creates the class list """
        self.classSelectionListWidget = CustomClassQListWidget(self.app.theme.colours)
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

    def __searchForClass(self, newText: str) -> None:
        """ Searches and shows the classes that correspond to text """
        for listItemIndex in range(0,self.classSelectionListWidget.count()):
            listItem = self.classSelectionListWidget.item(listItemIndex)
            widgetInItem = self.classSelectionListWidget.itemWidget(listItem)
        
            if not newText:
                listItem.setHidden(False)

            elif newText.lower() not in widgetInItem.className.lower():
                listItem.setHidden(True)