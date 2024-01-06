"""
    classManager.py
    A class that manages the creation of classes and class viewing list
"""

from PyQt6 import QtCore, QtWidgets
from PyQt6 import QtGui
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QListWidgetItem, QProgressBar, QSpacerItem, QSizePolicy, QPushButton

class ClassManager:

    def __init__(self, app):
        """ init """
        self.app = app
        self.ui = app.ui


    def addClassToImbalanceList(self, className, numClass, numOfClasses, colour) -> None:
        """ Adds custom class item widget to class list on Project page""" 

        # Create class widget item   
        self.classListItem = ClassListItem(className, numClass, numOfClasses, colour) 

        # Add class widget item to list
        self.classListWidgetItem = QListWidgetItem(self.ui.classListWidget)
        self.classListWidgetItem.setSizeHint(self.classListItem.sizeHint())

        self.ui.classListWidget.addItem(self.classListWidgetItem)
        self.ui.classListWidget.setItemWidget(self.classListWidgetItem, self.classListItem)

        self.ui.classListWidget.setStyleSheet("QListView::item:hover {background-color: rgb(0,0,0);}")

class ClassListItem (QWidget):
    """
        Class that creates a custom class item widget for class list
    """
    def __init__(self, className, numClass, numOfClasses, colour, parent=None):
        super(ClassListItem, self).__init__(parent)

        # Class name label
        classItemLbl = QLabel(className)
        classItemLbl.setStyleSheet("QLabel{font: 14pt 'Gotham Rounded Light';}")
        classItemLbl.setMinimumSize(100, 20)
        classItemLbl.setMaximumSize(300, 20)
        classItemLbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # Colour picker button
        classColourButton = QPushButton()
        classColourButton.setStyleSheet("QPushButton{"
                                        "background-color: rgb(0, 201, 0);"
                                        "border-radius: 4px;"
                                        "border: 2px solid rgb(105, 105, 105)"
                                        "}")
        classColourButton.setFixedWidth(16)
        classColourButton.setFixedHeight(16)

        

        # Numer of annotations for class
        numClassItemLbl = QLabel(str(numClass))
        numClassItemLbl.setStyleSheet("QLabel{font: 14pt 'Gotham Rounded Light';}")
        numClassItemLbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        numClassItemLbl.setMinimumSize(100, 20)
        numClassItemLbl.setMaximumSize(200, 20)
        numClassItemLbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # Horizontal spacers
        classColourhorizontalSpacer = QSpacerItem(15, 5, QSizePolicy.Policy.Fixed)
        deleteBtnSpacer = QSpacerItem(20, 5, QSizePolicy.Policy.Fixed)

        # Class imbalance bar
        classNumBar = QProgressBar()
        classNumBar.setMinimum(0)
        classNumBar.setMaximum(numOfClasses)
        classNumBar.setValue(numClass)
        classNumBar.setTextVisible(False)
        classNumBar.setFixedHeight(15)

        classNumBar.setStyleSheet("QProgressBar::chunk{"
                                       "background-color: rgb(0, 201, 0);"
                                       "border-radius: 3px;"
                                       "}"
                                       "QProgressBar"
                                       "{background: rgb(105, 105, 105);"
                                       "border-radius: 3px;"
                                       "}")

        
        # Setting layout of custom widget 
        classItemWidetLayout = QHBoxLayout()
        classItemWidetLayout.addWidget(classColourButton)
        classItemWidetLayout.addItem(classColourhorizontalSpacer)
        classItemWidetLayout.addWidget(classItemLbl)
        classItemWidetLayout.addWidget(numClassItemLbl)
        classItemWidetLayout.addWidget(classNumBar)
        classItemWidetLayout.addItem(deleteBtnSpacer)

        self.setLayout(classItemWidetLayout)
