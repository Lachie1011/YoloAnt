"""
    customEllipseGraphicsItem.py
"""

from enum import Enum
from PyQt6.QtCore import Qt, QEvent, QPointF, QPoint
from PyQt6.QtGui import QPixmap, QColor, QPen, QBrush
from PyQt6.QtWidgets import QGraphicsRectItem, QGraphicsItem, QGraphicsEllipseItem


class Handles(Enum):
    """ An enum to define the possible handles used for a bouding box"""
    topLeft=0
    topRight=1
    bottomLeft=2 
    bottomRight=3

class CustomEllipseGraphicsItem(QGraphicsEllipseItem):
    """ A custom graphics item that reimplements QGraphicsEllipseItem """
    def __init__(self, x, y, width, height, parent, classColour, handleType):
        super().__init__(x, y, width, height, parent)
        
        self.parent = parent
        self.classColour = classColour
        self.handleType = handleType  #TODO: make handleType an enum
        
        self.selected = False
        self.lastPos = self.pos()

        # Filling the handle
        self.setBrush(QBrush(self.classColour, style = Qt.BrushStyle.SolidPattern))

        # Setting flags
        self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsMovable | 
                        QGraphicsItem.GraphicsItemFlag.ItemIsSelectable | 
                        QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)

    def itemChange(self, change, value):
        """ Reimplements the itemChange function """
        if change == QGraphicsItem.GraphicsItemChange.ItemSelectedChange:
            # If the ellipse item has lost selection, inform the rect item by toggling its edit mode 
            if value:
                self.selected = True
            else:
                self.selected = False
                self.parent.toggleEditMode(False)
        
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            # Calculating the change in position
            dx = self.lastPos.x() - self.pos().x()
            dy = self.lastPos.y() - self.pos().y()
            self.lastPos = self.pos()
            # Update parents position wtr to the new position and handleType
            self.parent.updateRectangle(dx, dy, self.handleType)
        return super().itemChange(change, value)

    def mousePressEvent(self, event):
        """ Reimplements mouse press events for the ellipse item """
        self.selected = True
        return super().mousePressEvent(event)
   
    def mouseReleaseEvent(self, event):
        # now that the mouse has finished, reset positions
        self.parent.updateHandlePositions(self.handleType, True)
        self.setPos(0,0)
        self.lastPos = self.pos()
        return super().mouseReleaseEvent(event)

