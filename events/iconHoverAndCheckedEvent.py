"""
    iconHoverEvent.py
"""

from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QObject, QEvent
from PyQt6.QtWidgets import QPushButton


class IconHoverAndCheckedEvent(QObject):
    """
        Class to detect a hover event and change the icon of a QObject
    """
    def __init__(self, target: QObject, unselectedIconImagePath: str, selectedIconImagePath: str):
        super().__init__()
        self.object = target
        self.unselectedPath = unselectedIconImagePath
        self.selectedPath = selectedIconImagePath
        target.setIcon(QIcon(unselectedIconImagePath))

    def eventFilter(self, object, event):
        if not isinstance(object, QPushButton):
            return super().eventFilter(object, event)

        if object.isChecked():
            object.setIcon(QIcon(self.selectedPath))
            return False

        if event.type() == QEvent.Type.Enter:
            object.setIcon(QIcon(self.selectedPath))
            return False

        if event.type() == QEvent.Type.Leave:
            object.setIcon(QIcon(self.unselectedPath))
            return False

        return super().eventFilter(object, event)
