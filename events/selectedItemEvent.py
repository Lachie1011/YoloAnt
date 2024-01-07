"""
    selectedItemEvent.py
"""

from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QObject, QEvent

class SelectedItemEvent(QObject):
    """
        Class to change the displayed widgets when item is selected in QListWidget
    """

    def __init__(self, object: QObject, selectedRGBcolour, unselectedRGBColour):
        super().__init__()
        self.object = object
        self.selectedRGBcolour = selectedRGBcolour
        self.unselectedRGBColour = unselectedRGBColour

    def eventFilter(self, object, event):

        # Ensure object is of QPushButton class
        if object.itemSelectionChanged():
            listItem = object.selectedItems()[0]
            widgetInItem = listItem.ItemWidget(listItem)
            return False
        
        # Standard event processing
        return QObject.eventFilter(self, object, event)