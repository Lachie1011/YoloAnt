"""
    annotationListWidgetItem.py
"""
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QCursor, QIcon
from PyQt6.QtWidgets import (QFrame, QLabel, QHBoxLayout, QSpacerItem, QPushButton, QSizePolicy)

class AnnotationListWidgetItem(QFrame):
    """
        Class that creates a custom annotation item widget for annotation list.

        params:

    """
    def __init__(self, annotationName, themePaletteColours):
        super().__init__()
        self.annotationName = annotationName
        self.parentItem = None
        self.themePaletteColours = themePaletteColours

        # Setup stylesheet
        self.__setupStyleSheet()

        # Setup signals and slots
        self.hideAnnotationBtn.clicked.connect(lambda: self.__displayedHideAnnotationIcon())
    
    def enterEvent(self, event) -> None:
        """ Sets background of widget when mouse enters item widget """
        if not self.parentItem.isSelected():
            self.annotationNameLbl.setStyleSheet("QLabel{"
                                                 f"color: {self.themePaletteColours['font.hover']};}}")

    def leaveEvent(self, event) -> None:
        """ Sets background of widget when mouse leaves item widget """
        if not self.parentItem.isSelected():
            self.annotationNameLbl.setStyleSheet("QLabel{"
                                                 f"color: {self.themePaletteColours['font.regular']};}}")

    def __setupStyleSheet(self) -> None:
        """ Sets up style sheet for annotation selection frame """
        self.setFixedHeight(60)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Annotation name
        self.annotationNameLbl = QLabel(self.annotationName)
        self.annotationNameLbl.setStyleSheet("QLabel{"
                                             f"color: {self.themePaletteColours['font.regular']};}}")
        self.annotationNameLbl.setMinimumSize(100, 30)

        # Hide annotation button - eye closed
        self.hideAnnotationBtn = QPushButton()
        self.hideAnnotationBtn.setStyleSheet("QPushButton{"
                                             "border-image: url('icons/icons8-eye-open-25.png');}"
                                             "QPushButton:hover{"
                                             "border-image: url('icons/icons8-eye-open-hover-25.png');}")
        self.hideAnnotationBtn.setFixedWidth(20)
        self.hideAnnotationBtn.setFixedHeight(20)
        self.hideAnnotationBtn.setCheckable(True)
        self.hideAnnotationBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Delete button
        self.annotationDeleteButton = QPushButton()
        self.annotationDeleteButton.setStyleSheet("QPushButton{"
                                                 "border-image: url('icons/icons8-trash-can-25.png');}")
        self.annotationDeleteButton.setFixedWidth(18)
        self.annotationDeleteButton.setFixedHeight(18)
        self.annotationDeleteButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Horizontal spacers
        spacer1 = QSpacerItem(15, 5, QSizePolicy.Policy.Fixed)
        spacer2 = QSpacerItem(15, 5, QSizePolicy.Policy.Fixed)
        
        # Setting layout of custom widget 
        self.annotaitonWidgetItemLayout = QHBoxLayout()
        self.annotaitonWidgetItemLayout.addItem(spacer1)
        self.annotaitonWidgetItemLayout.addWidget(self.annotationNameLbl)
        self.annotaitonWidgetItemLayout.addItem(spacer2)
        self.annotaitonWidgetItemLayout.addWidget(self.hideAnnotationBtn)
        self.annotaitonWidgetItemLayout.addWidget(self.annotationDeleteButton)
        self.setLayout(self.annotaitonWidgetItemLayout)

    def __displayedHideAnnotationIcon(self) -> None:
        """ Changes the icon depending on checked status """
        if self.hideAnnotationBtn.isChecked():
            self.hideAnnotationBtn.setStyleSheet("QPushButton{"
                                                 "border-image: url('icons/icons8-eye-closed-25.png');}"
                                                 "QPushButton:hover{"
                                                 "border-image: url('icons/icons8-eye-closed-hover-25.png');}")

        else:
            self.hideAnnotationBtn.setStyleSheet("QPushButton{"
                                                 "border-image: url('icons/icons8-eye-open-25.png');}"
                                                 "QPushButton:hover{"
                                                 "border-image: url('icons/icons8-eye-open-hover-25.png');}")