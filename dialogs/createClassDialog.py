"""
    createClassDialog.py
"""

from PyQt6.QtWidgets import QDialog, QListWidget

from dialogs.ui.createClassDialog_ui import Ui_createClassDialog
from utils.classListWidget import ClassListWidget
from dialogs.colourSelectorDialog import getColour

class CreateClassDialog(QDialog):
    """
        Class that creates a dialog window to create a class
    """
    def __init__(self, classListWidget: QListWidget, numOfClasses) -> None:
        """ init """
        super().__init__()

        self.ui = Ui_createClassDialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Create Class")
        self.__setupStyleSheet()
        self.setModal(True)

        # Set default colour
        self.selectedColour = (65, 66, 64)
        self.classListWidget = classListWidget

        # Connect signals and slots
        self.ui.classColourBtn.clicked.connect(lambda: self.__selectColour())
        self.ui.createClassBtn.clicked.connect(lambda: self.createClass(numOfClasses))

        self.show()

    def __setupStyleSheet(self) -> None:
        """ Sets up style sheet of create class dialog """
        self.ui.classColourBtn.setStyleSheet("QPushButton{"
                                             "border-radius: 4px;"
                                             "background-color: rgb(138, 226, 52);"
                                             "border: 3px solid rgb(105, 105, 105);}"
                                             "QPushButton:hover{border-color: rgb(165, 165, 165)}")

        self.ui.createClassBtn.setStyleSheet("QPushButton{"
                                             "background-color: rgb(65, 66, 64);"
                                             "border : 1px solid;"
                                             "border-radius: 10px;"
                                             "border-color:  rgb(85, 87, 83);"
                                             "font: 75 bold 12pt 'Gotham Rounded';"
                                             "color: rgb(255, 255, 255);}"
                                             "QPushButton::hover{background-color : rgb(105, 105, 105);"
                                             "border : 1px solid rgb(105, 105, 105);}")

    def __selectColour(self) -> None:
        """ Gets the specified colour from the colour selector dialog """
        self.selectedColour = getColour(self.selectedColour)
        self.r, self.g, self.b = self.selectedColour
        self.ui.classColourBtn.setStyleSheet("QPushButton{"
                                             f"background-color: rgb({self.r}, {self.g}, {self.b});"
                                             "border-radius: 4px;"
                                             "border: 3px solid rgb(105, 105, 105)}"
                                             "QPushButton:hover{border-color: rgb(165, 165, 165)}")
        self.ui.classColourBtn.repaint()


    def __validateDialogInputs(self) -> bool:
        """
            Validates the text input for the dialog and returns the class name
        """
        className = self.ui.classNameLineEdit.text()

        # Validating input
        valid = True   
        if className == "":
            self.ui.classNameLineEdit.setStyleSheet("QLineEdit{"
                                                    "background-color: rgb(65, 66, 64);"
                                                    "color: rgb(255, 255, 255);"
                                                    "border : 1px solid red;}")
            valid = False
        else: 
            self.ui.classNameLineEdit.setStyleSheet("QLineEdit{"
                                                    "background-color: rgb(65, 66, 64);"
                                                    "color: rgb(255, 255, 255);}")

        if not valid:
            return
        
        self.className = className

        return True


    def createClass(self, numOfClasses) -> None:
        """ Creats a user specified class if inputs are valid """
        if self.__validateDialogInputs():
            self.classListWidget.addItemToListWidget(self.className, 0, numOfClasses, self.selectedColour)
            self.done(1)
