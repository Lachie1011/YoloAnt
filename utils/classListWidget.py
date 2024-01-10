"""
    classListWidget.py
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QAbstractItemView, QListWidgetItem, QSizePolicy, QListWidget, QAbstractScrollArea)
from utils.classListItemWidget import ClassListItemWidget 

class ClassListWidget (QListWidget):
    """
        Class that creates a custom list widget
    """
    def __init__(self):
        super().__init__()

        # Setup list widget
        self.setMinimumSize(0, 0)
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        
        self.setStyleSheet("QScrollBar:vertical{"
                           "border: none;"
                           "width: 10px;"
                           "margin: 15px 0 15px 0;"
                           "border-radius: 0px;}"
                           "QScrollBar::handle:vertical{"
                           "background-color: rgb(80,80,80);"
                           "min-height:30px;"
                           "border-radius: 4px;}"
                           "QScrollBar::handle:vertical:pressed{"	
	                       "background-color: rgb(185, 0, 92);}"
                           "QScrollBar::sub-line:vertical{"
                           "border: none;"
                           "background: none;"
                           "color: none;}"
                           "QScrollBar::add-line:vertical{"
                           "border: none;"
                           "background: none;"
                           "color: none;}")               

        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Store selected item in list
        self.itemSelected = None

        # Connect signals and slots
        self.itemClicked.connect(lambda item: self.__selectItem(item))
        self.itemSelectionChanged.connect(lambda: self.__enabledWidgetEditMode())

    def mouseMoveEvent(object, event):
        # Disables selection with mouse click + drag
        event.ignore()    

    def __selectItem(self, item: QListWidgetItem) -> None:
        """ Set the chosen item to selected """
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setCurrentItem(item)
        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)

    def __clearSelection(self) -> None:
        """ clears the list of selected items """
        if self.itemSelected:
            widgetInItem = self.itemWidget(self.itemSelected)
            widgetInItem.disableEdit()

        self.clearSelection()

    def __enabledWidgetEditMode(self):
        """ Sets the widget in item to edit mode """
        self.__clearSelection()

        # Change selected item to edit mode
        listItem = self.currentItem()
        widgetInItem = self.itemWidget(listItem)
        widgetInItem.enableEdit()

        # Save selected item
        self.itemSelected = listItem

    def addItemToListWidget(self, className: str, numClass: int, numOfClasses: int, colour: str) -> None:
        """ Adds item widget to list widget""" 
        # Create class widget for list item
        classListItemWidget = ClassListItemWidget(className, numClass, numOfClasses, colour) 

        # Create class item for list 
        classListItem = QListWidgetItem(self)
        self.addItem(classListItem)
        classListItem.setSizeHint(classListItemWidget.sizeHint())

        # Connect delete button
        classListItemWidget.classDeleteButton.clicked.connect(lambda: self.removeItemFromListWidget(classListItem))

        # Add class item to list
        self.addItem(classListItem)
        self.setItemWidget(classListItem, classListItemWidget)

    def removeItemFromListWidget(self, item: QListWidgetItem) -> None:
        """ Removes item widget from list widget""" 
        self.takeItem(self.row(item))
        self.itemSelected = None
