"""
    notificationListItemWidget.py
"""

from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QPushButton

from dialogs.notificationDialog import NotificationLevel


class NotificationListItemWidget(QWidget):
    """ A custom class for the notification list item widget """
    def __init__(self, notificationText: str, notificationLevel: NotificationLevel, parent=None):
        super(NotificationListItemWidget, self).__init__(parent)

        # Constructing the widget
        self.notificationListItemWidgetLbl = QLabel(notificationText)
        self.notificationListItemWidgetBtn = QPushButton()
        self.notificationListItemWidgetBtn.setFixedSize(30, 30)

        # Applying styling
        backgroundColour = "#0096FF"
        if notificationLevel == NotificationLevel.Warning:
            backgroundColour = "#FFC300"
        if notificationLevel == NotificationLevel.Error: 
            backgroundColour = "#C70039"

        self.notificationListItemWidgetBtn.setStyleSheet(f"background-color: {backgroundColour};")

        self.classItemWidetLayout = QHBoxLayout()
        self.classItemWidetLayout.addWidget(self.notificationListItemWidgetLbl)
        self.classItemWidetLayout.addWidget(self.notificationListItemWidgetBtn)

        self.setLayout(self.classItemWidetLayout)
