"""
    customRectangleGraphicsItem.py
"""

from PyQt6.QtCore import Qt, QEvent, QPointF, QPoint
from PyQt6.QtGui import QPixmap, QColor, QPen, QBrush
from PyQt6.QtWidgets import QGraphicsRectItem, QGraphicsItem, QGraphicsEllipseItem

from customWidgets.customEllipseGraphicsItem import CustomEllipseGraphicsItem


class CustomRectangleGraphicsItem(QGraphicsRectItem):
    """ A custom graphics item that reimplements QGraphicsRectItem """
    def __init__(self, x, y, width, height, scene, classColour):
        super().__init__(x, y, width, height)

        self.scene = scene
        self.classColour = classColour

        # Handle definitions
        self.DIAMETER = 12    # technically you set a length and width for the ellipse but diameter
        self.X_BORDER = 0
        self.Y_BORDER = 0

        self.editable = False

        # TODO: create a dict to hold all the handles and states
        # we will iter

        self.handles = []
        self.handleSelected = False

        # Setting pen
        self.rectPen = QPen()
        self.rectPen.setWidth(3)  #TODO: width could be read in via some config script
        self.rectPen.setColor(self.classColour)
        self.setPen(self.rectPen)

        # Setting flags
        self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsMovable | QGraphicsItem.GraphicsItemFlag.ItemIsSelectable | QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)

    def itemChange(self, change, value):
        """ Reimplements the itemChange function """
        if change == QGraphicsItem.GraphicsItemChange.ItemSelectedChange:
            if(value):
                self.editable = True
                self.addHandles()
            else:
                # TODO: if the item has lost selected, check that one of its handles has not been selected
                # loop through dict
                # if not handleSelected: 
                #     self.editable = False
                #     self.removeHandles()

        return super().itemChange(change, value)

    def addHandles(self):
        """ Adds editable handles to the rectItem """
        # If we already have handles dont add anymore TODO: fix warning when we already have handles

        # Creating top-left, top-right, bottom-left, bottom-right "handles"
        self.topLeftHandle = CustomEllipseGraphicsItem(self.rect().left() - self.X_BORDER - self.DIAMETER / 2, self.rect().top() - self.Y_BORDER - self.DIAMETER / 2, self.DIAMETER, self.DIAMETER, self, self.classColour)
        self.topRightHandle = CustomEllipseGraphicsItem(self.rect().right() + self.X_BORDER - self.DIAMETER / 2, self.rect().top() - self.Y_BORDER - self.DIAMETER / 2, self.DIAMETER, self.DIAMETER, self, self.classColour)
        self.bottomLeftHandle = CustomEllipseGraphicsItem(self.rect().left() - self.X_BORDER - self.DIAMETER / 2, self.rect().bottom() + self.Y_BORDER - self.DIAMETER / 2, self.DIAMETER, self.DIAMETER, self, self.classColour)
        self.bottomRightHandle = CustomEllipseGraphicsItem(self.rect().right() + self.X_BORDER - self.DIAMETER / 2, self.rect().bottom() + self.Y_BORDER - self.DIAMETER / 2, self.DIAMETER, self.DIAMETER, self, self.classColour)

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