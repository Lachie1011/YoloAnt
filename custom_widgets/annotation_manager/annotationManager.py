"""
    annotationManager.py
"""

from typing import Any
from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSignal as Signal
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QFrame

from custom_widgets.customBaseObjects.customClassQListWidget import CustomClassQListWidget
from custom_widgets.customBaseObjects.customUserInputQLineEdit import CustomUserInputQLineEdit
from custom_widgets.annotation_manager.classItem import ClassItem

class AnnotationManager(QFrame):
    """ 
        A custom widget for the annotation class selection for selecting and searching for classes 
    """
    annotation_selected = Signal(str)
    annotation_removed = Signal(str)
    annotation_hidden = Signal(str, bool)

    def __init__(self, app, ui, themePaletteColours: dict, fontRegular, fontTitle):
        super(AnnotationManager, self).__init__()

        # Member variables
        self.app = app
        self.ui = ui
        self.themePaletteColours = themePaletteColours
        self.fontRegular = fontRegular
        self.fontTitle = fontTitle

        self._classes = []
        self.classListItems = []

        # Setup stylesheet of frame
        self.__setupStyleSheet()
 
        # Connect signals and slots
        self.classSearchLineEdit.textChanged.connect(lambda searchInput: self.__searchForClass(searchInput))
        self.ui.editPageBtn.toggled.connect(lambda toggled: self.classSelectionListWidget.setEditMode(toggled))

    def reset(self) -> None:
        """ Resets the widget to an empty state """
        self.classSelectionListWidget.clear()
        self._classes = []
        self.classListItems = []

    def generateClassItems(self) -> None:
        """ Generates the class items for the widget """
        for _class in self.app.project.classesDataset:
            if _class.className not in self._classes:
                self.generateClassItem(_class.className, _class.classColour)

    def generateClassItem(self, className: str, classColour: tuple ) -> None:
        """ Generates a class item """
        if className not in self._classes:
            self.addClassSelectionListItem(className, classColour)
            self._classes.append(className)

    def getClass(self, className: str) -> Any:
        """ Finds an ML Class """
        for _class in self.app.project.classesDataset:
            if _class.className == className:
                return _class

    def generateAnnotationItems(self, image: Any) -> None:
        """ Generates annotation items for an image"""
        for annotation in image.boundingBoxes:
            self.generateAnnotationItem(annotation)

    def generateAnnotationItem(self, annotation: Any) -> None:
        """ Generates an annotation item """
        # Finding the annotation's class
        if annotation.className not in self._classes:
            # An annotation is dependant on its class item being present
            _class = self.getClass(annotation.className)
            self.generateClassItem(_class.className, _class.classColour)

        self.addAnnotationToClassItem(annotation.className, annotation.id)

    def addClassSelectionListItem(self, className: str, classColour: tuple) -> None:
        """ Adds a class item to the class selection list widget """
        classListItem = ClassItem(className, classColour, self.themePaletteColours, self.fontRegular, self.fontTitle, app=self)
        classListItem.annotation_selected.connect(lambda annotation_id: self.annotation_selected.emit(annotation_id))
        classListItem.annotation_removed.connect(lambda annotation_id: self.annotation_removed.emit(annotation_id))
        classListItem.annotation_hidden.connect(lambda annotation_id, hidden: self.annotation_hidden.emit(annotation_id, hidden))

        self.classListItems.append(classListItem)
        self.classSelectionListWidget.addItemToListWidget(classListItem)

    def addAnnotationToClassItem(self, className: str, annotationID: str) -> None:
        """
        Adds an annotation item to a class item
        """
        for classListItem in self.classListItems:
            if classListItem.className == className:
                classListItem.addAnnotationToClassItem(str(annotationID))

    def __setupStyleSheet(self) -> None:
        """ Sets the style sheet for the custom widget """
        # Create utility frame 
        self.classSelectionUtilityFrame = QFrame()
        self.classSelectionUtilityFrame.setMinimumSize(0, 30)
        self.classSelectionUtilityFrame.setMaximumSize(16777215, 30)

        # Create class selection list frame
        self.classSelectionListFrame = QFrame()
        self.classSelectionListFrame.setStyleSheet("QFrame{"
                                                   f"background: {self.themePaletteColours['panel.sunken']};}}")   

        # Create search line edit widget
        self.classSearchLineEdit = CustomUserInputQLineEdit(self.themePaletteColours, self.fontRegular)
        self.classSearchLineEdit.setPlaceholderText('Search class...')
        self.classSearchLineEdit.setMinimumSize(0, 25)
        self.classSearchLineEdit.setMaximumSize(170, 25)
        self.classSearchLineEdit.editingFinished.connect(lambda: self.classSearchLineEdit.clearFocus())
        self.classSearchLineEdit.setTextMargins(5,0,5,0)

        # Create class add button widget
        self.classAddAnnoPageBtn = QPushButton()
        self.classAddAnnoPageBtn.setStyleSheet("QPushButton{"
                                               f"font: 75 bold 11pt {self.fontTitle};"
                                               f"background-color: {self.themePaletteColours['buttonFilled.background']};"
                                               "border-radius: 8px;}"
                                               "QPushButton::hover{"
                                               f"background-color : {self.themePaletteColours['buttonFilled.hover']};"
                                               f"color: {self.themePaletteColours['font.header']};}}")
        self.classAddAnnoPageBtn.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.classAddAnnoPageBtn.setText('+ Class')
        self.classAddAnnoPageBtn.setFixedHeight(25)

        # Apply layout to utility frame
        self.classSelectionUtilityLayout = QHBoxLayout()
        self.classSelectionUtilityLayout.addWidget(self.classSearchLineEdit)
        self.classSelectionUtilityLayout.addWidget(self.classAddAnnoPageBtn)
        self.classSelectionUtilityLayout.setContentsMargins(0,0,0,0)
        self.classSelectionUtilityLayout.setSpacing(15)
        self.classSelectionUtilityFrame.setLayout(self.classSelectionUtilityLayout)

        # Create custom class selection list widget        
        self.classSelectionListWidget = CustomClassQListWidget(self.themePaletteColours)
        self.classSelectionListWidget.setObjectName("annotationClassListWidget")
        self.classSelectionListWidget.setSpacing(3)

        # Apply layout to class selection list frame 
        self.classSelectionListLayout = QVBoxLayout()
        self.classSelectionListLayout.addWidget(self.classSelectionListWidget)
        self.classSelectionListLayout.setSpacing(5)
        self.classSelectionListLayout.setContentsMargins(3,3,3,3)
        self.classSelectionListFrame.setLayout(self.classSelectionListLayout)

        # Apply layout to 
        self.annotationClassSelectionLayout = QVBoxLayout()
        self.annotationClassSelectionLayout.addWidget(self.classSelectionUtilityFrame)
        self.annotationClassSelectionLayout.addWidget(self.classSelectionListFrame)
        self.annotationClassSelectionLayout.setSpacing(5)
        self.annotationClassSelectionLayout.setContentsMargins(0,0,0,0)
        self.ui.annotationClassSelectionFrame.setLayout(self.annotationClassSelectionLayout)

    def __searchForClass(self, searchInput: str) -> None:
        """ Searches and shows the classes that correspond to text """
        for listItemIndex in range(0,self.classSelectionListWidget.count()):
            listItem = self.classSelectionListWidget.item(listItemIndex)
            widgetInItem = self.classSelectionListWidget.itemWidget(listItem)
        
            if not searchInput:
                listItem.setHidden(False)

            elif searchInput.lower() not in widgetInItem.className.lower():
                listItem.setHidden(True)
