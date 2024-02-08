"""
    classListItemWidget.py
"""
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor 
from PyQt6.QtWidgets import (QFrame, QLabel, QHBoxLayout, QLineEdit, QProgressBar, 
                             QSpacerItem, QSizePolicy, QPushButton)

from customWidgets.customQObjects import *
from dialogs.colourSelectorDialog import getColour

class ProjectClassListItemWidget (CustomWidgetItemQFrame):
    """
        Class that creates a custom class item widget for class list

        params:
            className - Name of class
            numClassAnnotations  - Number of annotataions in dataset of this class type
            numOfAnnotations - Number of classes in the dataset 
            colour - Annotation colour of class in RGB format: (_,_,_) 
    """
    def __init__(self, className: str, numClassAnnotations: int, numOfAnnotations: int, colour: tuple, parent=None):
        """ init """

        # Member variables
        self.colour = colour
        self.className = className
        self.numOfAnnotations = numOfAnnotations
        self.numClassAnnotations = numClassAnnotations

        self.parentItem = None
        self.parentSelected = False
        self.r, self.g, self.b = self.colour
        super().__init__(self.parentSelected, (105,105,105), (65, 66, 64))

        # Setup stylesheet
        self.__setupStyleSheet()

        # Connect signals and slots
        self.classColourButton.clicked.connect(lambda: self.selectColour())
        self.classDeleteButton.clicked.connect(lambda: self.parent().parent().removeItemFromListWidget(self.parentItem))

    def __setupStyleSheet(self) -> None:
        """ Sets up style sheet of item widget """
        # Colour picker label
        self.classColourLbl = QLabel()
        self.classColourLbl.setStyleSheet("QLabel{"
                                          f"background-color: rgb({self.r}, {self.g}, {self.b});"
                                          "border-radius: 4px;"
                                          "border: 3px solid rgb(105, 105, 105)}")
        self.classColourLbl.setFixedWidth(18)
        self.classColourLbl.setFixedHeight(18)

        # Colour picker button
        self.classColourButton = QPushButton()
        self.classColourButton.setStyleSheet("QPushButton{"
                                             f"background-color: rgb({self.r}, {self.g}, {self.b});"
                                             "border-radius: 4px;"
                                             "border: 3px solid rgb(105, 105, 105)}"
                                             "QPushButton:hover{border-color: rgb(165, 165, 165)}"
                                             )
        self.classColourButton.setFixedWidth(18)
        self.classColourButton.setFixedHeight(18)
        self.classColourButton.setVisible(False)
        self.classColourButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Class name label
        self.classItemLbl = QLabel(self.className)
        self.classItemLbl.setStyleSheet("QLabel{font: 14pt 'Gotham Rounded Light';}")
        self.classItemLbl.setMinimumSize(100, 30)
        self.classItemLbl.setMaximumSize(300, 30)
        self.classItemLbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # Class name line edit, not visible by default
        self.classItemLineEdit = CustomQLineEdit()

        # self.classItemLineEdit = QLineEdit()
        self.classItemLineEdit.editingFinished.connect(lambda: self.setClassName(self.classItemLineEdit.text()))
        self.classItemLineEdit.setStyleSheet("QLineEdit{"
                                             "font: 14pt 'Gotham Rounded Light';}"
                                             "QLineEdit:hover{"
                                             "background-color: rgb(105, 105, 105);}")
        self.classItemLineEdit.setText(self.className)
        self.classItemLineEdit.setMinimumSize(100, 30)
        self.classItemLineEdit.setMaximumSize(300, 30)
        self.classItemLineEdit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.classItemLineEdit.setVisible(False)

        # Numer of annotations for class
        self.numClassItemLbl = QLabel(str(self.numClassAnnotations))
        self.numClassItemLbl.setStyleSheet("QLabel{font: 14pt 'Gotham Rounded Light';}")
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
                                             "background-color: rgb(232, 93, 84);}"
                                             "QPushButton:hover{background-color: rgb(255, 43, 28)}")
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
        self.classItemWidetLayout.addWidget(self.classColourLbl)
        self.classItemWidetLayout.addWidget(self.classColourButton)
        self.classItemWidetLayout.addItem(self.classColourhorizontalSpacer)
        self.classItemWidetLayout.addWidget(self.classItemLbl)
        self.classItemWidetLayout.addWidget(self.classItemLineEdit)
        self.classItemWidetLayout.addWidget(self.numClassItemLbl)
        self.classItemWidetLayout.addWidget(self.classNumBar)
        self.classItemWidetLayout.addWidget(self.classDeleteLbl)
        self.classItemWidetLayout.addWidget(self.classDeleteButton)

        self.setLayout(self.classItemWidetLayout)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    def enableEdit(self) -> None:
        """ Sets the item widget to edit mode """
        self.parentSelected = True
        self.setStyleSheet(self.styleSheet() + "background: rgb(85, 87, 83);")
        self.classItemLbl.setVisible(False)
        self.classItemLineEdit.setVisible(True)
        self.classColourLbl.setVisible(False)
        self.classColourButton.setVisible(True)
        self.classDeleteLbl.setVisible(False)
        self.classDeleteButton.setVisible(True)
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        
    def disableEdit(self) -> None:
        """ Disables edit mode of item widget """
        self.parentSelected = False
        self.setStyleSheet(self.styleSheet() + "background: rgb(65, 66, 64);")
        self.classItemLbl.setVisible(True)
        self.classItemLineEdit.setVisible(False)
        self.classColourLbl.setVisible(True)
        self.classColourButton.setVisible(False)
        self.classDeleteLbl.setVisible(True)
        self.classDeleteButton.setVisible(False)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    def setClassName(self, text: str) -> None:
        """ Sets the name of the class from user input """
        self.className = text
        self.classItemLbl.setText(text)
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
        self.colour = getColour(self.colour)
        self.r, self.g, self.b = self.colour

        self.classColourLbl.setStyleSheet("QLabel{"
                                          f"background-color: rgb({self.r}, {self.g}, {self.b});"
                                          "border-radius: 4px;"
                                          "border: 3px solid rgb(105, 105, 105)}")

        self.classColourButton.setStyleSheet("QPushButton{"
                                             f"background-color: rgb({self.r}, {self.g}, {self.b});"
                                             "border-radius: 4px;"
                                             "border: 3px solid rgb(105, 105, 105)}"
                                             "QPushButton:hover{border-color: rgb(165, 165, 165)}")
        self.classColourLbl.repaint()
        self.classColourButton.repaint()