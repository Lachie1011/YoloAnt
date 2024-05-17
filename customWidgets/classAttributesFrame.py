"""
    classAttributesFrame.py
"""
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import (QFrame, QLineEdit, QPushButton, QSizePolicy, QLabel, QHBoxLayout)

from customWidgets.customBaseObjects.customListItemQLineEdit import CustomListItemQLineEdit

class ClassAttributesFrame(QFrame):
    """
        Class that creates a frame that houses all class attributes. Used by classSelectionListWidgetItem.
    """

    def __init__(self, themePaletteColours, fontRegular):
        super().__init__()
        self.themePaletteColours = themePaletteColours
        self.fontRegular = fontRegular
        self.__setupStyleSheet()

        # Display the base frame by default
        self.editClassAttributesFrame.setVisible(False)

    def __setupStyleSheet(self) -> None:
        """ Sets up the style sheet of the frame """
        # Create base and edit frames
        self.baseClassAttributesFrame = self.__createBaseFrame()
        self.editClassAttributesFrame = self.__createEditFrame()

        # Set layout to frame 
        self.classAttributesFrameLayout = QHBoxLayout()
        self.classAttributesFrameLayout.addWidget(self.baseClassAttributesFrame)
        self.classAttributesFrameLayout.addWidget(self.editClassAttributesFrame)
        self.classAttributesFrameLayout.setContentsMargins(0,0,0,0)  
        self.setLayout(self.classAttributesFrameLayout)
    
    def __createBaseFrame(self) -> QFrame:
        """ Creates a base frame """
        # Colour picker label
        self.classColourLbl = QLabel()
        self.classColourLbl.setStyleSheet("QLabel{"
                                          f"background-color: transparent;"
                                          "border-radius: 4px;"
                                          "border-top-right-radius: 0px;"
                                          "border-bottom-right-radius: 0px;}")
        self.classColourLbl.setFixedWidth(20)

        # Class name label
        self.classNameLbl = QLabel()
        self.classNameLbl.setStyleSheet(f"QLabel{{font: 12pt {self.fontRegular};}}")
        self.classNameLbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.classNameLbl.setMinimumSize(20, 30)
        self.classNameLbl.setMaximumSize(170, 30)

        # Hotkey label
        self.classHotKeyLbl = QLabel()
        self.classHotKeyLbl.setStyleSheet("QLabel{"
                                          "background-color: transparent;"
                                          f"border: 2px solid {self.themePaletteColours['buttonFilled.background']};"
                                          "border-radius: 5px;}")
        self.classHotKeyLbl.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.classHotKeyLbl.setFixedWidth(25)
        self.classHotKeyLbl.setFixedHeight(25)

        # Annotation count label
        self.classAnnotationsCountLbl = QLabel()
        self.classAnnotationsCountLbl.setStyleSheet("QLabel{"
                                                    f"background-color: {self.themePaletteColours['panel.sunken']};"
                                                    f"border: 2px solid {self.themePaletteColours['panel.sunken']};"
                                                    "border-radius: 5px;}")
        self.classAnnotationsCountLbl.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.classAnnotationsCountLbl.setFixedWidth(25)
        self.classAnnotationsCountLbl.setFixedHeight(20)

        # Setting layout of custom widget 
        self.baseClassAttributesFrameLayout = QHBoxLayout()
        self.baseClassAttributesFrameLayout.addWidget(self.classColourLbl)
        self.baseClassAttributesFrameLayout.addWidget(self.classNameLbl)
        self.baseClassAttributesFrameLayout.addWidget(self.classHotKeyLbl)
        self.baseClassAttributesFrameLayout.addWidget(self.classAnnotationsCountLbl)
        self.baseClassAttributesFrameLayout.setContentsMargins(0,0,5,0)  

        # Create base frame
        self.baseClassAttributesFrame = QFrame()
        self.baseClassAttributesFrame.setLayout(self.baseClassAttributesFrameLayout)

        return self.baseClassAttributesFrame

    def __createEditFrame(self) -> QFrame:
        """ Creates a frame that will be used when in edit mode """ 
        # Colour picker button
        self.classColourBtn = QPushButton()
        self.classColourBtn.setStyleSheet("QPushButton{"
                                          f"background-color: transparent;"
                                          "border-radius: 4px;"
                                          f"border: 3px solid {self.themePaletteColours['buttonFilled.background']};}}"
                                          f"QPushButton:hover{{border: 3px solid {self.themePaletteColours['buttonFilled.hover']};}}")
        self.classColourBtn.setFixedWidth(20)
        self.classColourBtn.setFixedHeight(20)
        self.classColourBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Class name line edit
        self.classNameLineEdit = CustomListItemQLineEdit(self.themePaletteColours, f"font: 75 12pt {self.fontRegular};")
        self.classNameLineEdit.setMinimumSize(100, 30)
        self.classNameLineEdit.setMaximumSize(150, 30)
        self.classNameLineEdit.setTextMargins(2,0,2,0)
        self.classNameLineEdit.setCursorPosition(0)
        self.classNameLineEdit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.classNameLineEdit.setEditMode(True)

        # Hotkey button
        self.classHotKeyBtn = QPushButton()
        self.classHotKeyBtn.setStyleSheet("QPushButton{"
                                          f"background-color: {self.themePaletteColours['buttonFilled.background']};"
                                          f"border: 2px solid {self.themePaletteColours['buttonFilled.background']};"
                                          "border-radius: 5px;}"
                                          "QPushButton:hover{"
                                          f"background-color: {self.themePaletteColours['buttonFilled.hover']};"
                                          f"border: 2px solid {self.themePaletteColours['buttonFilled.hover']};}}")
        self.classHotKeyBtn.setFixedWidth(25)
        self.classHotKeyBtn.setFixedHeight(25)
        self.classHotKeyBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Delete button
        self.classDeleteBtn = QPushButton()
        self.classDeleteBtn.setStyleSheet("QPushButton{"
                                          "border-image: url('icons/icons8-trash-can-25.png');"
                                          "background-color: transparent;}")
        self.classDeleteBtn.setFixedWidth(20)
        self.classDeleteBtn.setFixedHeight(20)
        self.classDeleteBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Setting layout of custom widget 
        self.editClassAttributesFrameLayout = QHBoxLayout()
        self.editClassAttributesFrameLayout.addWidget(self.classColourBtn)
        self.editClassAttributesFrameLayout.addWidget(self.classNameLineEdit)
        self.editClassAttributesFrameLayout.addWidget(self.classHotKeyBtn)
        self.editClassAttributesFrameLayout.addWidget(self.classDeleteBtn)
        self.editClassAttributesFrameLayout.setContentsMargins(5,0,4,0)
        self.editClassAttributesFrameLayout.setSpacing(2)

        # Create frame
        self.editClassAttributesFrame = QFrame()
        self.editClassAttributesFrame.setLayout(self.editClassAttributesFrameLayout)
    
        return self.editClassAttributesFrame

    def setClassNameText(self, className: str) -> None:
        """ Updates widgets with specified class name """
        self.classNameLbl.setText(className)
        self.classNameLineEdit.setText(className)
        self.update()

    def setHotKeyText(self, hotKeyChar: str) -> None:
        """ Updates widgets with specified hot key character """
        self.classHotKeyLbl.setText(hotKeyChar) 
        self.classHotKeyBtn.setText(hotKeyChar)
        self.update()  

    def setClassColour(self, colour: tuple) -> None:
        """ Updates widgets with specified colour """
        self.classColourLbl.setStyleSheet("QLabel{"
                                          f"background-color: rgb{colour};"
                                          "border-radius: 4px;"
                                          "border-top-right-radius: 0px;"
                                          "border-bottom-right-radius: 0px;}")

        self.classColourBtn.setStyleSheet("QPushButton{"
                                          f"background-color: rgb{colour};"
                                          "border-radius: 4px;"
                                          f"border: 3px solid {self.themePaletteColours['buttonFilled.background']};}}"
                                          f"QPushButton:hover{{border: 3px solid {self.themePaletteColours['buttonFilled.hover']};}}")
        self.update()  

    def setClassAnnotationsCount(self, numberOfAnnotations: int) -> None:
        """ Updates widgets with specified annotations count """
        self.classAnnotationsCountLbl.setText(numberOfAnnotations)
        self.update()  

    def setEditMode(self, toggled: bool) -> None:
        """ Sets the edit mode of the frame """
        if toggled:
            self.baseClassAttributesFrame.setVisible(False)
            self.editClassAttributesFrame.setVisible(True)

        else:
            self.baseClassAttributesFrame.setVisible(True)
            self.editClassAttributesFrame.setVisible(False)