"""
    annotationListWidgetItem.py
"""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor 
from PyQt6.QtWidgets import (QFrame, QLabel, QHBoxLayout, QSpacerItem, QPushButton, QSizePolicy)

class AnnotationListWidgetItem(QFrame):
    def __init__(self, annotationName):
        super().__init__()
        self.annotationName = annotationName
        self.parentItem = None

        # Setup stylesheet
        self.__setupStyleSheet()
    
    def enterEvent(self, event) -> None:
        """ Sets background of widget when mouse enters item widget """
        if not self.parentItem.isSelected():
            self.annotationNameLbl.setStyleSheet("QLabel{"
                                                 "color: rgb(255,255,255);}")

    def leaveEvent(self, event) -> None:
        """ Sets background of widget when mouse leaves item widget """
        if not self.parentItem.isSelected():
            self.annotationNameLbl.setStyleSheet("QLabel{"
                                                 "color: rgb(200,200,200);}")

    def __setupStyleSheet(self) -> None:

        self.setFixedHeight(40)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Annotation name
        self.annotationNameLbl = QLabel(self.annotationName)
        self.annotationNameLbl.setStyleSheet("QLabel{"
                                             "color: rgb(200,200,200);}")
        self.annotationNameLbl.setMinimumSize(100, 30)

        # Hide annotation button
        self.hideAnnotationBtn = QPushButton()
        self.hideAnnotationBtn.setStyleSheet("QPushButton{"
                                             "background-color: rgb(105,105,105);}")
        self.hideAnnotationBtn.setFixedWidth(20)
        self.hideAnnotationBtn.setFixedHeight(20)
        self.hideAnnotationBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Delete button
        self.annotationDeleteButton = QPushButton()
        self.annotationDeleteButton.setStyleSheet("QPushButton{"
                                             "background-color: rgb(105,105,105);}")
        self.annotationDeleteButton.setFixedWidth(20)
        self.annotationDeleteButton.setFixedHeight(20)
        self.annotationDeleteButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Horizontal spacers
        spacer = QSpacerItem(15, 5, QSizePolicy.Policy.Fixed)
        
        # Setting layout of custom widget 
        self.annotaitonWidgetItemLayout = QHBoxLayout()
        self.annotaitonWidgetItemLayout.addItem(spacer)
        self.annotaitonWidgetItemLayout.addWidget(self.annotationNameLbl)
        self.annotaitonWidgetItemLayout.addItem(spacer)
        self.annotaitonWidgetItemLayout.addWidget(self.hideAnnotationBtn)
        self.annotaitonWidgetItemLayout.addWidget(self.annotationDeleteButton)

        # self.classItemWidetLayout.setContentsMargins(0,0,0,0)
        self.setLayout(self.annotaitonWidgetItemLayout)