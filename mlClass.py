"""
    mlClass.py
"""


class MLClass():
    """ A class to abstractly represent a class for ML """
    def __init__(self, className, classColour) -> None:
        self.className = className
        self.classColour = classColour
       
        self.isValid = True

    def isValid(self) -> bool:
        """ Is valid function """
        return True
