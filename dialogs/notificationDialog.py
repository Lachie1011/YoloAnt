"""
    notificationDialog.py
"""

import time
from enum import Enum
from datetime import datetime
from PyQt6.QtWidgets import QDialog

from dialogs.ui.notificationDialog_ui import Ui_MainDialog


class NotificationLevel(Enum):
    """ Enum to represent levels of notification"""
    Info=0
    Warning=1
    Error=2


class State(Enum):
    """ Enum to represent the state of the notification """
    Inactive=0
    Active=1


class NotificationDialog(QDialog):
    """
        Class that creates a dialog window to inform user of information about YoloAnt
    """
    def __init__(self, text: str, notifLevel: NotificationLevel = NotificationLevel.Info) -> None:
        """ init """
        # We dont show the notification on init
        super().__init__()

        self.ui = Ui_MainDialog()
        self.ui.setupUi(self)

        self.shown = False
        self.state = State.Inactive
        self.notificationTime = time.time()

        self.text = text
        self.notificationLevel = notifLevel

        self.__populateWidgets()

    def __populateWidgets(self) -> None:
        """
            Populates the widgets text and colout
        """
        self.ui.notificationLbl.setText(f"[{datetime.now()}]  " + self.text)
        backgroundColour = "#0096FF"
        if self.notificationLevel == NotificationLevel.Warning:
            backgroundColour = "#FFC300"
        if self.notificationLevel == NotificationLevel.Error: 
            backgroundColour = "#C70039"

        self.ui.colourLbl.setStyleSheet(f"background-color : {backgroundColour};")