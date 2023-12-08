"""
    notifier.py
    A class that manages and raises notifications within yoloAnt
"""

import time

from PyQt6 import QtCore

from dialogs.notificationDialog import State
from dialogs.notificationDialog import NotificationDialog
from dialogs.notificationDialog import NotificationLevel

class NotificationManager:
    """
        Creates a notifier object and sets up related functionality.
    """
    def __init__(self) -> None:
        """ init """
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
        self.notifications.append(notification)
    
    def __closeNotifications(self):
        """ Closes all notifications """
        for notification in self.notifications:
            notification.close()