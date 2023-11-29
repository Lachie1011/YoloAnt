"""
    hoverEvent.py
"""

from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QObject, QEvent

class HoverEvent(QObject):
    """
        Class to detect a hover event and change the icon of a QObject
    """
    def __init__(self, object: QObject, unselectedPath: str, selectedPath: str):
        super().__init__()
        self.object = object
        self.unselectedPath = unselectedPath
        self.selectedPath = selectedPath

    def eventFilter(self, object, event):

        # Mouse has entered QObject
        if event.type() == QEvent.Type.Enter:
            self.object.setIcon(QIcon(self.selectedPath))
            return True

        # Mouse has left QObject
        if event.type() == QEvent.Type.Leave:
            self.object.setIcon(QIcon(self.unselectedPath))
            return True
        
        else:
            # Standard event processing
            return QObject.eventFilter(self, object, event)