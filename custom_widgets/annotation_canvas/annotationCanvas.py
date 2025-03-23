"""
    annotationCanvas.py
"""

from pathlib import Path
from PyQt6.QtCore import Qt, pyqtSignal as Signal
from PyQt6.QtGui import QPixmap, QColor, QPen
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsItem

from boundingBox import BoundingBox
from pages.annotationPage import Tools
from custom_widgets.annotation_canvas.customRectangleGraphicsItem import CustomRectangleGraphicsItem


class AnnotationCanvas(QGraphicsView):
    """ A custom widget for the annotation canvas used for drawing bounding boxes """
    # Signals
    new_annotation = Signal(BoundingBox)
    annotationSelectedSignal = Signal(str, int)

    def __init__(self, parent):
        super(AnnotationCanvas, self).__init__(parent)

        self.app = None  # TODO: wanted to avoid passing in app, but not sure how else to get the next annotation ID 

        # Attributes
        self.image = None
        self.rectBegin = None
        self.rectEnd = None
        self.imagePath = None
        self.rects = []  # QGraphicsRectItem list of bounding boxes

        # Annotation canvas attributes
        self.mode = Tools.mouseTool
        self.currentClassName = None
        self.currentClassColour = None

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
    
    def updateImage(self, image) -> None:
        """ Updates the image currently being shown as a QGraphicsPixmapItem """
        # Set up for new image
        self.image = image
        
        # Setup for new image
        if not Path(self.image.path).is_file():
            return
        self.imagePixmap = QPixmap(image.path)
        
        # Clear working rects
        self.rects = []

        # Create rectangles from bounding boxes
        for boundingBox in self.image.boundingBoxes:
            self.createRect(boundingBox.x, boundingBox.y, boundingBox.width, boundingBox.height, boundingBox.colour, boundingBox.className, boundingBox.id, True, True, True)

        self.resetScene()

    def resetScene(self):
        """ Resets the scene environment """
        # Clearing the scene of all the rectangles that dont need to be there
        for item in self.scene.items():
            if item not in self.rects and isinstance(item, CustomRectangleGraphicsItem):
                # Check that the item isnt a child item of the one of the rects
                self.scene.removeItem(item)

        # Adding the image item back immediately after clearing
        self.imageItem = QGraphicsPixmapItem(self.imagePixmap)
        self.imageItem.setZValue(-1)  # Make sure that this is always on the lowest z value
        self.scene.addItem(self.imageItem)
    
    def generateBoundingBoxes(self) -> None:
        """ Loops through all of the rectangles and stores bounding boxes. Update respective image object """
        if not self.image:
            return
        boundingBoxes = []
        for rect in self.rects:
            boundingBox = BoundingBox(rect.x() + rect.rect().x(),
                                      rect.y() + rect.rect().y(),
                                      rect.rect().width(),
                                      rect.rect().height(),
                                      rect.classColour,
                                      rect.className,
                                      rect.id)
            boundingBoxes.append(boundingBox)
        self.image.updateBoundingBoxes(boundingBoxes)

    def createRect(self, x: float, y: float, width: float, height: float, colour, className: str, id: int, store: bool, reload: bool, load: bool):
        """ Creates a rectangle based on mouse location and adds the rectangle to the scene """
        # Creating the rectangle
        rect = CustomRectangleGraphicsItem(x, y, width, height, self.scene, colour, className, id, self)
        rect.connectSignals(lambda className, id: self.annotationSelectedSignal.emit(className, id))

        self.scene.addItem(rect)
        if store:
            # Add rect to list
            self.rects.append(rect)
            if not load:
                # Dont emit new annotation when loading existing annotations
                self.new_annotation.emit(BoundingBox(rect.x() + rect.rect().x(),
                                          rect.y() + rect.rect().y(),
                                          rect.rect().width(),
                                          rect.rect().height(),
                                          rect.classColour,
                                          rect.className,
                                          rect.id))

    def selectAnnotation(self, id: str):
        """ Selects an annotation """
        rect = None
        for _rect in self.rects:
            _rect.setSelected(False)
            if str(_rect.id) == id:
                rect = _rect
        if rect:
            rect.setSelected(True)

    def removeAnnotation(self, id: str):
        """ Removes an annotation """
        rect = None
        for _rect in self.rects:
            if str(_rect.id) == id:
                rect = _rect
        if rect:
            self.scene.removeItem(rect)
            self.rects.remove(rect)
            self.generateBoundingBoxes()

    def hideAnnotation(self, id: str, hidden: bool):
        """ Hides an annotation """
        rect = None
        for _rect in self.rects:
            if str(_rect.id) == id:
                rect = _rect
        if rect:
            if hidden:
                rect.hide()
            else:
                rect.show()

    def mousePressEvent(self, event):
        """ Event to capture mouse press and update rect coords """
        super(AnnotationCanvas, self).mousePressEvent(event)
        self.rectBegin = self.mapToScene(event.pos())
        self.rectEnd = self.mapToScene(event.pos())

    def mouseMoveEvent(self, event):
        """ Event to capture mouse move and update rect coords """
        super(AnnotationCanvas, self).mouseMoveEvent(event)
        self.rectEnd = self.mapToScene(event.pos())
        # Only add rectangle if in annotation mode
        if self.mode == Tools.annotationTool:
            self.resetScene()
            self.createRect(self.rectBegin.x(),
                            self.rectBegin.y(),
                            abs(self.rectEnd.x() - self.rectBegin.x()),
                            abs(self.rectEnd.y() - self.rectBegin.y()),
                            self.currentClassColour,
                            self.currentClassName,
                            None,
                            False,
                            False,
                            False)

    def mouseReleaseEvent(self, event):
        """ Event to capture mouse release and update rect coords """
        super(AnnotationCanvas, self).mouseReleaseEvent(event)
        self.rectEnd = self.mapToScene(event.pos())
        # Only add rectangle if in annotation mode
        if self.mode == Tools.annotationTool:
            self.resetScene()
            self.createRect(self.rectBegin.x(),
                            self.rectBegin.y(),
                            abs(self.rectEnd.x() - self.rectBegin.x()),
                            abs(self.rectEnd.y() - self.rectBegin.y()),
                            self.currentClassColour,
                            self.currentClassName,
                            self.app.project.getNextAnnotationID(),
                            True,
                            False,
                            False)
 
        # update image reference to bounding box list 
        self.generateBoundingBoxes()