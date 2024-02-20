"""
    image.py
"""

from path import Path

class Image():
    """ A class to abstractly represent an image """
    def __init__(self, imagePath) -> None:
        self.path = imagePath
        
        self.isValid = True
        
        # Image related attributes
        self.imageDim = None

        # Annotation related values
        self.annotated = False
        self.needsWork = False

        self.createMetadata()
    
    def createMetadata(self) -> None:
        """ Creates basic metadata for the image""" 
        if not Path(self.imagePath).is_File():
            return
        
        
        
