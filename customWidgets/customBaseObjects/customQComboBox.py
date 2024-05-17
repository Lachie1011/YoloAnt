"""
    customQComboBox.py
"""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QComboBox

class CustomQComboBox(QComboBox):
    def __init__(self, themePaletteColours, fontRegular):
        super().__init__()
        self.themePaletteColours = themePaletteColours
        self.fontRegular = fontRegular
        self.__baseStyleSheet()
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def __baseStyleSheet(self) -> None:
        self.setStyleSheet("QComboBox{"
                           f"font: 75 12pt {self.fontRegular};"
                           "border-radius: 5px;"
                           f"border: 1px solid {self.themePaletteColours['userInput.border']};"
                           f"background-color: {self.themePaletteColours['panel.sunken']};}}"
                           "QComboBox:hover{"
                           f"border: 1px solid {self.themePaletteColours['focus.foreground']}}}"
                           "QComboBox::drop-down:button{"
                           f"background-color: {self.themePaletteColours['panel.sunken']};"
                           "border-radius: 5px}"
                           "QComboBox::drop-down{"
                           f"color: {self.themePaletteColours['panel.sunken']};}}"
                           "QComboBox::down-arrow{"
                           "image: url(icons/icons8-drop-down-arrow-10.png)}")

    def focusInEvent(self, event):
        """ Sets background colour of widget when it is focused """
        super().focusInEvent(event)
        self.setStyleSheet("QLineEdit{"
                           f"font: 75 12pt {self.fontRegular};"
                           "border-radius: 5px;"
                           f"border: 1px solid {self.themePaletteColours['focus.foreground']};"
                           f"background-color: {self.themePaletteColours['panel.sunken']};}}"
                           "QComboBox::drop-down:button{"
                           f"background-color: {self.themePaletteColours['panel.sunken']};"
                           "border-radius: 5px}"
                           "QComboBox::drop-down{"
                           f"color: {self.themePaletteColours['panel.sunken']};}}"
                           "QComboBox::down-arrow{"
                           "image: url(icons/icons8-drop-down-arrow-10.png)}")