"""
    resizeEvent.py
"""

from PyQt6.QtCore import QObject, QEvent

class ResizeEvent(QObject):
    """
        Class to detect a resize event and enforce ratio
    """
    def __init__(self, object: QObject):
        super().__init__()
        self.object = object

    def eventFilter(self, object, event):
        if event.type() == QEvent.Type.Resize:
            if self.object.width() > self.object.height(): 
                self.object.resize(self.object.height(), self.object.height())
            # else:
            #     self.object.resize(self.object.height(), self.object.height())
            return True

        # Standard event processing
        return QObject.eventFilter(self, object, event)