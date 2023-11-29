"""
    annotationPage.py
"""

import sys
from yoloAnt_ui import Ui_MainWindow
from events.hoverEvent import HoverEvent

from PyQt6.QtGui import QCursor
from PyQt6 import QtCore

class AnnotationPage():
    """
        Class to set up the functionality for the annotation page
    """
    def __init__(self, app) -> None:
        # TODO: fix up app type to yoloant app involes add futyure annotations and some if typing
        self.app = app
        self.ui = app.ui

        # Connecting signals and slots for the page

        # Applying hover events and cursor change to QObjects

        # Navigation Buttons
        self.ui.prevUnannoImageBtn.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.prevUnannoBtnHoverEvent = HoverEvent(self.ui.prevUnannoImageBtn, "icons/icons8-chevron-prev-30.png", "icons/icons8-chevron-prev-30-selected.png")
        self.ui.prevUnannoImageBtn.installEventFilter(self.prevUnannoBtnHoverEvent)

        self.ui.prevImageBtn.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.prevBtnHoverEvent = HoverEvent(self.ui.prevImageBtn, "icons/icons8-chevron-left-30.png", "icons/icons8-chevron-left-30-selected.png")
        self.ui.prevImageBtn.installEventFilter(self.prevBtnHoverEvent)

        self.ui.nextImageBtn.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.nextBtnHoverEvent = HoverEvent(self.ui.nextImageBtn, "icons/icons8-chevron-right-30.png", "icons/icons8-chevron-right-30-selected.png")
        self.ui.nextImageBtn.installEventFilter(self.nextBtnHoverEvent)

        self.ui.nextUnannoImageBtn.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.nextUnannoBtnHoverEvent = HoverEvent(self.ui.nextUnannoImageBtn, "icons/icons8-chevron-next-30.png", "icons/icons8-chevron--next-30-selected.png")
        self.ui.nextUnannoImageBtn.installEventFilter(self.nextUnannoBtnHoverEvent)

        # Tool Selection Buttons
        self.ui.mouseToolBtn.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.mouseBtnHoverEvent = HoverEvent(self.ui.mouseToolBtn, "icons/cursor-inactive.png", "icons/cursor-active.png")
        self.ui.mouseToolBtn.installEventFilter(self.mouseBtnHoverEvent)

        self.ui.annotateToolBtn.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.annotateBtnHoverEvent = HoverEvent(self.ui.annotateToolBtn, "icons/bounding-inactive.png", "icons/bounding-active.png")
        self.ui.annotateToolBtn.installEventFilter(self.annotateBtnHoverEvent)

