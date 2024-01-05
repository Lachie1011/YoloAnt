"""
    notificationManagerDialog.py
"""

import yaml
from PyQt6 import QtCore
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtWidgets import QDialog, QListWidgetItem

from dialogs.notificationDialog import State
from dialogs.notificationDialog import NotificationLevel
from dialogs.ui.notificationManager_ui import Ui_MainDialog

from customWidgets.notificationListItemWidget import NotificationListItemWidget


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
        self.numberNotifications = 0
        self.expanded = False
        self.minimised = True

        self.doNotDisturb = False

        self.__updateUi()

        self.__connectCloseBtn()
        self.__connectClearNotifsBtn()
        self.__connectDoNotDisturbBtn()

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
        self.ui.clearNotifsBtn.setStyleSheet("QPushButton::hover"
                                        "{"
                                        "background-color : #61635e;"
                                        "border-radius: 20px;"
                                        "}")

    def __connectClearNotifsBtn(self) -> None:
        """ Connects the clear notifs btn """
        self.ui.clearNotifsBtn.clicked.connect(lambda: self.clearNotifications())

    def clearNotifications(self): 
        """ Clears all notifications """
        self.ui.notificationListWidget.clear()
        self.numberNotifications = 0

    def __connectCloseBtn(self) -> None:
        """ Connects the notification manager close btn """
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

    def addNotification(self, notification: str, level: NotificationLevel) -> None:
        """ Adds a notification to the list widget """
        # Updating notification header
        self.numberNotifications = self.numberNotifications + 1
        self.ui.notificationLbl.setText("NOTIFICATIONS")

        # Creating custom widget to add to list
        notificationListItem = NotificationListItemWidget(notification, level)
        notificationListItemWidget = QListWidgetItem(self.ui.notificationListWidget)
        notificationListItemWidget.setSizeHint(notificationListItem.sizeHint())

        self.ui.notificationListWidget.addItem(notificationListItemWidget)
        self.ui.notificationListWidget.setItemWidget(notificationListItemWidget, notificationListItem)

    def showNotificationManager(self) -> None:
        """ Shows the notification manager """
        if self.numberNotifications > 0:
            self.ui.notificationLbl.setText("NOTIFICATIONS")
        
        if self.numberNotifications == 0:
            self.ui.notificationLbl.setText("NO NEW NOTIFICATIONS")
        
        self.show()