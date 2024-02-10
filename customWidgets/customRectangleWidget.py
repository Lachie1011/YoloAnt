"""
    customRectangleWidget.py
"""

from enum import Enum
from PyQt6.QtCore import Qt, QEvent, QPointF, QPoint
from PyQt6.QtGui import QPixmap, QColor, QPen, QBrush
from PyQt6.QtWidgets import QGraphicsRectItem, QGraphicsItem, QGraphicsEllipseItem


class CustomRectangleWidget(QGraphicsRectItem):
    """ A custom widget that reimplements QGraphicsRectItem """
    def __init__(self, x, y, width, height, scene, classColour):
        super().__init__(x, y, width, height)

        self.scene = scene
        self.classColour = classColour

        # Handle definitions
        self.DIAMETER = 12    # technically you set a length and width for the ellipse but diameter
        self.X_BORDER = 0
        self.Y_BORDER = 0

        self.editable = False

        self.handles = []

    def itemChange(self, change, value):
        """ Reimplements the itemChange function """
        if change == QGraphicsItem.GraphicsItemChange.ItemSelectedChange:
            if(value):
                self.editable = True
                self.addHandles()
            else:
                self.editable = False
                self.removeHandles()

        return super().itemChange(change, value)

    def addHandles(self):
        """ Adds editable handles to the rectItem """
        # If we already have handles dont add anymore TODO: fix warning when we already have handles

        # Creating top-left, top-right, bottom-left, bottom-right "handles"
        self.topLeftHandle = QGraphicsEllipseItem(self.rect().left() - self.X_BORDER - self.DIAMETER / 2, self.rect().top() - self.Y_BORDER - self.DIAMETER / 2, self.DIAMETER, self.DIAMETER, self)
        self.topRightHandle = QGraphicsEllipseItem(self.rect().right() + self.X_BORDER - self.DIAMETER / 2, self.rect().top() - self.Y_BORDER - self.DIAMETER / 2, self.DIAMETER, self.DIAMETER, self)
        self.bottomLeftHandle = QGraphicsEllipseItem(self.rect().left() - self.X_BORDER - self.DIAMETER / 2, self.rect().bottom() + self.Y_BORDER - self.DIAMETER / 2, self.DIAMETER, self.DIAMETER, self)
        self.bottomRightHandle = QGraphicsEllipseItem(self.rect().right() + self.X_BORDER - self.DIAMETER / 2, self.rect().bottom() + self.Y_BORDER - self.DIAMETER / 2, self.DIAMETER, self.DIAMETER, self)

        # Colouring the handles
        self.topLeftHandle.setBrush(QBrush(self.classColour, style = Qt.BrushStyle.NoBrush))
        self.topRightHandle.setBrush(QBrush(self.classColour, style = Qt.BrushStyle.SolidPattern))
        self.bottomLeftHandle.setBrush(QBrush(self.classColour, style = Qt.BrushStyle.SolidPattern))
        self.bottomRightHandle.setBrush(QBrush(self.classColour, style = Qt.BrushStyle.SolidPattern))

        # Appending handles to list to track
        self.handles.append(self.topLeftHandle)
        self.handles.append(self.topRightHandle)
        self.handles.append(self.bottomLeftHandle)
        self.handles.append(self.bottomRightHandle)

        # Adding handles to scene
        for handle in self.handles:
            self.scene.addItem(handle)

    def removeHandles(self):
        """ Removes handles from the rect item """
        for handle in self.handles:
            self.scene.removeItem(handle)
        self.handles = []

    def mousePressEvent(self, event):
        """ Reimplements the mouse press event """
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """ Reimplements the mouse move event """
        return super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        """ Reimplements the mouse release event """
        return super().mouseReleaseEvent(event)