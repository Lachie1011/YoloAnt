"""
    customWidgetItemQFrame.py
"""
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QFrame

class CustomWidgetItemQFrame(QFrame):
    """
        Class that creates a custom QFrame
    """
    def __init__(self, themePaletteColours):
        """ init """
        super().__init__()
        self.themePaletteColours = themePaletteColours
        self.parentSelected = False
        self.__baseStyleSheet()

    def enterEvent(self, event) -> None:
        """ Sets background of widget when mouse enters item widget """
        if not self.parentSelected:
            self.setStyleSheet(f"background: {self.themePaletteColours['app.hover']};")

    def leaveEvent(self, event) -> None:
        """ Sets background of widget when mouse leaves item widget """
        if not self.parentSelected:
            self.setStyleSheet(f"background: {self.themePaletteColours['listItem.background']};")

    def __baseStyleSheet(self) -> None:
        """ Sets the base style sheet for the widget """
        self.setStyleSheet(f"QFrame{{background-color: {self.themePaletteColours['listItem.background']};}}")
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setFixedHeight(60)

    def __editStyleSheet(self) -> None:
        """ Sets the edit style sheet for the widget """
        self.setStyleSheet(f"QFrame{{background-color: {self.themePaletteColours['listItem.edit']};}}")
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

    def setSelected(self) -> None:
        """ Changes stylesheet of widgets to reflect being selected """
        self.setStyleSheet(f"QFrame{{background-color: {self.themePaletteColours['app.selected']};}}")
        self.parentSelected = True

    def clearSelection(self) -> None:
        """ Changes stylesheet of widgets to reflect being selected """
        self.__baseStyleSheet()
        self.parentSelected = False

    def setEditMode(self, toggled: bool) -> None:
        """ Sets the edit mode of the widget """
        if toggled:
            self.__editStyleSheet()

        else:
            self.__baseStyleSheet()