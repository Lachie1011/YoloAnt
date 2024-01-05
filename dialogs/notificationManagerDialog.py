"""
    notificationManagerDialog.py
"""

import yaml
from PyQt6 import QtCore
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog

from dialogs.notificationDialog import State
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

        self.state = State.Inactive

        self.doNotDisturb = False

        self.__updateUi()

        self.__connectCloseBtn()
        self.__connectDoNotDisturbBtn()

        # self.show()

    def __updateUi(self) -> None:
        """ Updates stylesheets on the dialog"""
        # Adding hover stylesheet to both do not disturb and hide buttons
        self.ui.doNotDisturbBtn.setStyleSheet("QPushButton::hover"
                                        "{"
                                        "background-color : #61635e;"
                                        "border-radius: 20px;"
                                        "}")

        self.ui.hideBtn.setStyleSheet("QPushButton::hover"
                                        "{"
                                        "background-color : #61635e;"
                                        "border-radius: 20px;"
                                        "}")

        # styling for the list widget items
        # self.ui.notificationListWidget.setStyleSheet("QListView::item"
        #                           "{"
        #                           "border : 1px solid; border-color: rgb(65, 66, 64); border-radius : 5px;"
        #                           "}"
        #                           )

    def __connectCloseBtn(self) -> None:
        """ Connects the notification manager close functionality """
        self.ui.hideBtn.clicked.connect(lambda: self.__closeNotificationManager())

    def __closeNotificationManager(self) -> None:
        """ Closes the dialog """
        self.state = State.Inactive
        self.close()

    def __connectDoNotDisturbBtn(self) -> None:
        """ Connects the do not disturb button """
        self.ui.doNotDisturbBtn.clicked.connect(lambda: self.__toggleDoNotDisturb())
    
    def __toggleDoNotDisturb(self) -> None:
        """ Toggles the do not disturb state of dialog"""
        self.doNotDisturb = not self.doNotDisturb

        # updating icon
        if self.doNotDisturb: 
            self.ui.doNotDisturbBtn.setIcon(QIcon("dialogs/ui/icons/icons8-do-not-disturb-30.png"))
        else: 
            self.ui.doNotDisturbBtn.setIcon(QIcon("dialogs/ui/icons/icons8-notification-bell-30-inactive.png"))

        print(self.doNotDisturb)

