"""
    classListItemWidget.py
"""
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor, QFont
from PyQt6.QtWidgets import (QFrame, QLabel, QHBoxLayout, QLineEdit, QProgressBar, 
                             QSpacerItem, QSizePolicy, QPushButton)

from customWidgets.customQObjects import *
from dialogs.colourSelectorDialog import getColour

class ProjectClassListItemWidget (QFrame):
    """
        Class that creates a custom class item widget for class list

        params:
            className - Name of class
            numClassAnnotations  - Number of annotataions in dataset of this class type
            numOfAnnotations - Number of classes in the dataset 
            colour - Annotation colour of class in RGB format: (_,_,_) 
    """
    def __init__(self, className: str, numClassAnnotations: int, numOfAnnotations: int, colour: tuple, themePaletteColours: dict, fontRegular: str, 
                 fontTitle, parent=None):
        """ init """
        super().__init__()

        # Member variables
        self.fontRegular = fontRegular
        self.fontTitle = fontTitle
        self.colour = colour
        self.className = className
        self.numOfAnnotations = numOfAnnotations
        self.numClassAnnotations = numClassAnnotations
        self.themePaletteColours = themePaletteColours

        self.editEnabled = False
        self.parentItem = None
        self.parentSelected = False

        # Setup stylesheet
        self.__setupStyleSheet()

        # Connect signals and slots
        self.classColourButton.clicked.connect(lambda: self.selectColour())
        self.classDeleteButton.clicked.connect(lambda: self.parent().parent().removeItemFromListWidget(self.parentItem))

    def __setupStyleSheet(self) -> None:
        """ Sets up style sheet of item widget """

        # Colour picker button
        self.classColourButton = QPushButton()
        self.classColourButton.setStyleSheet("QPushButton{"
                                             f"background-color: rgb{self.colour};"
                                             "border-radius: 4px;}")
        self.classColourButton.setFixedWidth(18)
        self.classColourButton.setFixedHeight(18)

        # Class name line edit
        self.classItemLineEdit = PanelQLineEdit(self.themePaletteColours, f"font: 75 12pt {self.fontRegular};")
        self.classItemLineEdit.editingFinished.connect(lambda: self.setClassName(self.classItemLineEdit.text()))
        self.classItemLineEdit.setText(self.className)
        self.classItemLineEdit.setMinimumSize(100, 30)
        self.classItemLineEdit.setMaximumSize(300, 30)
        self.classItemLineEdit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # Numer of annotations for class
        self.numClassItemLbl = QLabel(str(self.numClassAnnotations))
        self.numClassItemLbl.setStyleSheet("QLabel{"
                                           f"color: {self.themePaletteColours['font.regular']};"
                                           f"font: 12pt {self.fontRegular};}}")
        self.numClassItemLbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.numClassItemLbl.setMinimumSize(100, 20)
        self.numClassItemLbl.setMaximumSize(200, 20)
        self.numClassItemLbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # Horizontal spacers
        self.padSpacer = QSpacerItem(5, 5, QSizePolicy.Policy.Fixed)
        self.classColourhorizontalSpacer = QSpacerItem(38, 5, QSizePolicy.Policy.Fixed)
        

        # Delete Label placeholder picker label
        self.classDeleteLbl = QLabel()
        self.classDeleteLbl.setStyleSheet("QLabel{"
                                          "background-color: transparent;}")
        self.classDeleteLbl.setFixedWidth(15)
        self.classDeleteLbl.setFixedHeight(15)

        # Delete button
        self.classDeleteButton = QPushButton()
        self.classDeleteButton.setStyleSheet("QPushButton{"
                                             f"background-color: {self.themePaletteColours['cancelButton.background']};}}"
                                             "QPushButton:hover{"
                                             f"background-color: {self.themePaletteColours['buttonFilled.hover']}}}")
        self.classDeleteButton.setFixedWidth(15)
        self.classDeleteButton.setFixedHeight(15)
        self.classDeleteButton.setVisible(False)
        self.classDeleteButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Class imbalance bar
        self.classNumBar = QProgressBar()
        self.classNumBar.setMinimum(0)
        self.classNumBar.setMaximum(self.numOfAnnotations)
        self.classNumBar.setValue(self.numClassAnnotations)
        self.classNumBar.setTextVisible(False)
        self.classNumBar.setFixedHeight(15)
        self.classNumBar.setStyleSheet("QProgressBar::chunk{"
                                       f"background-color: rgb({self.warningColour()});"
                                       "border-radius: 3px;}"
                                       "QProgressBar{"
                                       "background: rgb(105, 105, 105);"
                                       "border-radius: 3px;}")
        
        # Setting layout of custom widget 
        self.classItemWidetLayout = QHBoxLayout()
        self.classItemWidetLayout.addItem(self.padSpacer)
        self.classItemWidetLayout.addWidget(self.classColourButton)
        self.classItemWidetLayout.addItem(self.classColourhorizontalSpacer)
        self.classItemWidetLayout.addWidget(self.classItemLineEdit)
        self.classItemWidetLayout.addWidget(self.numClassItemLbl)
        self.classItemWidetLayout.addWidget(self.classNumBar)
        self.classItemWidetLayout.addWidget(self.classDeleteLbl)
        self.classItemWidetLayout.addWidget(self.classDeleteButton)

        self.setLayout(self.classItemWidetLayout)

    def enableEdit(self) -> None:
        """ Sets the item widget to edit mode """
        self.parentSelected = True
        self.editEnabled = True
        self.setStyleSheet(self.styleSheet() + f"background: {self.themePaletteColours['listItem.edit']};")
        self.classItemLineEdit.setEditMode(True)

        self.classColourButton.setStyleSheet("QPushButton{"
                                             f"background-color: rgb{self.colour};"
                                             "border-radius: 4px;"
                                             f"border: 3px solid {self.themePaletteColours['listItemButton.background']}}}"
                                             f"QPushButton:hover{{border-color: {self.themePaletteColours['listItemButton.hover']}}}")
        self.classColourButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.classDeleteLbl.setVisible(False)
        self.classDeleteButton.setVisible(True)
        
    def disableEdit(self) -> None:
        """ Disables edit mode of item widget """
        self.parentSelected = False
        self.setStyleSheet(self.styleSheet() + f"background: {self.themePaletteColours['panel.background']};")
        self.classColourButton.setStyleSheet("QPushButton{"
                                             f"background-color: rgb{self.colour};"
                                             "border-radius: 4px;"
                                             f"border: 1px solid {self.themePaletteColours['listItemButton.background']}}}")
        self.classColourButton.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.classItemLineEdit.setEditMode(False)
        self.classDeleteLbl.setVisible(True)
        self.classDeleteButton.setVisible(False)

    def setClassName(self, text: str) -> None:
        """ Sets the name of the class from user input """
        self.className = text
        self.classItemLineEdit.setText(text)

        if self.classItemLineEdit.hasFocus():
            self.classItemLineEdit.clearFocus()

    def warningColour(self) -> str:
        """ Determins the warning colour to be displayed on the progress bar """
        if self.numClassAnnotations < round(self.numOfAnnotations/3):
            return "255, 0, 0"

        if self.numClassAnnotations > round(self.numOfAnnotations*3/4):
            return "242, 186, 2"
        
        else:
            return "0, 201, 0"

    def selectColour(self) -> None:
        """ Gets a selected colour from the user """
        if self.editEnabled:
            self.colour = getColour(self.themePaletteColours, self.fontRegular, self.fontTitle, self.colour)
            self.classColourButton.setStyleSheet("QPushButton{"
                                                f"background-color: rgb{self.colour};"
                                                "border-radius: 4px;"
                                                f"border: 3px solid {self.themePaletteColours['listItemButton.background']}}}"
                                                f"QPushButton:hover{{border-color: {self.themePaletteColours['listItemButton.hover']}}}")
            self.classColourButton.repaint()