"""
    annotationPage.py
"""

import sys
from enum import Enum
from typing import Any

from PyQt6 import QtCore
from PyQt6.QtGui import QCursor, QIcon, QColor
from PyQt6.QtWidgets import QApplication, QGraphicsDropShadowEffect

from yoloAnt_ui import Ui_MainWindow

from mlClass import MLClass
from image import Image
from events.hoverEvent import HoverEvent
from events.resizeEvent import ResizeEvent
from dialogs.createClassDialog import CreateClassDialog
from customWidgets.annotationClassSelectionWidget import AnnotationClassSelectionWidget

class NavigationModes(Enum):
    """ 
        Enum to represent different canvas navigation modes 
    """
    next=0
    previous=1
    nextUnannotated=2
    previousUnannotated=3


class Tools(Enum):
    """ 
        Enum to represent the annotation tools within the page
    """
    mouseTool=0
    annotationTool=1


class AnnotationPage():
    """
        Class to set up the functionality for the annotation page
    """
    def __init__(self, app) -> None:
        # TODO: fix up app type to yoloant app involes add future annotations and some if typing
        self.app = app
        self.ui = app.ui

        self.ui.annotationCanvasWidget.app = app

        self.__setupStyleSheet()
        self.__setupPagePalette()

        # Page attributes:
        self.currentIndex = 0
        self.pageInitialised = False
        
        # Dict to hold the unannotatedImages TODO: probs could be made into some kind of Kd tree to make searching faster
        self.unannotatedImages = {}

        # Connecting signals and slots for the page
        self.__connectIconHover()
        self.__connectAnnotationToolButtons()
        self.__connectImageNavigationButtons()

        # Connect signals and slots
        self.annotationClassSelectionWidget.classAddAnnoPageBtn.clicked.connect(self.__openCreateClassDialog)
        self.ui.editPageBtn.toggled.connect(lambda toggled: self.annotationClassSelectionWidget.classSelectionListWidget.setEditMode(toggled))
        self.ui.annotationCanvasWidget.new_annotation.connect(lambda annotation: self.annotationClassSelectionWidget.generateAnnotationItem(annotation))

    def __connectImageNavigationButtons(self):
        """ Connects the buttons used to navigate throughout the canvas"""
        self.app.ui.nextImageBtn.clicked.connect(lambda: self.__navigateCanvasWidget(NavigationModes.next))
        self.app.ui.prevImageBtn.clicked.connect(lambda: self.__navigateCanvasWidget(NavigationModes.previous))
        self.app.ui.nextUnannoImageBtn.clicked.connect(lambda: self.__navigateCanvasWidget(NavigationModes.nextUnannotated))
        self.app.ui.prevUnannoImageBtn.clicked.connect(lambda: self.__navigateCanvasWidget(NavigationModes.previousUnannotated))

    def __connectAnnotationToolButtons(self) -> None:
        """ Connects the annotation buttons to update the mouse icon as well as checked state """
        self.ui.mouseToolBtn.clicked.connect(lambda: self.updateAnnotationToolSelected(Tools.mouseTool))
        self.ui.annotateToolBtn.clicked.connect(lambda: self.updateAnnotationToolSelected(Tools.annotationTool))

    def loadPage(self):
        """ Loads all information and functionality """ 
        if len(self.app.project.annotationDataset) < 0:
            self.app.notificationManager.raiseNotification("Dataset contains no images")
            return

        if not self.pageInitialised:
            # Creating metadata for inital image
            self.app.project.annotationDataset[self.currentIndex].createMetadata()
            self.pageInitialised = True

        # Updating widgets
        self.app.ui.annotationCanvasWidget.updateImage(self.app.project.annotationDataset[self.currentIndex])
        self.updateAnnotationToolSelected(Tools.mouseTool)
        self.__updateImageInformationPanel()
        self.__updateAnnotationClassSelectionWidget(self.app.project.annotationDataset[self.currentIndex]) 

    def updateAnnotationToolSelected(self, tool: Tools) -> None:
        """ Updates the mouse icon based on selected tool """
        if tool is Tools.mouseTool:
            # updating checked state
            self.ui.mouseToolBtn.setChecked(True)
            self.ui.mouseToolBtn.setIcon(QIcon("icons/cursor-active.png")) 
            self.ui.annotateToolBtn.setChecked(False)
            self.ui.annotateToolBtn.setIcon(QIcon("icons/bounding-inactive.png"))
            # update mouse icon
            QApplication.restoreOverrideCursor()

            # Updating annotationCanvasWidget mode
            self.ui.annotationCanvasWidget.mode = Tools.mouseTool

        if tool is Tools.annotationTool:
            if (len(self.app.project.classesDataset) == 0) or (self.ui.annotationCanvasWidget.currentClassName is None):
                # A class is required to perform annotations
                self.app.notificationManager.raiseNotification("Please add a class before annotating")
                self.updateAnnotationToolSelected(Tools.mouseTool)
                return

            # updating checked state
            self.ui.annotateToolBtn.setChecked(True)
            self.ui.annotateToolBtn.setIcon(QIcon("icons/bounding.active.png"))
            self.ui.mouseToolBtn.setChecked(False)
            self.ui.mouseToolBtn.setIcon(QIcon("icons/cursor-inactive.png"))
            # update mouse icon
            QApplication.setOverrideCursor(QtCore.Qt.CursorShape.CrossCursor)

            # Updating annotationCanvasWidget mode
            self.ui.annotationCanvasWidget.mode = Tools.annotationTool

    def __updateImageInformationPanel(self):
        """ Updates the image information panel with info from the latest image """
        image = self.app.project.annotationDataset[self.currentIndex]
        if not image.isValid:
            self.app.notificationManager.raiseNotification(f"Image {image.path} is not valid")
            return

        self.app.ui.imageName.setText(image.path.split("/")[-1])  # dont think we need the whole path ?
        self.app.ui.imageDimLbl.setText(f"{image.width}x{image.height}")
        self.app.ui.imageNumberLbl.setText(f"{self.currentIndex + 1} of {len(self.app.project.annotationDataset)}")
        self.app.ui.datasetProgressBar.setValue(self.currentIndex / len(self.app.project.annotationDataset) * 100)
        self.app.ui.datasetProgressBar.repaint()

        annotationStatusTxt = None
        annotationStatusColour = None
        if image.annotated:
            annotationStatusTxt = "annotated"
            annotationStatusColour = "background-color: rgb(115,210,22); border-radius: 3px;"
        elif not image.annotated:
            annotationStatusTxt = "unannotated"
            annotationStatusColour = "background-color: rgb(204,0,0); border-radius: 3px;"
        elif image.needsWork:  # no way to set this yet :( - TODO: revisit and makes these states an enum
            annotationStatusTxt = "needs work"
            annotationStatusColour = "background-color: rgb(245,121,22); border-radius: 3px;"
        
        if annotationStatusTxt:
            self.app.ui.annotationStatusLbl.setText(annotationStatusTxt)
            self.app.ui.statusColourIndicatorLbl.setStyleSheet(annotationStatusColour)

    def __updateAnnotationClassSelectionWidget(self, image: Any) -> None:
        """ Updates the annotation class selection widget"""
        self.annotationClassSelectionWidget.reset()
        self.annotationClassSelectionWidget.generateClassItems()
        self.annotationClassSelectionWidget.generateAnnotationItems(image)
    
    def __navigateCanvasWidget(self, navigationType):
        """ Logic for page navigation """
        #TODO: not the best place for this, but have to save the image somewhere else as well, i.e. not only when navigating :(
        #TODO: this logic assumes that a new image will be found only when moving next not previously
        self.__checkImageState(self.app.project.annotationDataset[self.currentIndex])
        if navigationType is NavigationModes.next:
            if (self.currentIndex + 1) < len(self.app.project.imageDataset):
                # Setup the next image
                nextImage = self.app.project.annotationDataset[self.currentIndex + 1]
                nextImage.createMetadata()
                if nextImage.isValid:
                    # go to next image
                    self.app.ui.annotationCanvasWidget.updateImage(nextImage)
                    self.currentIndex = self.currentIndex + 1
                else:
                    # TODO: If the image is not valid show blank image / skip ahead to the next valid image??
                    self.app.notificationManager.raiseNotification(f"Image: {0} is not valid", nextImage.path)
        if navigationType is NavigationModes.previous:
            if (self.currentIndex - 1) >= 0:
                self.app.ui.annotationCanvasWidget.updateImage(self.app.project.annotationDataset[self.currentIndex - 1])
                self.currentIndex = self.currentIndex - 1
        if navigationType is NavigationModes.nextUnannotated:
            closestIndex = None
            # Check cache first
            if self.unannotatedImages:
                for _, index in self.unannotatedImages.items():
                    if index > self.currentIndex:
                        if closestIndex is None:
                            closestIndex = index
                        if (index < closestIndex) and index != self.currentIndex:
                            closestIndex = index
                            
            # If we couldnt find anything in the cache, check annotation dataset 
            if closestIndex is None:
                for i in range(self.currentIndex + 1, len(self.app.project.annotationDataset) - 1):
                    if not self.app.project.annotationDataset[i].annotated:
                        closestIndex = i
                        break
            if closestIndex is not None:
                self.app.ui.annotationCanvasWidget.updateImage(self.app.project.annotationDataset[closestIndex])
                self.currentIndex = closestIndex 
        if navigationType is NavigationModes.previousUnannotated:
            closestIndex = None
            # check the cache first
            if self.unannotatedImages:
                for _, index in self.unannotatedImages.items():
                    if index < self.currentIndex:
                        if closestIndex is None:
                            closestIndex = index
                        if (index > closestIndex) and index != self.currentIndex:
                            closestIndex = index
            # if we couldnt find anything in the cache, check annotation dataset
            if closestIndex is None:
                for i in range(self.currentIndex - 1, len(self.app.project.annotationDataset), -1):
                    if not self.app.project.annotationDataset[i].annotated:
                        closestIndex = i
                        break
            if closestIndex is not None:
                self.app.ui.annotationCanvasWidget.updateImage(self.app.project.annotationDataset[closestIndex])
                self.currentIndex = closestIndex
        
        # after switching image - update widgets
        self.__updateImageInformationPanel()
        self.__updateAnnotationClassSelectionWidget(self.app.project.annotationDataset[self.currentIndex])

    def __checkImageState(self, image) -> None:
        """ Checks the current images state and updates related properties """
        # this removes the image from the unannotated list if it has been annotated
        if image.annotated and (image in self.unannotatedImages):
            self.unannotatedImages.pop(image)
        # adds image to unannotated list if not annotated
        if not image.annotated:
            self.unannotatedImages.update({self.app.project.annotationDataset[self.currentIndex]:self.currentIndex})
    
    def __openCreateClassDialog(self) -> None:
        """ Opens the create class dialog """
        self.createClassDialog = CreateClassDialog(self.app.theme.colours, self.app.fontTypeRegular, self.app.fontTypeHeader)
        self.createClassDialog.exec()
        if self.createClassDialog.isValid:
            _class = MLClass(self.createClassDialog.className, self.createClassDialog.selectedColour)
            self.app.project.classesDataset.append(_class) 
            self.annotationClassSelectionWidget.generateClassItem(_class.className, _class.classColour)

    def __setupPagePalette(self) -> None:
        """ Sets the colour palette for the page widgets """  
        self.ui.imageFrame.setStyleSheet(self.ui.imageFrame.styleSheet() +
                                         f"background: {self.app.theme.colours['app.sunken']};")   

        dropshadowEffect1 = QGraphicsDropShadowEffect()
        dropshadowEffect1.setBlurRadius(10)
        color = QColor(self.app.theme.colours['app.dropshadow'])
        dropshadowEffect1.setColor(color)
        dropshadowEffect1.setOffset(0,2)
        self.ui.classSelectionFrame.setGraphicsEffect(dropshadowEffect1)
        self.ui.classSelectionFrame.setStyleSheet(self.ui.classSelectionFrame.styleSheet() + 
                                             f"background: {self.app.theme.colours['panel.background']};")   

        dropshadowEffect2 = QGraphicsDropShadowEffect()
        dropshadowEffect2.setBlurRadius(10)
        color = QColor(self.app.theme.colours['app.dropshadow'])
        dropshadowEffect2.setColor(color)
        dropshadowEffect2.setOffset(0,2) 
        self.ui.imageInfoFrame.setGraphicsEffect(dropshadowEffect2)
        self.ui.imageInfoFrame.setStyleSheet(self.ui.imageInfoFrame.styleSheet() +
                                             f"background: {self.app.theme.colours['panel.background']};") 
        
        dropshadowEffect3 = QGraphicsDropShadowEffect()
        dropshadowEffect3.setBlurRadius(10)
        color = QColor(self.app.theme.colours['app.dropshadow'])
        dropshadowEffect3.setColor(color)
        dropshadowEffect3.setOffset(0,2)  
        self.ui.annotationToolsFrame.setGraphicsEffect(dropshadowEffect3)
        self.ui.annotationToolsFrame.setStyleSheet(self.ui.annotationToolsFrame.styleSheet() + 
                                                   f"background: {self.app.theme.colours['panel.background']};")
    def __setupStyleSheet(self) -> None:
        """ Sets the style sheet for the page """
        # Setup annotation class selection frame
        self.annotationClassSelectionWidget = AnnotationClassSelectionWidget(self.app, self.ui, self.app.theme.colours, self.app.fontTypeRegular, self.app.fontTypeTitle)

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

