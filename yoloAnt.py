"""
    yoloAnt.py
    WIP: main entry point for the yoloant application
"""

import sys
from enum import Enum
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow

from yoloAnt_ui import Ui_MainWindow

from pages.startPage import StartPage
from pages.projectPage import ProjectPage
from pages.annotationPage import AnnotationPage
from pages.machineLearningPage import MachineLearningPage


class Pages(Enum):
    """ Enum to represent the pages within the application"""
    StartPage=0
    AnnotationPage=1
    ProjectPage=2
    MachineLearningPage=3

class YoloAnt(QMainWindow):
    """
        Class that creates and runs the yoloant application
    """
    def __init__(self) -> None:
        """ init """
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Setting up some member variables
        self.currentPage = Pages.StartPage
        
        # Connecting signals and slots for the application
        self.__connectNavigationButtons()
        self.__connectIconHoverFunc()

        self.startPage = StartPage(self.ui)
        # Connecting signals and slots for the annotation page
        # Connecting signals and slots for the projects page
        # Connecting signals and slots for the machine learning page

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
        """ Connects the hover over functionality to icons """
        pass

def main() -> None:
    """
        main entry point
    """
    app = QApplication(sys.argv)
    main_window = YoloAnt()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()