"""
    customQListWidget.py
"""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QListWidget, QListWidgetItem

class CustomQListWidget(QListWidget):
    """
        Class that creates a custom list widget
    """
    def __init__(self):
        """ init """
        super().__init__()

    def addItemToList(self, listWidgetItem: QListWidgetItem) -> None:
        """ Adds item to list widget """ 
        # Create item for list widget
        listItem = QListWidgetItem(self)
        listItem.setSizeHint(listWidgetItem.sizeHint())
        listWidgetItem.parentItem = listItem
        
        # Add item to list widget
        self.addItem(listItem)
        self.setItemWidget(listItem, listWidgetItem)

    def removeItemFromList(self, listItem: QListWidgetItem) -> None:
        """ Removes list item from list widget""" 
        self.takeItem(self.row(listItem))