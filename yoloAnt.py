"""
    yoloAnt.py
"""

import sys
from enum import Enum

from PyQt6 import QtCore
from PyQt6.QtGui import QCursor, QIcon
from PyQt6.QtCore import QObject, QEvent
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow

from yoloAnt_ui import Ui_MainWindow

from pages.startPage import StartPage
from pages.projectPage import ProjectPage
from pages.annotationPage import AnnotationPage
from pages.machineLearningPage import MachineLearningPage

from dialogs.infoDialog import InfoDialog

from events.hoverEvent import HoverEvent


class Pages(Enum):
    """ Enum to represent the pages within the application"""
    StartPage=0
    AnnotationPage=1
    ProjectPage=2
    MachineLearningPage=3


class YoloAnt(QMainWindow):
    """
        Class that creates the yoloant application
    """
    def __init__(self) -> None:
        """ init """
        super().__init__()

        self.ui = Ui_MainWindow()
        
        self.ui.setupUi(self)
        
        # Setting up some member variables
        self.currentPage = Pages.StartPage
        self.project = None
        
        # Connecting signals and slots for the application
        self.__connectNavigationButtons()
        self.__connectIconHover()
        self.__connectRemainingButtons()

        self.startPage = StartPage(self)
        self.annotationPage = AnnotationPage(self)

        self.show()
    
    def __connectNavigationButtons(self) -> None:
        """ Connects the navigation buttons to update the current page of the stacked widget and updates checked state """
        # updates stacked widget index
        self.ui.annotTabBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))    
        self.ui.projectsTabBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))    
        self.ui.mlTabBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(3))

        # updates the state of the navigation buttons
        self.ui.annotTabBtn.clicked.connect(lambda: self.__updateStateOfNavigationButtons(Pages.AnnotationPage))
        self.ui.projectsTabBtn.clicked.connect(lambda: self.__updateStateOfNavigationButtons(Pages.ProjectPage))
        self.ui.mlTabBtn.clicked.connect(lambda: self.__updateStateOfNavigationButtons(Pages.MachineLearningPage)) 

    def __updateStateOfNavigationButtons(self, page: Pages) -> None:
        """ Updates the state of the navigation buttons """
        if(page is Pages.AnnotationPage):
            self.currentPage = Pages.AnnotationPage
            # Because of hover event, update check and also icon TODO: explore a cleaner alternative to checking / unchecking
            self.ui.annotTabBtn.setChecked(True)
            self.ui.projectsTabBtn.setChecked(False)
            self.ui.projectsTabBtn.setIcon(QIcon("icons/icons8-project-50.png"))
            self.ui.mlTabBtn.setChecked(False)
            self.ui.mlTabBtn.setIcon(QIcon("icons/icons8-ant-head-50.png"))
            self.ui.infoBtn.setChecked(False)
            self.ui.infoBtn.setIcon(QIcon("icons/icons8-information-50.png"))
        elif(page is Pages.ProjectPage):
            self.currentPage = Pages.ProjectPage
            self.ui.projectsTabBtn.setChecked(True)
            self.ui.annotTabBtn.setChecked(False)
            self.ui.annotTabBtn.setIcon(QIcon("icons/icons8-pencil-50.png"))
            self.ui.mlTabBtn.setChecked(False)
            self.ui.mlTabBtn.setIcon(QIcon("icons/icons8-ant-head-50.png"))
            self.ui.infoBtn.setChecked(False)
            self.ui.infoBtn.setIcon(QIcon("icons/icons8-information-50.png"))
        elif(page is Pages.MachineLearningPage):
            self.currentPage = Pages.MachineLearningPage
            self.ui.mlTabBtn.setChecked(True)
            self.ui.annotTabBtn.setChecked(False)
            self.ui.annotTabBtn.setIcon(QIcon("icons/icons8-pencil-50.png"))
            self.ui.projectsTabBtn.setChecked(False)
            self.ui.projectsTabBtn.setIcon(QIcon("icons/icons8-project-50.png"))
            self.ui.infoBtn.setChecked(False)
            self.ui.infoBtn.setIcon(QIcon("icons/icons8-information-50.png"))

    def __connectRemainingButtons(self) -> None:
        """ Connects the info button """
        self.ui.infoBtn.clicked.connect(lambda: self.__handleInfoDialog(True))

    def __handleInfoDialog(self, displayInfoDialog: bool) -> None:
        """ Handles the display of the info dialog box"""
        self.infoDialog = InfoDialog()
        
        if(displayInfoDialog and not self.infoDialog.isVisible()):
            self.infoDialog.exec()    

    def __connectIconHover(self) -> None:
        """ 
            Installs the hover event filter onto the application navigation buttons
            and updates the cursor icon on hover.
        """
        # Applying hover event and cursor change to annotTabBtn
        self.ui.annotTabBtn.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.annotTabHoverEvent = HoverEvent(self.ui.annotTabBtn, "icons/icons8-pencil-50.png", "icons/icons8-pencil-50-selected.png")
        self.ui.annotTabBtn.installEventFilter(self.annotTabHoverEvent)

        # Applying hover event and cursor change to projectsTabBtn
        self.ui.projectsTabBtn.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.projectsTabHoverEvent = HoverEvent(self.ui.projectsTabBtn, "icons/icons8-project-50.png", "icons/icons8-project-50-selected.png")
        self.ui.projectsTabBtn.installEventFilter(self.projectsTabHoverEvent)

        # Applying hover event and cursor change to mlTabBtn
        self.ui.mlTabBtn.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.mlTabHoverEvent = HoverEvent(self.ui.mlTabBtn, "icons/icons8-ant-head-50.png", "icons/icons8-ant-head-50-selected.png")
        self.ui.mlTabBtn.installEventFilter(self.mlTabHoverEvent)

        # Applying hover event and cursor change to infoBtn
        self.ui.infoBtn.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.infoBtnEvent = HoverEvent(self.ui.infoBtn, "icons/icons8-information-50.png", "icons/icons8-information-50-selected.png")
        self.ui.infoBtn.installEventFilter(self.infoBtnEvent)

        # Applying hover event and cursor change to notificationBtn
        self.ui.notificationBtn.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.notificationBtnEvent = HoverEvent(self.ui.notificationBtn, "icons/icons8-notification-bell-30-inactive.png", "icons/icons8-notification-bell-30-active.png")
        self.ui.notificationBtn.installEventFilter(self.notificationBtnEvent)


def main() -> None:
    """
        main entry point
    """
    app = QApplication(sys.argv)
    YoloAnt()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()