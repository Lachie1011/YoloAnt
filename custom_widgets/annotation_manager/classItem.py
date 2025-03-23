"""
    classItem.py
"""
from PyQt6.QtCore import Qt, pyqtSignal as Signal
from PyQt6.QtGui import QColor 
from PyQt6.QtWidgets import (QFrame, QHBoxLayout, QToolButton, QVBoxLayout)
                        
from custom_widgets.customBaseObjects.customWidgetItemQFrame import CustomWidgetItemQFrame
from custom_widgets.customBaseObjects.customClassQListWidget import CustomClassQListWidget

from dialogs.keySelectionDialog import getKeyInput
from dialogs.colourSelectorDialog import getColour
from utils.expandingFrame import ExpandingFrame

from custom_widgets.annotation_manager.classAttributesFrame import ClassAttributesFrame
from custom_widgets.annotation_manager.annotationItem import AnnotationItem

class ClassItem (QFrame):
    """
        Class that creates a custom class item widget for class list.
    """
    # Annotation signals
    annotation_selected = Signal(str)
    annotation_removed = Signal(str)
    annotation_hidden = Signal(str, bool)

    def __init__(self, className: str, colour: tuple, themePaletteColours: dict, fontRegular: str, fontTitle: str, app, parent=None):
        super().__init__()

        # Member variables
        self.colour = colour
        self.className = className
        self.themePaletteColours = themePaletteColours
        self.fontRegular = fontRegular
        self.fontTitle = fontTitle
        self.app = app
        self.parentItem = None
        self.parentSelected = False
        self.editEnabled = False

        self.annotations = []

        # Setup stylesheet of widget
        self.__setupStyleSheet()

        # Initialise widget with class attributes
        self.classAttributesFrame.setClassColour(self.colour)
        self.classAttributesFrame.setClassNameText(self.className)
        self.classAttributesFrame.setHotKeyText('a')
        self.classAttributesFrame.setClassAnnotationsCount('0')
        
        # Connect signals and slots
        self.classAttributesFrame.classHotKeyBtn.clicked.connect(lambda: self.setHotKey())
        self.classAttributesFrame.classColourBtn.clicked.connect(lambda: self.selectColour())
        self.classAttributesFrame.classNameLineEdit.editingFinished.connect(lambda: self.setClassName(self.classAttributesFrame.classNameLineEdit.text()))
        self.classAttributesFrame.classDeleteBtn.clicked.connect(lambda: self.parent().parent().removeItemFromListWidget(self.parentItem))

        self.expandBtn.clicked.connect(lambda checked: self.__expandFrame(checked))

    def addAnnotationToClassItem(self, annotationName: str) -> None:
        """ Adds an annotation item to the annotations list widget of class list item """
        annotationItem = AnnotationItem(annotationName, self.themePaletteColours)
        annotationItem.selected.connect(lambda id: self.annotation_selected.emit(id))
        annotationItem.removed.connect(lambda id: self.annotation_removed.emit(id))
        annotationItem.removed.connect(lambda id: self.handleDeleteButton(id))
        annotationItem.hidden.connect(lambda id, hidden: self.annotation_hidden.emit(id, hidden))

        # Add item to list
        self.annotationsListWidget.addItemToListWidget(annotationItem)
        self.annotations.append(annotationName)

        # Update size to accomodate new annotation
        self.__expandFrame(self.expandBtn.isChecked())

        # Show button as there is now an annotation
        self.expandBtn.show()

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
        self.app.ui.annotationCanvas.currentClassColour = QColor(int(self.colour[0]), int(self.colour[1]), int(self.colour[2]))
        self.app.ui.annotationCanvas.currentClassName = self.className

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

    def handleDeleteButton(self, id) -> None:
        """ Handles annotation item deletion """
        print("HERE")
        self.annotations.remove(id)
        if len(self.annotations) == 0:
            self.expandBtn.hide()
            self.expandBtn.setChecked(False)

        self.__expandFrame(self.expandBtn.isChecked())

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
        self.expandBtn.hide()  # Only show button when there are anntotaions

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
        self.classAnnotationsFrame = QFrame() # ExpandingFrame(self.annotationsFrameLayout)
        self.classAnnotationsFrame.setLayout(self.annotationsFrameLayout)

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
        if checked and len(self.annotations) > 0:
            print("a")
            self.expandBtn.setStyleSheet("QToolButton{"
                                         "border-image: url('icons/icons8-expand-arrow-down-25.png');"
                                         "background-color: transparent;}"
                                         "QToolButton:hover{"
                                         "border-image: url('icons/icons8-expand-arrow-down-hover-25.png');}")
            self.classAnnotationsFrame.setFixedHeight(self.annotationsFrameLayout.sizeHint().height())
            self.setFixedHeight(self.height() + self.annotationsFrameLayout.sizeHint().height())
            print("Class item is: " + str(self.height()))
            print("Annotations frame is " + str(self.classAnnotationsFrame.height()))

        if not checked and len(self.annotations) > 0:
            print("b")
            self.expandBtn.setStyleSheet("QToolButton{"
                                         "border-image: url('icons/icons8-expand-arrow-left-25.png');"
                                         "background-color: transparent;}"
                                         "QToolButton:hover{"
                                         "border-image: url('icons/icons8-expand-arrow-left-hover-25.png');}")
            self.classAnnotationsFrame.setFixedHeight(0)
            self.setFixedHeight(60)
            print("Class item is: " + str(self.height()))
            print("Annotations frame is " + str(self.classAnnotationsFrame.height()))

        if not checked and len(self.annotations) == 0:
            self.expandBtn.setStyleSheet("QToolButton{"
                                         "border-image: url('icons/icons8-expand-arrow-left-25.png');"
                                         "background-color: transparent;}"
                                         "QToolButton:hover{"
                                         "border-image: url('icons/icons8-expand-arrow-left-hover-25.png');}")
            self.classAnnotationsFrame.setFixedHeight(0)
            self.setFixedHeight(self.height())

        if self.parentItem:
            self.parentItem.setSizeHint(self.sizeHint())

