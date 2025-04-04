"""
    customRectangleGraphicsItem.py  
"""

from PyQt6.QtCore import Qt, QEvent, QPointF, QPoint, QRect, pyqtSignal as Signal
from PyQt6.QtGui import QPixmap, QColor, QPen, QBrush
from PyQt6.QtWidgets import QGraphicsRectItem, QGraphicsItem, QGraphicsEllipseItem

from custom_widgets.annotation_canvas.customEllipseGraphicsItem import CustomEllipseGraphicsItem, Handles


class CustomRectangleGraphicsItem(QGraphicsRectItem):
    """ A custom graphics item that reimplements QGraphicsRectItem """

    annotationSelectedSignal = Signal(str, str)
    def __init__(self, x, y, width, height, scene, classColour, className, id, canvas):
        super().__init__(x, y, width, height)

        self.scene = scene
        self.id = id
        self.classColour = classColour
        self.className = className
        self.canvas = canvas

        # Handle definitions
        self.DIAMETER = 12    # technically you set a length and width for the ellipse but diameter
        
        # Bounding box definitions
        self.X_BORDER = 0
        self.Y_BORDER = 0
        self.MIN_AREA = 1
        
        self.handles = []
        self.editable = False

        # Setting pen
        self.rectPen = QPen()
        self.rectPen.setWidth(3)  #TODO: width could be read in via some config script
        self.rectPen.setColor(self.classColour)
        self.setPen(self.rectPen)

        # Setting flags
        self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsMovable | 
                        QGraphicsItem.GraphicsItemFlag.ItemIsSelectable | 
                        QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        
    def itemChange(self, change, value):
        """ Reimplements the itemChange function """
        if change == QGraphicsItem.GraphicsItemChange.ItemSelectedChange:
            if(value):
                self.toggleEditMode(True)
                if hasattr(self, "onSelected"):
                    self.onSelected(self.className, self.id)
            else:
                self.toggleEditMode(False)

        return super().itemChange(change, value)

    def toggleEditMode(self, editable: bool) -> None:
        """ Reponsible for toggling the edit mode on a rectangle """
        if editable:
            self.editable = True
            self.addHandles()
        else:
            # Dont remove handles from rectangle just because it lost selection - a handle might be selected
            if self.handleIsSelected():
                return
            self.editable = False
            self.removeHandles()

    def updateRectangle(self, dx, dy, handle) -> None:
        """ Updates position and geometry of a rectangle based on a handle """
        x = self.rect().x()
        y = self.rect().y()
        width = self.rect().width()
        height = self.rect().height()        

        if handle == Handles.topLeft:
            x = self.rect().x() - dx
            y = self.rect().y() - dy
            width = self.rect().width() + dx
            height = self.rect().height() + dy            
        if handle == Handles.topRight:
            # x doesnt change
            y = self.rect().y() - dy
            width = self.rect().width() - dx
            height = self.rect().height() + dy 
        if handle == Handles.bottomLeft:
            x = self.rect().x() - dx
            # y doesnt change
            width = self.rect().width() + dx
            height = self.rect().height() - dy
        if handle == Handles.bottomRight:
            # x doesnt change
            # y doesnt change
            width = self.rect().width() - dx
            height = self.rect().height() - dy

        # constraints
        if (width * height) <= self.MIN_AREA:
            return

        self.setRect(x, y, width, height)
        self.updateHandlePositions(handle, False)
        # after position change update image annotations ref
        self.canvas.generateBoundingBoxes()

    def updateHandlePositions(self, handle, mouseUpdate) -> None:
        """ Handles updates to handle positions """
        if handle != Handles.topLeft or mouseUpdate:
            self.topLeftHandle.setRect(self.rect().left() - self.X_BORDER - self.DIAMETER / 2, 
                                        self.rect().top() - self.Y_BORDER - self.DIAMETER / 2, 
                                        self.DIAMETER, self.DIAMETER)
        if handle != Handles.topRight or mouseUpdate:
            self.topRightHandle.setRect(self.rect().right() + self.X_BORDER - self.DIAMETER / 2, 
                                         self.rect().top() - self.Y_BORDER - self.DIAMETER / 2, 
                                         self.DIAMETER, self.DIAMETER)
        if handle != Handles.bottomLeft or mouseUpdate:
            self.bottomLeftHandle.setRect(self.rect().left() - self.X_BORDER - self.DIAMETER / 2, 
                                          self.rect().bottom() + self.Y_BORDER - self.DIAMETER / 2, 
                                          self.DIAMETER, self.DIAMETER)
        if handle != Handles.bottomRight or mouseUpdate:
            self.bottomRightHandle.setRect(self.rect().right() + self.X_BORDER - self.DIAMETER / 2, 
                                           self.rect().bottom() + self.Y_BORDER - self.DIAMETER / 2, 
                                           self.DIAMETER, self.DIAMETER)

    def handleIsSelected(self) -> bool:
        """ Loops through all handles to determine if a handle has been selected """
        for handle in self.handles:
            if handle.selected:
                return True
        return False

    def addHandles(self) -> None:
        """ Adds editable handles to the rectItem """
        # Only add handles once
        if not self.handles:
            # Creating top-left, top-right, bottom-left, bottom-right handles, this also adds them to the scene
            self.topLeftHandle = CustomEllipseGraphicsItem(self.rect().left() - self.X_BORDER - self.DIAMETER / 2, 
                                                            self.rect().top() - self.Y_BORDER - self.DIAMETER / 2, 
                                                            self.DIAMETER, self.DIAMETER, self, self.classColour, Handles.topLeft)
            self.topRightHandle = CustomEllipseGraphicsItem(self.rect().right() + self.X_BORDER - self.DIAMETER / 2, 
                                                            self.rect().top() - self.Y_BORDER - self.DIAMETER / 2, 
                                                            self.DIAMETER, self.DIAMETER, self, self.classColour, Handles.topRight)
            self.bottomLeftHandle = CustomEllipseGraphicsItem(self.rect().left() - self.X_BORDER - self.DIAMETER / 2, 
                                                              self.rect().bottom() + self.Y_BORDER - self.DIAMETER / 2, 
                                                              self.DIAMETER, self.DIAMETER, self, self.classColour, Handles.bottomLeft)
            self.bottomRightHandle = CustomEllipseGraphicsItem(self.rect().right() + self.X_BORDER - self.DIAMETER / 2, 
                                                              self.rect().bottom() + self.Y_BORDER - self.DIAMETER / 2, 
                                                              self.DIAMETER, self.DIAMETER, self, self.classColour, Handles.bottomRight)
            # Appending handles to list to track
            self.handles.append(self.topLeftHandle)
            self.handles.append(self.topRightHandle)
            self.handles.append(self.bottomLeftHandle)
            self.handles.append(self.bottomRightHandle)
        
        # Show all the handles:
        for handle in self.handles:
            if not handle.isVisible():
                handle.show()
            
    def removeHandles(self) -> None:
        """ Removes handles from the rect item """
        for handle in self.handles:
            handle.hide()

    def connectSignals(self, onSelected):
        self.onSelected = onSelected