"""
    image.py
"""

import os
import cv2


class Image():
    """ A class to abstractly represent an image """
    def __init__(self, imagePath, boundingBoxes = []) -> None:
        self.path = imagePath 
       
        self.isValid = True
        
        self.metadataCreated = False

        self.boundingBoxes = boundingBoxes
        
        # Image related attributes
        self.height = None
        self.width = None
        self.channels = None

        # Annotation related attributes
        self.annotated = False
        self.needsWork = False
        
        if self.boundingBoxes:
            self.annotated = True
    

    def updateBoundingBoxes(self, boundingBoxes) -> None:
        """ Updates list of bounding boxes """
        self.boundingBoxes = boundingBoxes

        if len(self.boundingBoxes) > 0:
            self.annotated = True

    def createMetadata(self) -> None:
        """ Creates basic metadata for the image"""
        
        if self.metadataCreated:
            return
    
        if not os.path.exists(self.path):
            print("not valid path")
            return

        image = cv2.imread(self.path) 
        if image is None:
            self.isValid = False
            return

        self.height, self.width, self.channels = image.shape
        self.metadataCreated = True

