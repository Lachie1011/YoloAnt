"""
    classSelectionListWidgetItem.py
"""
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor 
from PyQt6.QtWidgets import (QFrame, QHBoxLayout, QToolButton, QVBoxLayout)
                        
from customWidgets.customQObjects import *
from customWidgets.classAttributesFrame import ClassAttributesFrame
from dialogs.keySelectionDialog import getKeyInput
from utils.expandingFrame import ExpandingFrame
from dialogs.colourSelectorDialog import getColour
from customWidgets.annotationsListWidgetItem import AnnotationsListWidgetItem

class ClassSelectionListWidgetItem (QFrame):
    """
        Class that creates a custom class item widget for class list.

        params:
            className - Name of class
            colour - Annotation colour of class in RGB format: _,_,_ 
    """
    def __init__(self, className: str, colour: tuple, themePaletteColours: dict, fontRegular: str, fontTitle: str, page, parent=None):
        super().__init__()

        # Member variables
        self.colour = colour
        self.className = className
        self.themePaletteColours = themePaletteColours
        self.fontRegular = fontRegular
        self.fontTitle = fontTitle
        self.page = page
        self.parentItem = None
        self.parentSelected = False
        self.editEnabled = False

        # Setup stylesheet of widget
        self.__setupStyleSheet()

        # Initialise widget with class attributes
        self.classAttributesFrame.setClassColour(self.colour)
        self.classAttributesFrame.setClassNameText(self.className)
        self.classAttributesFrame.setHotKeyText('a')
        self.classAttributesFrame.setClassAnnotationsCount('0')

        # Test calls
        self.addAnnotationToClassItem("Dog 1")
        
        # Connect signals and slots
        self.classAttributesFrame.classHotKeyBtn.clicked.connect(lambda: self.setHotKey())
        self.classAttributesFrame.classColourBtn.clicked.connect(lambda: self.selectColour())
        self.classAttributesFrame.classNameLineEdit.editingFinished.connect(lambda: self.setClassName(self.classAttributesFrame.classNameLineEdit.text()))
        self.classAttributesFrame.classDeleteBtn.clicked.connect(lambda: self.parent().parent().removeItemFromListWidget(self.parentItem))
        self.expandBtn.clicked.connect(lambda checked: self.__expandFrame(checked))

    def __setupStyleSheet(self) -> None:
        """ Sets up style sheet for list widget item"""

        # Class attributes frame
        self.classAttributesFrame = ClassAttributesFrame(self.themePaletteColours, self.fontRegular)

        # Expand annotations frame button
        self.expandBtn = QToolButton()
        self.expandBtn.setStyleSheet("QToolButton{"
                                     "border-image: url('icons/icons8-expand-arrow-left-25.png');"
                                     "background-color: transparent;}"
                                     "QToolButton:hover{"
                                     "border-image: url('icons/icons8-expand-arrow-left-hover-25.png');}")
        self.expandBtn.setFixedWidth(15)
        self.expandBtn.setFixedHeight(15)
        self.expandBtn.setCheckable(True)
        self.expandBtn.setChecked(False)

        # Setup class selection frame
        self.classSelectionFrame = CustomWidgetItemQFrame(self.themePaletteColours, self.parentSelected)

        self.classSelectionFrameLayout = QHBoxLayout()
        self.classSelectionFrameLayout.addWidget(self.classAttributesFrame)
        self.classSelectionFrameLayout.addWidget(self.expandBtn)
        self.classSelectionFrameLayout.setContentsMargins(0,0,5,0)
        self.classSelectionFrameLayout.setSpacing(5)
        self.classSelectionFrame.setLayout(self.classSelectionFrameLayout)

        # Class annotations frame
        self.annotationsListWidget = CustomClassQListWidget(self.themePaletteColours)

        # Create layout for annotations frame
        self.annotationsFrameLayout = QVBoxLayout()
        self.annotationsFrameLayout.addWidget(self.annotationsListWidget)
        self.annotationsFrameLayout.setContentsMargins(0,0,0,0)
        self.classAnnotationsFrame = ExpandingFrame(self.annotationsFrameLayout)

        # Apply contents to widget item
        self.annotationPageListWidgetItemLayout = QVBoxLayout()
        self.annotationPageListWidgetItemLayout.addWidget(self.classSelectionFrame)
        self.annotationPageListWidgetItemLayout.addWidget(self.classAnnotationsFrame)
        self.annotationPageListWidgetItemLayout.setContentsMargins(0,0,0,0)
        self.annotationPageListWidgetItemLayout.setSpacing(0)
        self.annotationPageListWidgetItemLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.annotationPageListWidgetItemLayout)

    def __expandFrame(self, checked) -> None:
        """ Expands and shrinks the annotations frame when expand arrow is toggled """
        self.classAnnotationsFrame.start_animation(checked)

        if checked: 
            self.expandBtn.setStyleSheet("QToolButton{"
                                         "border-image: url('icons/icons8-expand-arrow-down-25.png');"
                                         "background-color: transparent;}"
                                         "QToolButton:hover{"
                                         "border-image: url('icons/icons8-expand-arrow-down-hover-25.png');}")
            self.classAnnotationsFrame.setFixedHeight(self.annotationsFrameLayout.sizeHint().height())
            self.setFixedHeight(self.height() + self.annotationsFrameLayout.sizeHint().height())

        else: 
            self.expandBtn.setStyleSheet("QToolButton{"
                                         "border-image: url('icons/icons8-expand-arrow-left-25.png');"
                                         "background-color: transparent;}"
                                         "QToolButton:hover{"
                                         "border-image: url('icons/icons8-expand-arrow-left-hover-25.png');}")
            self.classAnnotationsFrame.setFixedHeight(0)
            self.setFixedHeight(self.height() - self.annotationsFrameLayout.sizeHint().height())

        if self.parentItem:
            self.parentItem.setSizeHint(self.sizeHint())

    def enableEdit(self) -> None:
        """ Sets the list widget item into edit mode """
        self.classSelectionFrame.setEditMode(True)
        self.classAttributesFrame.setEditMode(True)
        
    def disableEdit(self) -> None:
        """ Disables edit mode of list widget item """
        self.classSelectionFrame.setEditMode(False)
        self.classAttributesFrame.setEditMode(False)

    def setSelected(self) -> None:
        """ Sets list widget item to selected state """
        self.classSelectionFrame.setSelected()
        self.classSelectionFrame.parentSelected = True
        self.parentSelected = True

        # If we select an item, update the canvas
        self.page.ui.annotationCanvasWidget.currentClassColour = QColor(self.colour[0], self.colour[1], self.colour[2])
        self.page.ui.annotationCanvasWidget.currentClassName = self.className

    def clearSelected(self) -> None:
        """ Clears selected state of list widget item """
        self.classSelectionFrame.clearSelection()
        self.classSelectionFrame.parentSelected = False
        self.parentSelected = False

    def setClassName(self, className: str) -> None:
        """ Sets the name of the class """
        self.className = className
        self.classAttributesFrame.setClassNameText(className)
        if self.classAttributesFrame.classNameLineEdit.hasFocus():
            self.classAttributesFrame.classNameLineEdit.clearFocus()

    def setHotKey(self) -> None:
        """ Gets a hotkey input from the user and sets the hotkey for the class """
        keyInput = getKeyInput()
        self.classAttributesFrame.setHotKeyText(keyInput.lower())

    def selectColour(self) -> None:
        """ Gets a selected colour from the user sets it as the class colour """
        self.colour = getColour(self.themePaletteColours, self.fontRegular, self.fontTitle, self.colour)
        self.classAttributesFrame.setClassColour(self.colour)

    def addAnnotationToClassItem(self, annotationName: str) -> None:
        """ Adds an annotation item to the annotations list widget of class list item """
        self.annotationsListWidget.addItemToListWidget(AnnotationsListWidgetItem(annotationName, self.themePaletteColours))
