"""
    annotationCanvasWidget.py
"""

from PyQt6.QtGui import QPixmap, QPixmap, QPainter, QPen, QColor
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout


class AnnotationCanvasWidget(QWidget):
    """ A custom widget for the annotation canvas used for drawing bounding boxes """
    def __init__(self, parent=None):
        super(AnnotationCanvasWidget, self).__init__(parent)

        # Members
        self.currentImagePath = None  # TODO: update as a list of images? 
        self.currentImagePath = "/home/lachie/extractedImages/1029.jpg"

        # Constructing the widget
        self.canvasLabel = QLabel()

        # Construcing the layout
        self.canvasLayout = QHBoxLayout()
        self.canvasLayout.addWidget(self.canvasLabel)

        self.setLayout(self.canvasLayout)

        self.drawRectangle()

    def drawRectangle(self):
        """ A test class to draw rectangles on a label """
        # set rectangle color and thickness
        self.penRectangle = QPen(QColor(0, 0, 0))
        self.penRectangle.setWidth(3)
     
        # convert image file into pixmap
        self.pixmap_image = QPixmap(self.currentImagePath)

        # create painter instance with pixmap
        self.painterInstance = QPainter(self.pixmap_image)

        # draw rectangle on painter
        self.painterInstance.setPen(self.penRectangle)
        self.painterInstance.drawRect(0, 0, 500, 500)

        # set pixmap onto the label widget
        self.canvasLabel.setPixmap(self.pixmap_image)
