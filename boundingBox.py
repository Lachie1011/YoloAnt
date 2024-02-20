"""
    boundingBox.py
"""

from PyQt6.QtGui import QColor

class BoundingBox():
    """ A class to represent a bounding box and related metadata """
    def __init__(self, x: float, y: float, width: float, height: float, colour: QColor):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour  #TODO: in the future this should be a class label which is then mapped to a colour
