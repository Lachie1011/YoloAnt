"""
    notifier.py
    A class that manages and raises notifications within yoloAnt
"""

import time

from PyQt6 import QtCore

from dialogs.notificationDialog import State
from dialogs.notificationDialog import NotificationDialog
from dialogs.notificationDialog import NotificationLevel
from dialogs.notificationManagerDialog import NotificationManagerDialog


class NotificationManager:
    """
        Creates a notifier object and sets up related functionality.
    """
    def __init__(self, app) -> None:
        """ init """
        self.app = app
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.__updateNotifications)
    
        self.notifcationManagerDialog = NotificationManagerDialog()

        self.notifications = []  # Notifications are reset per application start, TODO: may have persistence in future??

        self.timer.start(100)

    def __updateNotifications(self) -> None:
        """ Iterates through notifications and closes / raises appropriately """
        for notification in self.notifications:
            # Always bring forward new notifications. The shown var is used to indicate if it is a new notif
            if notification.shown == False:
                # Only one notification can exist at a time
                self.closeNotifications()
                self.__showNotification(notification)
                break
            
            # Closing notifications after 5 seconds. TODO: maybe a setting?
            if notification.persistent:
                return

            delta = time.time() - notification.notificationTime
            if ((delta > 5) and (notification.state == State.Active)):
                notification.state = State.Inactive
                notification.close()

    def __showNotification(self, notification) -> None:
        """ Function to show a notification in either the manager or individually """
        notification.shown = True
        notification.state = State.Active
        self.notifcationManagerDialog.addNotification(notification.time + notification.text, notification.notificationLevel)
        self.resizeNotificationManger()

        if self.notifcationManagerDialog.state == State.Inactive:
            notification.show()        

    def calculateNotificationGeometry(self, notification) -> tuple:
        """ Calculates the geometry for a notification based off the application windoe """
        x = self.app.x() + self.app.ui.centralwidget.width() - notification.width()
        y = self.app.y() + self.app.ui.centralwidget.height() - notification.height()
        width = notification.width()
        height = notification.height()
        return x, y, width, height

    def raiseNotification(self, text: str, notifLevel: NotificationLevel = NotificationLevel.Info, persistent: bool = False) -> None:
        """ Raises a notifcation with a specified notification level, defaulting to info """
        notification = NotificationDialog(text, notifLevel, persistent)
        x, y, width, height = self.calculateNotificationGeometry(notification)
        notification.setGeometry(x, y, width, height)
        self.notifications.append(notification)

    def resizeNotifications(self) -> None: 
        """ Resize all notifications based off of the application's geometry """
        if self.notifcationManagerDialog.state == State.Active:
            x, y, width, height = self.calculateNotificationGeometry(self.notifcationManagerDialog)
            self.notifcationManagerDialog.setGeometry(x, y, width, height)
            # return as only the manager or a notification can be present at a time
            return

        for notification in self.notifications: 
            if notification.state == State.Active:
                x, y, width, height = self.calculateNotificationGeometry(notification)
                notification.setGeometry(x, y, width, height)

    def resizeNotificationManger(self):
        """ Function to resize the notification manager """
        HEIGHT_PADDING = 200
        if (self.notifcationManagerDialog.numberNotifications > 0) and (self.notifcationManagerDialog.expanded == False):
            # sets geometry up for manager
            x, y, width, height = self.calculateNotificationGeometry(self.notifcationManagerDialog)
            self.notifcationManagerDialog.setGeometry(x, y - HEIGHT_PADDING, width, height + HEIGHT_PADDING)
            self.notifcationManagerDialog.expanded = True
            self.notifcationManagerDialog.minimised = False

        elif self.notifcationManagerDialog.numberNotifications == 0 and self.notifcationManagerDialog.minimised == False:
            # sets geometry up for manager
            x, y, width, height = self.calculateNotificationGeometry(self.notifcationManagerDialog)
            self.notifcationManagerDialog.setGeometry(x, y + HEIGHT_PADDING, width, height - HEIGHT_PADDING)
            self.notifcationManagerDialog.minimised = True
            self.notifcationManagerDialog.expanded = False

        else:
            x, y, width, height = self.calculateNotificationGeometry(self.notifcationManagerDialog)
            self.notifcationManagerDialog.setGeometry(x, y, width, height)
  
    def openNotificationManager(self):
        """ Opens the notification viewer and applys geometry updates similar to notifs """
        # close any existing notification
        self.closeNotifications()

        self.resizeNotificationManger()

        self.notifcationManagerDialog.state = State.Active
        self.notifcationManagerDialog.showNotificationManager()

    def closeNotifications(self):
        """ Closes all notifications """
        for notification in self.notifications:
            notification.state = State.Inactive
            notification.close()