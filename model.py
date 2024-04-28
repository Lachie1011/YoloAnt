
"""
    model.py
"""


class Model():
    """
        Class to abstractly represent a machine learning model
    """
    def __init__(self, state, modelName, modelType, device, dimensions, epochs, batchSize, workers) -> None:
        self.state = state
        self.modelName = modelName
        self.modelType = modelType
        self.device = device
        self.dimensions = dimensions
        self.epochs = epochs
        self.batchSize = batchSize
        self.workers = workers

    def isValid(self) -> bool:
        """ Validates model """
        return True
        
