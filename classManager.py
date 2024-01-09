"""
    classManager.py
    A class that manages the creation of classes and class viewing list
"""

from PyQt6 import QtCore, QtWidgets
from PyQt6 import QtGui
from PyQt6.QtGui import QFont, QCursor, QColor 
from PyQt6.QtWidgets import QAbstractItemView, QFrame, QWidget, QLabel, QHBoxLayout, QListWidgetItem, QLineEdit, QProgressBar, QSpacerItem, QSizePolicy, QPushButton, QListWidget, QAbstractScrollArea
from PyQt6.QtCore import QObject, QEvent, QPoint, Qt

class ClassListItemWidget (QFrame):
    """
        Class that creates a custom class item widget for class list
    """
    def __init__(self, className, numClass, numOfClasses, colour, parent=None):
        super(ClassListItemWidget, self).__init__(parent)

        # Class name label
        self.classItemLbl = QLabel(className)
        self.classItemLbl.setStyleSheet("QLabel{font: 14pt 'Gotham Rounded Light';}")
        self.classItemLbl.setMinimumSize(100, 30)
        self.classItemLbl.setMaximumSize(300, 30)
        self.classItemLbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # Class name line edit, not visible by default
        self.classItemLineEdit = QLineEdit()
        self.classItemLineEdit.setStyleSheet("QLineEdit{font: 14pt 'Gotham Rounded Light';"
                                             "background-color: rgb(105, 105, 105)}")
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
        self.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

    def hoverEnterEvent(self, event) -> None:
        print('yes')
        parent = self.parent().parent() 
        self.setStyleSheet("background: rgb(85, 87, 83);")
        self.numClassItemLbl.setStyleSheet(self.numClassItemLbl.styleSheet() + "background: rgb(85, 87, 83)")

    def leaveEvent(self, event) -> None:
        self.setStyleSheet("background: rgb(65, 66, 64);")
        self.numClassItemLbl.setStyleSheet(self.numClassItemLbl.styleSheet() + "background: rgb(85, 87, 83)")

class ClassListItem (QListWidgetItem):
    def __init__(self):
        super().__init__()

    def enterEvent(self, event) -> None:
        print('yes')

class ClassListItemEvent(QObject):
    """
        Class to detect a hover event and change the icon of a QObject
    """
    def __init__(self, object: QObject):
        super().__init__()
        self.object = object

class ClassListWidget (QListWidget):
    """
        Class that creates a custom list widget
    """
    def __init__(self):
        super().__init__()
        self.setMinimumSize(0, 0)
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setStyleSheet("QListView::item:hover {border: 5px solid;"
                           "border-color:  rgb(85, 87, 83);}")
        
        self.currentItemSelected = None
        self.itemClicked.connect(lambda: self.__selectItem())
        self.itemSelectionChanged.connect(lambda: self.__enabledEditMode())

    def mouseMoveEvent(object, event):
        # Disables selection with mouse click + drag
        event.ignore()    

    def __enabledEditMode(self):
        
        # Clear selections from list
        self.__clearSelections()

        # Change selected item to editable mode
        listItem = self.currentItem()
        listItem.setBackground(QtGui.QColor(85, 87, 83))
        widgetInItem = self.itemWidget(listItem)
        widgetInItem.setStyleSheet(widgetInItem.styleSheet() + "background: rgb(85, 87, 83);")
        widgetInItem.classItemLbl.setVisible(False)
        widgetInItem.classItemLineEdit.setVisible(True)

        # Save current selected item
        self.currentItemSelected = listItem

    def __selectItem(self) -> None:
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setCurrentItem(self.currentItem())
        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)

    def __clearSelections(self) -> None:

        if self.currentItemSelected:
            widgetInItem = self.itemWidget(self.currentItemSelected)
            self.currentItemSelected.setBackground(QtGui.QColor(65, 66, 64))
            widgetInItem.setStyleSheet(widgetInItem.styleSheet() + "background: rgb(65, 66, 64);")
            widgetInItem.classItemLbl.setVisible(True)
            widgetInItem.classItemLineEdit.setVisible(False)
        self.clearSelection()


    def addItemToListWidget(self, className, numClass, numOfClasses, colour) -> None:
        """ Adds item widget to list widget""" 

        # Create class widget item   
        classListWidget = ClassListItemWidget(className, numClass, numOfClasses, colour) 

        # Add class widget item to list
        classListWidgetItem = ClassListItem()
        self.classListItemEvent = ClassListItemEvent(classListWidgetItem)
        # classListWidgetItem.installEventFilter(self.classListItemEvent)

        # classListWidgetItem = QListWidgetItem(self)
        self.addItem(classListWidgetItem)
        classListWidgetItem.setSizeHint(classListWidget.sizeHint())

        self.addItem(classListWidgetItem)
        self.setItemWidget(classListWidgetItem, classListWidget)
