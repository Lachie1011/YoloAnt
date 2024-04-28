"""
    annotationClassSelectionWidget.py
"""

from PyQt6 import QtCore
from PyQt6.QtGui import QCursor, QIcon, QColor
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QLabel, QVBoxLayout, QPushButton, QFrame, QGraphicsDropShadowEffect, QSpacerItem, QSizePolicy

from customWidgets.customQObjects import CustomClassQListWidget, CustomUserInputQLineEdit
from customWidgets.classSelectionListWidgetItem import ClassSelectionListWidgetItem

class AnnotationClassSelectionWidget(QFrame):
    """ A custom widget for the annotation class selection for selecting and searching for classes """
    def __init__(self, ui, themePaletteColours: dict, fontRegular, fontTitle):
        super(AnnotationClassSelectionWidget, self).__init__()
        
        # Member variables
        self.ui = ui
        self.themePaletteColours = themePaletteColours
        self.fontRegular = fontRegular
        self.fontTitle = fontTitle

        # Setup stylesheet of frame
        self.__setupStyleSheet()

        # Test calls        
        # self.addClassSelectionListItem("Dog", (0, 201, 52))
        # self.addClassSelectionListItem("Cat", (0, 90, 255))
        
        # Connect signals and slots
        self.classSearchLineEdit.textChanged.connect(lambda searchInput: self.__searchForClass(searchInput))

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
        self.classAddAnnoPageBtn.setText('+ Add Class')
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

    def addClassSelectionListItem(self, className: str, classColour: tuple) -> None:
        """ Adds a class selection list item to the class selection list widget """
        self.classSelectionListWidget.addItemToListWidget(ClassSelectionListWidgetItem(className, classColour, 
                                                          self.themePaletteColours, self.fontRegular, self.fontTitle))
