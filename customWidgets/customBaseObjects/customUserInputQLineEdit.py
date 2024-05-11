"""
    customUserInputQLineEdit.py
"""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLineEdit

class CustomUserInputQLineEdit(QLineEdit):
    """
        Class that creates a user input line edit widget
    """
    def __init__(self, themePaletteColours, fontRegular):
        super().__init__()
        self.themePaletteColours = themePaletteColours
        self.fontRegular = fontRegular
        self.__baseStyleSheet()
        self.setTextMargins(3,3,3,3)

    def __baseStyleSheet(self) -> None:
        """ Sets the style sheet for the widget """
        self.setStyleSheet("QLineEdit{"
                           f"font: 12pt {self.fontRegular};"
                           "border-radius: 5px;"
                           f"color: {self.themePaletteColours['font.regular']};"
                           f"background-color: {self.themePaletteColours['panel.sunken']};"
                           f"border: 1px solid {self.themePaletteColours['userInput.border']}}}"
                           "QLineEdit:hover{"
                           f"border: 1px solid {self.themePaletteColours['focus.foreground']}}}")

    def validTextInput(self, valid) -> None:
        if not valid:
            self.setStyleSheet("QLineEdit{"
                               f"font: 12pt {self.fontRegular};"
                               "border-radius: 5px;"
                               f"color: {self.themePaletteColours['font.regular']};"
                               f"background-color: {self.themePaletteColours['panel.sunken']};"
                               "border: 1px solid red}")

        else:
            self.__baseStyleSheet()

    def focusInEvent(self, event):
        """ Sets background colour of widget when it is focused """
        super().focusInEvent(event)
        self.setStyleSheet("QLineEdit{"
                           f"font: 12pt {self.fontRegular};"
                           "border-radius: 5px;"
                           f"color: {self.themePaletteColours['font.regular']};"
                           f"background-color: {self.themePaletteColours['panel.sunken']};"
                           f"border: 1px solid {self.themePaletteColours['focus.foreground']};}}")

    def focusOutEvent(self, event):
        """ Sets background colour of widget when it loses focus """
        super().focusOutEvent(event)
        self.__baseStyleSheet()