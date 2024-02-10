"""
    customEllipseGraphicsItem.py
"""

from PyQt6.QtCore import Qt, QEvent, QPointF, QPoint
from PyQt6.QtGui import QPixmap, QColor, QPen, QBrush
from PyQt6.QtWidgets import QGraphicsRectItem, QGraphicsItem, QGraphicsEllipseItem


class CustomEllipseGraphicsItem(QGraphicsEllipseItem):
    """ A custom graphics item that reimplements QGraphicsEllipseItem """
    def __init__(self, x, y, width, height, parent, classColour):
        super().__init__(x, y, width, height, parent)

        self.classColour = classColour

        # Filling the handle
        self.setBrush(QBrush(self.classColour, style = Qt.BrushStyle.SolidPattern))

        # Setting flags
        self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsMovable | QGraphicsItem.GraphicsItemFlag.ItemIsSelectable | QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)

    def itemChange(self, change, value):
        """ Reimplements the itemChange function """
        if change == QGraphicsItem.GraphicsItemChange.ItemSelectedChange:
            if(value):
                self.parent.handleSelected = True

        return super().itemChange(change, value)