"""
    selectableQListWidget.py
"""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QListWidgetItem, QAbstractItemView

from customWidgets.commonWidgets.customQListWidget import CustomQListWidget

class SelectableQListWidget(CustomQListWidget):
    """
        Class that creates a list widget that holds all classes for creating annotations
    """
    def __init__(self):
        super().__init__()

        # Member variables
        self.currentItemSelected = None

        # Connect signals and slots
        self.itemClicked.connect(lambda item: self.selectItemFromList(item))

    def mouseMoveEvent(object, event):
        # Disables selection with mouse click + drag
        event.ignore()   

    def selectItemFromList(self, listItem: QListWidgetItem) -> None:
        """ Sets an item in the list widget to selected """
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.clearSelectionInList()
        self.itemWidget(listItem).setSelected()
        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.currentItemSelected = listItem

    def removeItemFromList(self, listItem: QListWidgetItem) -> None:
        """ Removes list item from list widget""" 
        super().removeItemFromList(listItem)
        self.currentItemSelected = None

    def clearSelectionInList(self) -> None:
        """ Clears the selection of items in list widget """
        if self.currentItemSelected is not None:
            self.itemWidget(self.currentItemSelected).clearSelected()
        self.clearSelection()

    def getCurrentSelectedItem(self) -> QListWidgetItem:
        """ Gets the current selected item in the list """
        return self.currentItemSelected