"""
    notificationManagerDialog.py
"""

import yaml
from PyQt6 import QtCore
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QDialog

from dialogs.ui.notificationManager_ui import Ui_MainDialog


class NotificationManagerDialog(QDialog):
    """
        Class that creates a notification manager dialog to capture all of the dialogs
    """
    def __init__(self) -> None:
        """ init """
        super().__init__()

        self.ui = Ui_MainDialog()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)   
        # self.__updateUi()

        self.__populateWidgets()

        self.show()

    def __updateUi(self) -> None: 
         # setting style sheet
        self.ui.notificationListWidget.setStyleSheet("QListView::item"
                                  "{"
                                  "border : 1px solid; border-color: rgb(65, 66, 64); border-radius : 5px;"
                                  "}"
                                  )

    def __populateWidgets(self) -> None:
        """
            Populates widgets with notifications
        """
        pass
