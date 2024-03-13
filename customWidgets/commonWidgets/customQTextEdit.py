"""
    customQTextEdit.py
"""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTextEdit

class CustomQTextEdit(QTextEdit):
    """
        Class that creates a custom text edit widget
    """
    def __init__(self, themePaletteColours, fontColour, fontStyle):
        super().__init__()
        # Member variables
        self.themePaletteColours = themePaletteColours
        self.fontColour = fontColour
        self.fontStyle = fontStyle
        
    def defaultStyleSheet(self) -> None:
        """ Sets the style sheet for the widget """
        self.setStyleSheet("QTextEdit{"
                           f"font: {self.fontStyle};"
                           f"background-color: {self.themePaletteColours['panel.sunken']};"
                           "border-radius: 5px;"
                           f"border: 2px solid {self.themePaletteColours['userInput.border']};"
                           f"color: {self.fontColour};}}"
                           "QTextEdit:hover{"
                           f"border: 2px solid {self.themePaletteColours['focus.foreground']}}}")
        self.viewport().setCursor(Qt.CursorShape.PointingHandCursor)        
        self.setViewportMargins(3,3,3,3)
        self.setReadOnly(False)
   
    def focusInEvent(self, event):
        """ Change stylesheet when focused """
        super().focusInEvent(event)
        self.setStyleSheet("QTextEdit{"
                           f"font: {self.fontStyle};"
                           f"background-color: {self.themePaletteColours['panel.sunken']};"
                           "border-radius: 5px;"
                           f"border: 2px solid {self.themePaletteColours['focus.foreground']};"
                           f"color: {self.fontColour};}}")
        self.viewport().setCursor(Qt.CursorShape.IBeamCursor)

    def focusOutEvent(self, event):
        """ Change stylesheet to default after loss of focus """
        super().focusOutEvent(event)
        self.defaultStyleSheet()