
"""
    model.py
"""

from enum import Enum 

class States(Enum):
    """ Enum to represent the state of a model - trained / not trained / training """
    NOT_TRAINED = "Not trained"
    TRAINING = "Training"
    TRAINED = "Trained"


class Model():
    """
        Class to abstractly represent a machine learning model
    """
    def __init__(self, modelName) -> None:
        self.state = States.NOT_TRAINED 
        self.modelName = modelName
        self.modelType = "YoloV7"  # perhaps these can be defaulted via settings
        self.device = "CPU"
        self.dimensions = [480, 640]
        self.epochs = "100"
        self.batchSize = "64"
        self.workers = "8"

    def isValid(self) -> bool:
        """ Validates model """
        return True

