"""
    yoloAnt.py
"""

import sys
from enum import Enum
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt6.QtGui import QCursor
from PyQt6 import QtCore
from PyQt6.QtCore import QObject, QEvent

from yoloAnt_ui import Ui_MainWindow

from pages.startPage import StartPage
from pages.projectPage import ProjectPage
from pages.annotationPage import AnnotationPage
from pages.machineLearningPage import MachineLearningPage

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
        self.__connectIconHoverFunc()

        self.startPage = StartPage(self)
        self.annotationPage = AnnotationPage(self)

        self.show()
    
    def __connectNavigationButtons(self) -> None:
        """ Connects the navigation buttons to update the current page of the stacked widget """
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
            self.ui.projectsTabBtn.setChecked(False)
            self.ui.mlTabBtn.setChecked(False)
        elif(page is Pages.ProjectPage):
            self.currentPage = Pages.ProjectPage
            self.ui.annotTabBtn.setChecked(False)
            self.ui.mlTabBtn.setChecked(False)
        elif(page is Pages.MachineLearningPage):
            self.currentPage = Pages.MachineLearningPage
            self.ui.annotTabBtn.setChecked(False)
            self.ui.projectsTabBtn.setChecked(False)

    def __connectIconHoverFunc(self) -> None:
        """ 
            Installs the hover event filter onto navigation btns and
            updates the cursor icon on hover
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


def main() -> None:
    """
        main entry point
    """
    app = QApplication(sys.argv)
    YoloAnt()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()