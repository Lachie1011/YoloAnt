"""
    classSelectionFrame.py
"""
from PyQt6.QtWidgets import QFrame

class classSelectionFrame(QFrame):
    """
        Class that creates a custom QFrame for the class selection list item
    """
    def __init__(self, themePaletteColours):
        super().__init__()

        # Member variables
        self.themePaletteColours = themePaletteColours
        self.parentSelected = False

        # Apply default style sheet
        self.__defaultStyleSheet()

    def __defaultStyleSheet(self) -> None:
        """ Applies default style sheet to frame """
        self.setStyleSheet(f"QFrame{{background-color: {self.themePaletteColours['listItem.background']};}}")
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setFixedHeight(60)

    def __editStyleSheet(self) -> None:
        """ Applies edit style sheet to frame """
        self.setStyleSheet(f"QFrame{{background-color: {self.themePaletteColours['listItem.edit']};}}")
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

    def enterEvent(self, event) -> None:
        """ Changes background of frame when mouse enters """
        if not self.parentSelected:
            self.setStyleSheet(f"background: {self.themePaletteColours['app.hover']};")

    def leaveEvent(self, event) -> None:
        """ Changes background of frame when mouse leaves """
        if not self.parentSelected:
            self.setStyleSheet(f"background: {self.themePaletteColours['listItem.background']};")

    def setToSelectedState(self) -> None:
        """ Changes background of frame to selected state """
        self.setStyleSheet(f"QFrame{{background-color: {self.themePaletteColours['app.selected']};}}")
        self.parentSelected = True

    def clearSelection(self) -> None:
        """ Changes stylesheet of frame to default state """
        self.__defaultStyleSheet()

    def setEditMode(self, toggled: bool) -> None:
        """ Sets the edit mode of the frame """
        if toggled:
            self.__editStyleSheet()

        else:
            self.__defaultStyleSheet()