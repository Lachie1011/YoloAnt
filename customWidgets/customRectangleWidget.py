"""
    customRectangleWidget.py
"""

from enum import Enum
from PyQt6.QtCore import Qt, QEvent, QPointF
from PyQt6.QtGui import QPixmap, QColor, QPen
from PyQt6.QtWidgets import QGraphicsRectItem, QGraphicsItem, QGraphicsEllipseItem


class CustomRectangleWidget(QGraphicsRectItem):
    """ A custom widget that reimplements QGraphicsRectItem """
    def __init__(self, x, y, width, height, scene):
        super().__init__(x, y, width, height)

        self.scene = scene

        # Handle definitions
        self.DIAMETER = 3  # technically you set a length and width for the ellipse but diameter
        self.X_BORDER = 3
        self.Y_BORDER = 3

        self.editable = False

    def itemChange(self, change, value):
        """ Reimplements the itemChange function """
        if change == QGraphicsItem.GraphicsItemChange.ItemSelectedChange:
            # TODO: check that item is in a selected state
            if(value):
                self.editable = True
                self.addHandles()
                print("Item is selected")
            else:
                self.editable = False
        return super().itemChange(change, value)

    def addHandles(self):
        """ Adds editable handles to the rectItem """
        # Creating top-left, top-right, bottom-left, bottom-right "handles"
        
        # mapped = self.mapToScene(self.x(), self.y())

        # topLeftHandle = QGraphicsEllipseItem(self.scenePos().x() - self.X_BORDER, self.scenePos().y() + self.Y_BORDER, self.DIAMETER, self.DIAMETER, self)
        # topRightHandle = QGraphicsEllipseItem(mapped.x() + self.rect().width() + self.X_BORDER, mapped.y() + self.Y_BORDER, self.DIAMETER, self.DIAMETER, self)
        # bottomLeftHandle = QGraphicsEllipseItem(mapped.x() - self.X_BORDER, mapped.y() - self.rect().height() - self.Y_BORDER, self.DIAMETER, self.DIAMETER, self)
        # bottomRightHandle = QGraphicsEllipseItem(mapped.x() + self.rect().width() + self.X_BORDER, mapped.y() - self.rect().height() - self.Y_BORDER, self.DIAMETER, self.DIAMETER, self)
        # # TODO: handle Constraints here

        print(self.scenePos().x())
        print(self.scenePos().y())

        print(self.pos().x())
        print(self.pos().y())

        print(self.x())
        print(self.y())

        # print(self.mapToScene(self.x(), self.y()))
        # print(self.mapToScene(self.x(), self.y()))
        # print(self.mapToScene(self.x(), self.y()))



        topLeftHandle = QGraphicsEllipseItem(self.scenePos().x(), self.scenePos().y(), 5, 5, self)
        # Adding handles to scene
        self.scene.addItem(topLeftHandle)
        # self.scene.addItem(topRightHandle)
        # self.scene.addItem(bottomLeftHandle)
        # self.scene.addItem(bottomRightHandle)

    def mousePressEvent(self, event):
        """ Reimplements the mouse press event """
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """ Reimplements the mouse move event """
        return super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        """ Reimplements the mouse release event """
        return super().mouseReleaseEvent(event)