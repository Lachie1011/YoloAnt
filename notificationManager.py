"""
    notifier.py
    A class that manages and raises notifications within yoloAnt
"""

import time

from PyQt6 import QtCore

from dialogs.notificationDialog import State
from dialogs.notificationDialog import NotificationDialog
from dialogs.notificationDialog import NotificationLevel

WIDTH_PADDING = 104
HEIGHT_PADDING = 35


class NotificationManager:
    """
        Creates a notifier object and sets up related functionality.
    """
    def __init__(self, app) -> None:
        """ init """
        self.app = app
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.__updateNotifications)
        self.notifications = []  # Notifications are reset per application start, TODO: may have persistence in future??

        self.timer.start(1000)

    def __updateNotifications(self):
        """ Iterates through notifications and closes / raises appropriately """
        for notification in self.notifications:
            # Always bring forward new notifications
            if notification.shown == False:
                # Only one notification can exist at a time
                self.__closeNotifications()
                # Set notification geometry to bottom right TODO: do resizing of notifications on resize event
                notification.show()
                notification.shown = True
                notification.state = State.Active
                break

            delta = time.time() - notification.notificationTime
            if ((delta > 5) and (notification.state == State.Active)):
                notification.state = State.Inactive
                notification.close()

    def raiseNotification(self, text: str, notifLevel: NotificationLevel = NotificationLevel.Info) -> None:
        """ Raises a notifcation with a specified notification level, defaulting to info """
        notification = NotificationDialog(text, notifLevel)
        notification.setGeometry(self.app.width() - notification.width() + WIDTH_PADDING, self.app.height() + notification.height() - HEIGHT_PADDING, notification.width(), notification.height())
        self.notifications.append(notification)
    
    def __closeNotifications(self):
        """ Closes all notifications """
        for notification in self.notifications:
            notification.close()