"""
    annotationCanvasWidget.py
"""

from PyQt6.QtCore import Qt
from PyQt6.QtCore import QPoint, QRect
from PyQt6.QtGui import QPixmap, QPixmap, QPainter, QPen, QColor, QCursor
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout


class AnnotationCanvasWidget(QWidget):
    """ A custom widget for the annotation canvas used for drawing bounding boxes """
    def __init__(self, parent):
        super(AnnotationCanvasWidget, self).__init__(parent)

        # Members
        self.rectBegin = QPoint()
        self.rectEnd = QPoint()
        self.currentImagePath = "/home/lachie/extractedImages/1029.jpg"  #TODO: this will need to be on each new image 

        ## TO BE CHANGED
        self.pixmap_image = QPixmap(self.currentImagePath)

        # set rectangle color and thickness TODO: this will be based off of a class colour
        self.penRectangle = QPen(QColor(0, 0, 0))
        self.penRectangle.setWidth(3)
        ## END TO BE CHANGED

        # Constructing the widget
        self.canvasLabel = QLabel()
        self.canvasLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.canvasLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Construcing the layout
        self.canvasLayout = QHBoxLayout()
        self.canvasLayout.addWidget(self.canvasLabel)

        self.setLayout(self.canvasLayout)

    def paintEvent(self, event):
        """ A paint event to draw rectangles """
        # Update image pixmap to reset canvas
        self.pixmap_image = QPixmap(self.currentImagePath)
        
        # Create painter instance with pixmap
        painterInstance = QPainter(self.pixmap_image)

        # Draw rectangle on painter
        painterInstance.setPen(self.penRectangle)
        painterInstance.drawRect(QRect(self.rectBegin, self.rectEnd))

        # Set pixmap onto the label widget
        self.canvasLabel.setPixmap(self.pixmap_image)

    def mousePressEvent(self, event):
        """ Event to capture mouse press and update rect coords """
        self.rectBegin = event.pos()
        self.rectEnd = event.pos()
        self.update()

    def mouseMoveEvent(self, event):
        """ Event to capture mouse move and update rect coords """
        self.rectEnd = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        """ Event to capture mouse release and update rect coords """
        self.rectBegin = event.pos()
        self.rectEnd = event.pos()
        self.update()
