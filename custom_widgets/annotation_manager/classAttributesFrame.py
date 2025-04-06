import os

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import (
    QFrame, QLabel, QPushButton, QHBoxLayout, QSizePolicy, QLineEdit
)
from PyQt6.uic import loadUi

from custom_widgets.customBaseObjects.customListItemQLineEdit import CustomListItemQLineEdit

ui_path = os.path.join(os.path.dirname(__file__), '../../ui/annotation_manager/')
class ClassAttributesFrame(QFrame):
    """
    Frame that contains widgets for class attributes in view/edit mode.
    """

    def __init__(self):
        super().__init__()
        self.__setupStyleSheet()
        self.setEditMode(False)

    def __setupStyleSheet(self):
        """ Sets up style sheet for frame """
        self.classItemFrame = loadUi(os.path.join(ui_path, "classItemFrame.ui"))
        self.classNameLbl = self.classItemFrame.findChild(QLabel, "classNameLbl")
        self.classHotKeyLbl = self.classItemFrame.findChild(QLabel, "classHotKeyLbl")
        self.annotationCountLbl = self.classItemFrame.findChild(QLabel, "annotationCountLbl")

        self.classItemEditableFrame = loadUi(os.path.join(ui_path, "classItemFrameEditable.ui"))
        self.classNameLineEdit = self.classItemEditableFrame.findChild(QLineEdit, "classNameLineEdit")
        self.classHotKeyBtn = self.classItemEditableFrame.findChild(QPushButton, "classHotKeyBtn")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.classItemFrame)
        layout.addWidget(self.classItemEditableFrame)

    # --- Public Setters ---
    def setClassNameText(self, className: str):
        self.classNameLbl.setText(className)
        self.classNameLineEdit.setText(className)

    def setHotKeyText(self, hotKeyChar: str):
        self.classHotKeyLbl.setText(hotKeyChar)
        self.classHotKeyBtn.setText(hotKeyChar)

    def setClassColour(self, colour: tuple):
        rgb = f"rgb{colour}"

        # self.classColourLbl.setStyleSheet(f"""
        #     QLabel {{
        #         background-color: {rgb};
        #         border-radius: 4px;
        #         border-top-right-radius: 0px;
        #         border-bottom-right-radius: 0px;
        #     }}
        # """)
        #
        # self.classColourBtn.setStyleSheet(f"""
        #     QPushButton {{
        #         background-color: {rgb};
        #         border-radius: 4px;
        #         border: 3px solid {self.themePaletteColours['buttonFilled.background']};
        #     }}
        #     QPushButton:hover {{
        #         border: 3px solid {self.themePaletteColours['buttonFilled.hover']};
        #     }}
        # """)

    def setClassAnnotationsCount(self, numberOfAnnotations: int):
        self.annotationCountLbl.setText(str(numberOfAnnotations))

    def setEditMode(self, toggled: bool):
        self.classItemFrame.setVisible(not toggled)
        self.classItemEditableFrame.setVisible(toggled)
