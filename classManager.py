"""
    classManager.py
    A class that manages the creation of classes and class viewing list
"""

from PyQt6 import QtCore, QtWidgets
from PyQt6 import QtGui
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QListWidgetItem, QLineEdit, QProgressBar, QSpacerItem, QSizePolicy, QPushButton

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

        self.ui.classListWidget.setStyleSheet("QListView::item:hover {border: 5px solid;"
                                              "border-color:  rgb(85, 87, 83);"
                                              "}"
                                              "QListWidget::item:selected{"
                                              "background: rgb(85, 87, 83);}")

class ClassListItem (QWidget):
    """
        Class that creates a custom class item widget for class list
    """
    def __init__(self, className, numClass, numOfClasses, colour, parent=None):
        super(ClassListItem, self).__init__(parent)

        # Class name label
        self.classItemLbl = QLabel(className)
        self.classItemLbl.setStyleSheet("QLabel{font: 14pt 'Gotham Rounded Light';" 
                                        "border-radius: 10px;"
                                        "border: 2px solid rgb(65, 66, 64);}")
        self.classItemLbl.setMinimumSize(100, 30)
        self.classItemLbl.setMaximumSize(300, 30)
        self.classItemLbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # Class name line edit, not visible by default
        self.classItemLineEdit = QLineEdit()
        self.classItemLineEdit.setStyleSheet("QLineEdit{font: 14pt 'Gotham Rounded Light';"  
                                             "background-color: rgb(105, 105, 105);"
                                             "border-radius: 10px;"
                                             "border: 2px solid rgb(85, 87, 83)}")
        self.classItemLineEdit.setText(className)
        self.classItemLineEdit.setMinimumSize(100, 30)
        self.classItemLineEdit.setMaximumSize(300, 30)
        self.classItemLineEdit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.classItemLineEdit.setVisible(False)

        # Colour picker label
        self.classColourLbl = QLabel()
        self.classColourLbl.setStyleSheet("QLabel{"
                                        "background-color: rgb(0, 201, 0);"
                                        "border-radius: 4px;"
                                        "border: 2px solid rgb(105, 105, 105)"
                                        "}")
        self.classColourLbl.setFixedWidth(16)
        self.classColourLbl.setFixedHeight(16)

        # Colour picker button
        self.classColourButton = QPushButton()
        self.classColourButton.setStyleSheet("QPushButton{"
                                        "background-color: rgb(0, 201, 0);"
                                        "border-radius: 4px;"
                                        "border: 2px solid rgb(105, 105, 105)"
                                        "}")
        self.classColourButton.setFixedWidth(16)
        self.classColourButton.setFixedHeight(16)
        self.classColourButton.setVisible(False)

        # Numer of annotations for class
        self.numClassItemLbl = QLabel(str(numClass))
        self.numClassItemLbl.setStyleSheet("QLabel{font: 14pt 'Gotham Rounded Light';}")
        self.numClassItemLbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.numClassItemLbl.setMinimumSize(100, 20)
        self.numClassItemLbl.setMaximumSize(200, 20)
        self.numClassItemLbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # Horizontal spacers
        self.classColourhorizontalSpacer = QSpacerItem(15, 5, QSizePolicy.Policy.Fixed)
        self.deleteBtnSpacer = QSpacerItem(20, 5, QSizePolicy.Policy.Fixed)

        # Class imbalance bar
        self.classNumBar = QProgressBar()
        self.classNumBar.setMinimum(0)
        self.classNumBar.setMaximum(numOfClasses)
        self.classNumBar.setValue(numClass)
        self.classNumBar.setTextVisible(False)
        self.classNumBar.setFixedHeight(15)
        self.classNumBar.setStyleSheet("QProgressBar::chunk{"
                                       "background-color: rgb(0, 201, 0);"
                                       "border-radius: 3px;"
                                       "}"
                                       "QProgressBar"
                                       "{background: rgb(105, 105, 105);"
                                       "border-radius: 3px;"
                                       "}")

        
        # Setting layout of custom widget 
        self.classItemWidetLayout = QHBoxLayout()
        self.classItemWidetLayout.addWidget(self.classColourLbl)
        self.classItemWidetLayout.addWidget(self.classColourButton)
        self.classItemWidetLayout.addItem(self.classColourhorizontalSpacer)
        self.classItemWidetLayout.addWidget(self.classItemLbl)
        self.classItemWidetLayout.addWidget(self.classItemLineEdit)
        self.classItemWidetLayout.addWidget(self.numClassItemLbl)
        self.classItemWidetLayout.addWidget(self.classNumBar)
        self.classItemWidetLayout.addItem(self.deleteBtnSpacer)

        self.setLayout(self.classItemWidetLayout)