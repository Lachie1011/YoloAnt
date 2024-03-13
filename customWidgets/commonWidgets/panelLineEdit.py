"""
    panelQLineEdit.py
"""
from PyQt6.QtCore import Qt
from customWidgets.commonWidgets.customQLineEdit import CustomQLineEdit

class PanelLineEdit(CustomQLineEdit):
    """
        Class that creates a custom line edit widget for application panel
    """
    def __init__(self, themePaletteColours, fontColour, fontStyle):
        """ __init__ """
        super().__init__(themePaletteColours, fontColour, fontStyle)
        # Member variables
        self.themePaletteColours = themePaletteColours
        self.fontStyle = fontStyle
        self.editableState = False

        # Set style sheet
        self.__styleSheet()

    def __styleSheet(self) -> None:
        """ Sets the style sheet for the widget """
        self.setStyleSheet("QLineEdit{"
                           f"font: {self.fontStyle};"
                           f"border: 1px solid {self.themePaletteColours['panel.background']};"
                           f"background-color: {self.themePaletteColours['panel.background']};"
                           "border-radius: 5px;"
                           f"color: {self.themePaletteColours['font.header']};}}")
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.setTextMargins(3,3,3,3)
        self.setReadOnly(True)

    def focusInEvent(self, event):
        """ Change background on focus in when widget is editable """
        if self.editableState:
            super().focusInEvent(event)

    def focusOutEvent(self, event):
        """ Change background on focus out when widget is editable """
        if self.editableState:
            super().focusOutEvent(event)

    def setEditMode(self, toggled: bool) -> None:
        """ Sets the edit mode of the widget """
        if toggled:
            super().defaultStyleSheet()

        else:
            self.__styleSheet()

        self.editableState = toggled