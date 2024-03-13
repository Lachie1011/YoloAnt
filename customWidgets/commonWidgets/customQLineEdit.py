"""
    customQLineEdit.py
"""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLineEdit

class CustomQLineEdit(QLineEdit):
    """
        Class that creates a custom line edit widget
    """
    def __init__(self, themePaletteColours, fontColour, fontStyle):
        """ init """
        super().__init__()

        # Member Variables
        self.themePaletteColours = themePaletteColours
        self.fontColour = fontColour
        self.fontStyle = fontStyle

    def defaultStyleSheet(self) -> None:
        """ Sets up default stylesheet of custom line edit widget """
        self.setStyleSheet("QLineEdit{"
                           f"background-color: {self.themePaletteColours['panel.sunken']};"
                           "border-radius: 5px;"
                           f"border: 2px solid {self.themePaletteColours['userInput.border']};"
                           f"font: {self.fontStyle};"
                           f"color: {self.fontColour};}}"
                           "QLineEdit:hover{"
                           f"border: 2px solid {self.themePaletteColours['focus.foreground']}}}")
        self.setReadOnly(False)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setTextMargins(3,3,3,3)

    def focusInEvent(self, event):
        """ Change stylesheet when focused """
        super().focusInEvent(event)
        self.setStyleSheet("QLineEdit{"
                           f"background-color: {self.themePaletteColours['panel.sunken']};"
                           "border-radius: 5px;"
                           f"border: 2px solid {self.themePaletteColours['focus.foreground']};"
                           f"font: {self.fontStyle};"
                           f"color: {self.fontColour};}}")
        self.setCursor(Qt.CursorShape.IBeamCursor)

    def focusOutEvent(self, event):
        """ Change stylesheet to default after loss of focus """
        super().focusOutEvent(event)
        self.defaultStyleSheet()
