"""
    annotationCanvasWidget.py
"""

from pathlib import Path
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QColor, QPen
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsItem

from boundingBox import BoundingBox
from pages.annotationPage import Tools
from customWidgets.customRectangleGraphicsItem import CustomRectangleGraphicsItem


class AnnotationCanvasWidget(QGraphicsView):
    """ A custom widget for the annotation canvas used for drawing bounding boxes """
    def __init__(self, parent):
        super(AnnotationCanvasWidget, self).__init__(parent)

        # Attributes
        self.rectBegin = None
        self.rectEnd = None
        self.boundingBoxes = []
        self.imagePath = None  #TODO: this will need to be on each new image

        # Annotation canvas attributes
        self.mode = Tools.mouseTool
        self.currentClassName = ""
        self.currentClassColour = QColor(0,0,0)

        # Setting alignment
        self.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        # Creating the graphics scene
        self.scene = QGraphicsScene()

        # Scene is bound to graphics view geometry
        self.scene.setSceneRect(self.x(), self.y(), self.width(), self.height())
        self.scene.setBackgroundBrush(QColor(255,255,255))

        # Creating initial canvas
        self.imagePixmap = QPixmap()
        self.imageItem = QGraphicsPixmapItem(self.imagePixmap)
        self.scene.addItem(self.imageItem)
        
        self.setScene(self.scene)
    
    def updateImage(self, imagePath) -> None:
        """ Updates the image currently being shown as a QGraphicsPixmapItem """
        # if we do not have an image, just show the canvas
        if not Path(imagePath).is_file():
            return
        self.imagePixmap = QPixmap(imagePath)
        self.resetScene()

    def resetScene(self):
        """ Resets the scene environment """
        # Clearing the scene of all the rectangles that dont need to be there
        self.scene.clear()

        # Adding the image item back immediately after clearing
        self.imageItem = QGraphicsPixmapItem(self.imagePixmap)
        self.scene.addItem(self.imageItem)
        
        # Adding stored rectangles back to the canvas
        for boundingBox in self.boundingBoxes:
            self.createRect(boundingBox.x, boundingBox.y, boundingBox.width, boundingBox.height, False, boundingBox.colour)

    def createRect(self, x: float, y: float, width: float, height: float, store: bool, colour):
        """ Creates a rectangle based on mouse location and adds the rectangle to the scene """
        # Creating the rectangle
        # rect = self.scene.addRect(x, y, width, height)
        rect = CustomRectangleGraphicsItem(x, y, width, height, self.scene, colour)
        self.scene.addItem(rect)

        if store:
            boundingBox = BoundingBox(x, y, width, height, self.currentClassColour)
            self.boundingBoxes.append(boundingBox)

    def mousePressEvent(self, event):
        """ Event to capture mouse press and update rect coords """
        super(AnnotationCanvasWidget, self).mousePressEvent(event)
        self.rectBegin = self.mapToScene(event.pos())
        self.rectEnd = self.mapToScene(event.pos())

    def mouseMoveEvent(self, event):
        """ Event to capture mouse move and update rect coords """
        super(AnnotationCanvasWidget, self).mouseMoveEvent(event)
        self.rectEnd = self.mapToScene(event.pos())
        # Only add rectangle if in annotation mode
        if self.mode == Tools.annotationTool:
            self.resetScene()
            self.createRect(self.rectBegin.x(), self.rectBegin.y(), abs(self.rectEnd.x() - self.rectBegin.x()), abs(self.rectEnd.y() - self.rectBegin.y()), False, self.currentClassColour)

    def mouseReleaseEvent(self, event):
        """ Event to capture mouse release and update rect coords """
        super(AnnotationCanvasWidget, self).mouseReleaseEvent(event)
        self.rectEnd = self.mapToScene(event.pos())
        # Only add rectangle if in annotation mode
        if self.mode == Tools.annotationTool:
            self.resetScene()
            self.createRect(self.rectBegin.x(), self.rectBegin.y(), abs(self.rectEnd.x() - self.rectBegin.x()), abs(self.rectEnd.y() - self.rectBegin.y()), True, self.currentClassColour)

