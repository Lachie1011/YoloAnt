"""
    annotationCanvasWidget.py
"""

from PyQt6.QtCore import Qt
from PyQt6.QtCore import QPoint, QRect
from PyQt6.QtGui import QPixmap, QPixmap, QPainter, QPen, QColor, QCursor
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QGraphicsView, QGraphicsScene


class AnnotationCanvasWidget(QGraphicsView):
    """ A custom widget for the annotation canvas used for drawing bounding boxes """
    def __init__(self, parent):
        super(AnnotationCanvasWidget, self).__init__(parent)

        # Members
        self.rectBegin = QPoint()
        self.rectEnd = QPoint()
        self.currentImagePath = "/home/lachie/extractedImages/1029.jpg"  #TODO: this will need to be on each new image 

        # Setting alignment
        self.setAlignm

        # Creating the graphics view and scene
        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush(QColor(255,255,255))

        self.setScene(self.scene)

    # def paintEvent(self, event):
    #     """ A paint event to draw rectangles """
    #     # Update image pixmap to reset canvas
    #     self.pixmap_image = QPixmap(self.currentImagePath)
        
    #     # Create painter instance with pixmap
    #     painterInstance = QPainter(self.pixmap_image)

    #     # Draw rectangle on painter
    #     painterInstance.setPen(self.penRectangle)
    #     painterInstance.drawRect(QRect(self.rectBegin, self.rectEnd))

    #     # Set pixmap onto the label widget
    #     self.canvasLabel.setPixmap(self.pixmap_image)

    # self.scene.addRect(-0,-0, 200,200)

    def mousePressEvent(self, event):
        """ Event to capture mouse press and update rect coords """
        self.rectBegin = self.mapToScene(event.pos())
        self.rectEnd = self.mapToScene(event.pos())

    def mouseMoveEvent(self, event):
        """ Event to capture mouse move and update rect coords """
        self.rectEnd = self.mapToScene(event.pos())
        self.scene.clear()
        print(self.rectBegin.x())
        print(self.rectBegin.y())
        print(self.rectEnd.x())
        print(self.rectEnd.y())
        print("width: " + str(abs(self.rectEnd.x() - self.rectBegin.x())))
        print("height: " + str(abs(self.rectEnd.y() - self.rectBegin.y())))


        self.scene.addRect(self.rectBegin.x(), self.rectBegin.y(), abs(self.rectEnd.x() - self.rectBegin.x()), abs(self.rectEnd.y() - self.rectBegin.y()))

    def mouseReleaseEvent(self, event):
        """ Event to capture mouse release and update rect coords """
        self.rectEnd = self.mapToScene(event.pos())
        self.scene.clear()
        self.scene.addRect(self.rectBegin.x(), self.rectBegin.y(), abs(self.rectEnd.x() - self.rectBegin.x()), abs(self.rectEnd.y() - self.rectBegin.y()))
