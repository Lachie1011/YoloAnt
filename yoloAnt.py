"""
    yoloAnt.py
"""

import sys
import signal
from dataclasses import dataclass

from PyQt6 import QtCore
from PyQt6.QtCore import QEvent
from PyQt6.QtGui import QIcon, QFontDatabase
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel

from ui.yoloAnt_ui import Ui_MainWindow
from pages.startPage import StartPage
from pages.projectPage import ProjectPage
from pages.annotationPage import AnnotationPage
from pages.machineLearningPage import MachineLearningPage

from dialogs.infoDialog import InfoDialog
from notificationManager import NotificationManager

from events.iconHoverAndCheckedEvent import IconHoverAndCheckedEvent

from theme import *

app = None

class Pages(Enum):
    """ Enum to represent the pages within the application"""
    StartPage=0
    AnnotationPage=1
    ProjectPage=2
    MachineLearningPage=3

@dataclass
class NavigationTab:
    button: QPushButton
    unselectedIconImagePath: str
    selectedIconImagePath: str
    unselectedIndicatorLabel: QLabel
    selectedIndicatorLabel: QLabel


class YoloAnt(QMainWindow):
    """
        Class that creates the yoloant application
    """
    def __init__(self, app) -> None:
        """ init """
        super().__init__()

        self.ui = Ui_MainWindow()
        
        self.ui.setupUi(self)
        
        # Setting up some member variables
        self.currentPage = Pages.StartPage
        self.project = None
        self.infoDialog = None

        # Set app colour palette
        self.theme = Theme()

        # Setup style sheet of application
        # self.__setupAppStyleSheet()
        self.__createNavigationButtonClasses()
        
        # Starting the notification manager
        self.notificationManager = NotificationManager(self)

        # Connecting signals and slots for the application
        self.__connectNavigationButtons()
        self.__connectIconHover()
        self.__connectInformationButton()
        self.__connectNotificationButton()

        self.__setupKeyBindings()

        # Add application font to database
        QFontDatabase.addApplicationFont(f"assets/fonts/{self.theme.colours['fontType.header']}")
        QFontDatabase.addApplicationFont(f"assets/fonts/{self.theme.colours['fontType.title']}")
        QFontDatabase.addApplicationFont(f"assets/fonts/{self.theme.colours['fontType.regular']}")
        self.fontTypeHeader = QFontDatabase.applicationFontFamilies(0)[0]
        self.fontTypeTitle = QFontDatabase.applicationFontFamilies(1)[1]
        self.fontTypeRegular = QFontDatabase.applicationFontFamilies(2)[1]
        
        # Creating pages        
        self.startPage = StartPage(self)
        self.projectPage = ProjectPage(self)
        self.annotationPage = AnnotationPage(self)
        self.machineLearningPage = MachineLearningPage(self)
        
        self.installEventFilter(self)

        #TODO: bind this to some setting
        # QResource.registerResource("icons.qrc")
        stylesheet_path = "themes/generated/dark_theme.qss"
        if os.path.exists(stylesheet_path):
            with open(stylesheet_path, "r") as f:
                qss = f.read()
                print("QSS Loaded:\n", qss)
                app.setStyleSheet(qss)

        print(self.ui.openProjectLbl.objectName())  # Should print "openProjectLbl"
        print(self.ui.openProjectLbl.styleSheet())  # Should be "" if not overridden in code
        self.ui.openProjectLbl.style().unpolish(self.ui.openProjectLbl)
        self.ui.openProjectLbl.style().polish(self.ui.openProjectLbl)
        self.ui.openProjectLbl.update()

        self.showMaximized()
        self.show()

    def eventFilter(self, object, event):
        """ Application level event filter """
        if event.type() == QEvent.Type.Resize or event.type() == QEvent.Type.Move:
            # resize notifications
            self.notificationManager.resizeNotifications()
            return False
        if event.type() == QEvent.Type.KeyPress:
            if event.modifiers() & QtCore.Qt.KeyboardModifier.ControlModifier and event.key() == QtCore.Qt.Key.Key_E:
                print(object)
        return False

    def closeEvent(self, event) -> None:
        """ Overrides the close event on the main window """
        # Save annotations
        if self.project:
            self.project.writeProject()
            self.project.writeClasses()
            self.project.writeModels()
            self.project.writeAnnotations()

        # Ensure all notifications are closed
        self.notificationManager.closeNotifications()
        # For now manually close info dialog TODO: have this close nicer
        if self.infoDialog:
            self.infoDialog.close()

        if self.notificationManager.notifcationManagerDialog:
            self.notificationManager.notifcationManagerDialog.close()
        event.accept()

    def __connectNavigationButtons(self) -> None:
        """ Connects the navigation buttons to update the current page of the stacked widget and updates checked state """
        # Connects the currentChanged signal for the stacked widget
        self.ui.stackedWidget.currentChanged.connect(self.__onPageChange)

        # Updates the state of the navigation buttons
        self.ui.annotTabBtn.clicked.connect(lambda: self.__updateStateOfNavigationButtons(Pages.AnnotationPage))
        self.ui.projectsTabBtn.clicked.connect(lambda: self.__updateStateOfNavigationButtons(Pages.ProjectPage))
        self.ui.mlTabBtn.clicked.connect(lambda: self.__updateStateOfNavigationButtons(Pages.MachineLearningPage))

    def __createNavigationButtonClasses(self) -> None:
        """ Initialises navigation tabs and creates associated data classes. """
        self.annotationTab = NavigationTab(
            self.ui.annotTabBtn,
            "icons/icons8-pencil-30.png",
            "icons/icons8-pencil-30-selected.png",
            self.ui.annotTabIndicatorLbl,
            self.ui.annotTabIndicatorSelectedLbl
        )
        self.ui.annotTabIndicatorSelectedLbl.setVisible(False)

        self.projectTab = NavigationTab(
            self.ui.projectsTabBtn,
            "icons/icons8-project-30.png",
            "icons/icons8-project-30-selected.png",
            self.ui.projectsTabIndicatorLbl,
            self.ui.projectsTabIndicatorSelectedLbl
        )
        self.ui.projectsTabIndicatorSelectedLbl.setVisible(False)

        self.mlTab = NavigationTab(
            self.ui.mlTabBtn,
            "icons/icons8-ant-head-30.png",
            "icons/icons8-ant-head-30-selected.png",
            self.ui.mlTabIndicatorLbl,
            self.ui.mlTabIndicatorSelectedLbl
        )
        self.ui.mlTabIndicatorSelectedLbl.setVisible(False)


    def __updateStateOfNavigationButtons(self, page: Pages) -> None:
        """ Updates the state of the navigation buttons """
        if not self.project:
            self.ui.stackedWidget.setCurrentIndex(Pages.StartPage.value)
            self.currentPage = Pages.StartPage
            self.__setNavigationTabToSelected(self.annotationTab, False)
            self.__setNavigationTabToSelected(self.projectTab, False)
            self.__setNavigationTabToSelected(self.mlTab, False)
            self.notificationManager.raiseNotification("No active project. Please open or create a new project.")
            return

        if page is Pages.AnnotationPage:
            self.ui.stackedWidget.setCurrentIndex(Pages.AnnotationPage.value)
            self.currentPage = Pages.AnnotationPage
            self.__setNavigationTabToSelected(self.annotationTab, True)
            self.__setNavigationTabToSelected(self.projectTab, False)
            self.__setNavigationTabToSelected(self.mlTab, False)
            self.annotationPage.loadPage()

        elif page is Pages.ProjectPage:
            self.ui.stackedWidget.setCurrentIndex(Pages.ProjectPage.value)
            self.currentPage = Pages.ProjectPage
            self.__setNavigationTabToSelected(self.annotationTab, False)
            self.__setNavigationTabToSelected(self.projectTab, True)
            self.__setNavigationTabToSelected(self.mlTab, False)
            self.projectPage.loadPage()

        elif page is Pages.MachineLearningPage:
            self.ui.stackedWidget.setCurrentIndex(Pages.MachineLearningPage.value)
            self.currentPage = Pages.MachineLearningPage
            self.__setNavigationTabToSelected(self.annotationTab, False)
            self.__setNavigationTabToSelected(self.projectTab, False)
            self.__setNavigationTabToSelected(self.mlTab, True)
            self.machineLearningPage.loadPage(None)

        self.ui.infoBtn.setChecked(False)
        self.ui.infoBtn.setIcon(QIcon("icons/icons8-information-30.png"))

    def __setNavigationTabToSelected(self, navigationTab: NavigationTab, isSelected: bool) -> None:
        """ Sets a navigation tab to selected state. """
        navigationTab.button.setChecked(isSelected)
        navigationTab.unselectedIndicatorLabel.setVisible(not isSelected)
        navigationTab.selectedIndicatorLabel.setVisible(isSelected)

        if not isSelected:
            navigationTab.button.setIcon(QIcon(navigationTab.unselectedIconImagePath))



    def __onPageChange(self) -> None:
        """ Resets some application attributes on a page change """
        # Reset cursor icon
        QApplication.restoreOverrideCursor() 

    def __connectInformationButton(self) -> None:
        self.ui.infoBtn.clicked.connect(lambda: self.__openInfoDialog(True))
    
    def __openInfoDialog(self, displayInfoDialog: bool) -> None:
        """ Handles the display of the info dialog box"""
        self.infoDialog = InfoDialog()        
        if(displayInfoDialog and not self.infoDialog.isVisible()):
            self.infoDialog.exec()    

    def __connectNotificationButton(self) -> None: 
        """ Connects the notification button """
        self.ui.notificationBtn.clicked.connect(lambda: self.__openNotificationManager())
    
    def __openNotificationManager(self) -> None:
        """ Opens the notification viewer """
        self.notificationManager.openNotificationManager()

    def __connectIconHover(self) -> None:
        """ Installs the hover event filter onto the application navigation buttons. """

        self.annotTabHoverEvent = IconHoverAndCheckedEvent(
            self.annotationTab.button,
            self.annotationTab.unselectedIconImagePath,
            self.annotationTab.selectedIconImagePath
        )
        self.ui.annotTabBtn.installEventFilter(self.annotTabHoverEvent)

        self.projectsTabHoverEvent = IconHoverAndCheckedEvent(
            self.projectTab.button,
            self.projectTab.unselectedIconImagePath,
            self.projectTab.selectedIconImagePath
        )
        self.ui.projectsTabBtn.installEventFilter(self.projectsTabHoverEvent)

        self.mlTabHoverEvent = IconHoverAndCheckedEvent(
            self.mlTab.button,
            self.mlTab.unselectedIconImagePath,
            self.mlTab.selectedIconImagePath
        )
        self.ui.mlTabBtn.installEventFilter(self.mlTabHoverEvent)

        self.infoBtnEvent = IconHoverAndCheckedEvent(
            self.ui.infoBtn,
            "icons/icons8-information-30.png",
            "icons/icons8-information-30-selected.png"
        )
        self.ui.infoBtn.installEventFilter(self.infoBtnEvent)

        self.notificationBtnEvent = IconHoverAndCheckedEvent(
            self.ui.notificationBtn,
            "icons/icons8-notification-bell-30-inactive.png",
            "icons/icons8-notification-bell-30-active.png"
        )
        self.ui.notificationBtn.installEventFilter(self.notificationBtnEvent)

    def __setupAppStyleSheet(self) -> None:
        """ Sets up the colour palette of the application """
        self.ui.menuBar.setStyleSheet(self.ui.menuBar.styleSheet() + f"background: {self.theme.colours['menu.background']};")
        self.ui.leftMenuSubContainer.setStyleSheet(self.ui.leftMenuSubContainer.styleSheet() + f"background: {self.theme.colours['navigationbar.background']};")
        self.ui.bottomBarFrame.setStyleSheet(self.ui.bottomBarFrame.styleSheet() + f"background: {self.theme.colours['navigationbar.background']};")
        self.ui.stackedWidget.setStyleSheet(self.ui.stackedWidget.styleSheet() + f"background: {self.theme.colours['app.background']};")
    
    def __toggleEditMode(self) -> None:
        """ Toggles the edit mode button """
        self.ui.editPageBtn.setChecked(not self.ui.editPageBtn.isChecked())

    def __setupKeyBindings(self) -> None:
        """ Sets up some keybindings for the application """
        # for the moment, hardcode these here - might be rebindable in some keybindings manager
        EDIT_SHORTCUT = "Ctrl+E"
        #self.editModeShortCut = QShortcut(QKeySequence(EDIT_SHORTCUT), self)
        #self.editModeShortCut.activated.connect(self.__toggleEditMode)

def signal_handler(sig, frame) -> None:
    """ Handles unix signals """
    # At the moment we are just worried about sigint and sigterm and both signals are handled the same
    global app
    app.exit(-1)  # Any non-typical exit is an error -1 


def main() -> None:
    """
        main entry point
    """ 
    
    # Handling application signals that are not handled by QT
    signal.signal(signal.SIGINT, signal_handler)  # SIGINT
    signal.signal(signal.SIGTERM, signal_handler)  # SIGTERM

    # Starting application
    global app  # Using a global reference for the signal handling - might be something better here
    app = QApplication(sys.argv)
    YoloAnt(app)
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
