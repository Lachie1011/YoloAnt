"""
    customPanelQTextEdit.py
"""
from PyQt6.QtCore import Qt, pyqtSignal as Signal 
from PyQt6.QtWidgets import QTextEdit

class CustomPanelQTextEdit(QTextEdit):
    """
        Class that creates a custom text edit widget for application panel
    """
    editingFinished = Signal() 

    def __init__(self, themePaletteColours, fontType):
        super().__init__()
        self.editableState = False
        self.themePaletteColours = themePaletteColours
        self.fontType = fontType
        self.__baseStyleSheet()
        self.setViewportMargins(3,3,3,3)

    def __baseStyleSheet(self) -> None:
        """ Sets the style sheet for the widget """
        self.setStyleSheet("QTextEdit{"
                           f"font: 75 12pt {self.fontType};"
                           f"border: 1px solid {self.themePaletteColours['panel.background']};"
                           f"background-color: {self.themePaletteColours['panel.background']};"
                           "border-radius: 5px;"
                           f"color: {self.themePaletteColours['font.header']};}}")
        self.setReadOnly(True)
        self.viewport().setCursor(Qt.CursorShape.ArrowCursor)

    def __editableStyleSheet(self) -> None:
        """ Sets the style sheet for the widget """
        self.setStyleSheet("QTextEdit{"
                           f"font: 75 12pt {self.fontType};"
                           f"background-color: {self.themePaletteColours['panel.sunken']};"
                           "border-radius: 5px;"
                           f"border: 2px solid {self.themePaletteColours['userInput.border']};"
                           f"color: {self.themePaletteColours['font.header']};}}"
                           "QTextEdit:hover{"
                           f"border: 1px solid {self.themePaletteColours['focus.foreground']}}}")
        self.setReadOnly(False)
        self.viewport().setCursor(Qt.CursorShape.PointingHandCursor)
   
    def focusInEvent(self, event):
        """ Sets background colour of widget when it is focused """
        if self.editableState:
            super().focusInEvent(event)
            self.viewport().setCursor(Qt.CursorShape.IBeamCursor)
            self.setStyleSheet("QTextEdit{"
                               f"font: 75 12pt {self.fontType};"
                               "border-radius: 5px;"
                               f"background-color: {self.themePaletteColours['panel.sunken']};"
                               f"border: 1px solid {self.themePaletteColours['focus.foreground']}}}")

    def focusOutEvent(self, event):
        """ Sets background colour of widget when it loses focus """
        if self.editableState:
            super().focusOutEvent(event)
            self.__editableStyleSheet()
            self.editingFinished.emit()

    def setEditMode(self, toggled) -> None:
        """ Sets the edit mode of the widget """
        if toggled:
            self.__editableStyleSheet()

        else:
            self.__baseStyleSheet()

        self.editableState = toggled
