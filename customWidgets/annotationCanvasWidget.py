"""
    annotationCanvasWidget.py
"""

import time

from PyQt6.QtCore import Qt
from PyQt6.QtCore import QPoint, QRect
from PyQt6.QtGui import QPixmap, QPixmap, QPainter, QPen, QColor, QCursor
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QGraphicsView, QGraphicsScene


class AnnotationCanvasWidget(QGraphicsView):
    """ A custom widget for the annotation canvas used for drawing bounding boxes """
    def __init__(self, parent):
        super(AnnotationCanvasWidget, self).__init__(parent)

        # Members
        self.rectBegin = None
        self.rectEnd = None
        self.currentImagePath = "/home/lachie/extractedImages/1029.jpg"  #TODO: this will need to be on each new image 

        # Setting alignment
        self.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        # Creating the graphics scene
        self.scene = QGraphicsScene()

        # Scene is bound to graphics view geometry
        self.scene.setSceneRect(self.x(), self.y(), self.width(), self.height())
        self.scene.setBackgroundBrush(QColor(255,255,255))

        self.setScene(self.scene)

    def mousePressEvent(self, event):
        """ Event to capture mouse press and update rect coords """
        self.rectBegin = self.mapToScene(event.pos())
        self.rectEnd = self.mapToScene(event.pos())

    def mouseMoveEvent(self, event):
        """ Event to capture mouse move and update rect coords """
        self.rectEnd = self.mapToScene(event.pos())
        self.scene.clear()
        self.scene.addRect(self.rectBegin.x(), self.rectBegin.y(), abs(self.rectEnd.x() - self.rectBegin.x()), abs(self.rectEnd.y() - self.rectBegin.y()))

    def mouseReleaseEvent(self, event):
        """ Event to capture mouse release and update rect coords """
        self.rectEnd = self.mapToScene(event.pos())
        self.scene.clear()
        self.scene.addRect(self.rectBegin.x(), self.rectBegin.y(), abs(self.rectEnd.x() - self.rectBegin.x()), abs(self.rectEnd.y() - self.rectBegin.y()))
