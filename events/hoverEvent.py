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
        
        # Ensure object is of QPushButton class
        if object.metaObject().className() != "QPushButton":
            return True

        # If object is checked, set selected icon 
        if object.isChecked():
            object.setIcon(QIcon(self.selectedPath))
            return False
    
        # Mouse has entered QObject
        if event.type() == QEvent.Type.Enter:
            object.setIcon(QIcon(self.selectedPath))
            return False

        # Mouse has left QObject
        if event.type() == QEvent.Type.Leave:
            object.setIcon(QIcon(self.unselectedPath))
            return False
        
        # Standard event processing
        return QObject.eventFilter(self, object, event)

class BackgroundHoverEvent(QObject):
    """
        Class to detect a hover event and change the background colour of a QObject
    """
    def __init__(self, object: QObject, rgbHoverColour, rgbBackgroundColour):
        super().__init__()
        self.object = object
        self.rgbHoverColour = rgbHoverColour
        self.rgbBackgroundColour = rgbBackgroundColour

    def eventFilter(self, object, event):
        print(event.type())
        # Mouse has entered QObject
        if event.type() == QEvent.Type.Enter:
            print(yes)
            if object.metaObject().className() == "QPushButton":
                self.__changePushButtonBackground(object, self.rgbHoverColour)

            if object.metaObject().className() == "QListWidgetItem":
                print('yes')
            return False

        # Mouse has left QObject
        if event.type() == QEvent.Type.Leave:
            if object.metaObject().className() == "QPushButton":
                self.__changePushButtonBackground(object, self.rgbBackgroundColour)
            return False
        
        # Standard event processing
        return QObject.eventFilter(self, object, event)

    def __changePushButtonBackground(self, object, colour: str) -> None:
        """ Change background colour of a pushbutton"""

        object.setStyleSheet(object.styleSheet() + f"background-color: rgb({colour});")