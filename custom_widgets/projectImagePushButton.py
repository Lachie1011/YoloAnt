"""
    projectImageQPushButton.py
"""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QPushButton, QSizePolicy, QGraphicsOpacityEffect)

class ProjectImagePushButton(QPushButton):
    """
        Class that creates a custom push button for project image selection.
    """
    def __init__(self, themePaletteColours):
        super().__init__()
        self.editableState = False
        self.themePaletteColours = themePaletteColours

        # Default stylesheet
        self.__baseStyleSheet()

    def __baseStyleSheet(self) -> None:
        """ Sets the style sheet for the widget """
        self.setStyleSheet("QPushButton{"
                           f"background-color: {self.themePaletteColours['panel.sunken']};" 
                           "border-radius: 5px;}")
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.opacityEffect = QGraphicsOpacityEffect()
        self.opacityEffect.setOpacity(0.99)
        self.setGraphicsEffect(self.opacityEffect)
        self.setAutoFillBackground(True)

    def __editableStyleSheet(self) -> None:
        """ Sets the style sheet for the widget """
        self.setStyleSheet("QPushButton{"
                           f"background-color: {self.themePaletteColours['panel.sunken']};" 
                           f"border: 1px solid {self.themePaletteColours['userInput.border']};"
                           "border-radius: 5px;}")
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def enterEvent(self, event) -> None:
        """ Sets background of widget when mouse enters item widget """
        if self.editableState:
            self.setStyleSheet("QPushButton{"
                               f"background-color: {self.themePaletteColours['panel.sunken']};" 
                               f"border: 1px solid {self.themePaletteColours['focus.foreground']};"
                               "border-radius: 5px;}")
            self.opacityEffect.setOpacity(0.5)

    def leaveEvent(self, event) -> None:
        """ Sets background of widget when mouse leaves item widget """
        if self.editableState:
            self.setStyleSheet("QPushButton{"
                                f"background-color: {self.themePaletteColours['panel.sunken']};" 
                                f"border: 1px solid {self.themePaletteColours['userInput.border']};"
                                "border-radius: 5px;}")
            self.opacityEffect.setOpacity(0.99)

    def setEditMode(self, toggled) -> None:
        """ Sets the edit mode of the widget """
        if toggled:
            self.__editableStyleSheet()

        else:
            self.__baseStyleSheet()

        self.editableState = toggled