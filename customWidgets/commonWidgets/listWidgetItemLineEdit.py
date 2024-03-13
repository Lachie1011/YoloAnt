"""
    listWidgetItemLineEdit.py
"""
from PyQt6.QtCore import Qt
from customWidgets.commonWidgets.customQLineEdit import CustomQLineEdit

class ListWidgetItemLineEdit(CustomQLineEdit):
    """
        Class that creates a custom line edit widget for a list widget item 
    """
    def __init__(self, themePaletteColours, fontColour, fontStyle):
        """ __init__ """
        super().__init__(themePaletteColours, fontColour, fontStyle)

        # Member variables
        self.editableState = False
        self.themePaletteColours = themePaletteColours
        self.fontStyle = fontStyle

        # Set stylesheet
        self.__styleSheet()

    def __styleSheet(self) -> None:
        """ Applies style sheet to widget """
        self.setStyleSheet("QLineEdit{"
                           f"{self.fontStyle};"
                           f"border: 1px solid transparent;"
                           f"background-color: transparent;"
                           "border-radius: 5px;"
                           f"color: {self.themePaletteColours['font.header']};}}")
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.setTextMargins(3,3,3,3)
        self.setReadOnly(True)


    def setEditMode(self, toggled: bool) -> None:
        """ Sets the edit mode of the widget """
        if toggled:
            super().defaultStyleSheet()

        else:
            self.__styleSheet()

        self.editableState = toggled