"""
    createClassDialog.py
"""

from PyQt6.QtWidgets import QDialog, QLabel, QListWidget, QHBoxLayout

from dialogs.ui.createClassDialog_ui import Ui_createClassDialog
from customWidgets.customQObjects import UserInputQLineEdit
from customWidgets.projectClassListItemWidget import ProjectClassListItemWidget
from dialogs.colourSelectorDialog import getColour

class CreateClassDialog(QDialog):
    """
        Class that creates a dialog window to create a class
    """
    def __init__(self, classListWidget: QListWidget, numOfClasses: int, themePaletteColours: dict, fontRegular: str, fontTitle: str) -> None:
        """ init """
        super().__init__()

        self.ui = Ui_createClassDialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Create Class")

        self.setModal(True)

        # Member variables
        self.selectedColour = (200, 66, 64)
        self.classListWidget = classListWidget
        self.themePaletteColours = themePaletteColours
        self.fontRegular = fontRegular
        self.fontTitle = fontTitle

        self.__setupStyleSheet()
        self.__setupPagePalette()

        # Connect signals and slots
        self.ui.classColourBtn.clicked.connect(lambda: self.__selectColour())
        self.ui.createClassBtn.clicked.connect(lambda: self.createClass(numOfClasses))

        self.show()
    def __setupPagePalette(self) -> None:
        """ Sets the colour palette for the page widgets """
        self.ui.mainFrame.setStyleSheet("QFrame{"
                                        f"background-color: {self.themePaletteColours['app.background']};"
                                        f"border: 1px solid {self.themePaletteColours['app.background']}}};")
        self.ui.classColourLbl.setStyleSheet("QLabel{"
                                             f"font: 75 12pt {self.fontTitle};"
                                             f"color: {self.themePaletteColours['font.regular']};}}")


    def __setupStyleSheet(self) -> None:
        """ Sets up style sheet of create class dialog """
        self.ui.classColourBtn.setStyleSheet("QPushButton{"
                                             "border-radius: 4px;"
                                             f"background-color: rgb{self.selectedColour};"
                                             f"border: 3px solid {self.themePaletteColours['buttonFilled.background']};}}"
                                             f"QPushButton:hover{{border-color: {self.themePaletteColours['buttonFilled.hover']}}}")

        self.ui.createClassBtn.setStyleSheet("QPushButton{"
                                             f"background-color: {self.themePaletteColours['buttonFilled.background']};"
                                             f"border : 1px solid {self.themePaletteColours['buttonFilled.background']};"
                                             "border-radius: 10px;"
                                             f"font: 75 bold 12pt {self.fontTitle};"
                                             f"color: {self.themePaletteColours['font.header']};}}"
                                             "QPushButton::hover{"
                                             f"background-color : {self.themePaletteColours['buttonFilled.hover']};"
                                             f"border : 1px solid {self.themePaletteColours['buttonFilled.hover']};}}")

        self.classNameLbl = QLabel('Class Name:')
        self.classNameLbl.setStyleSheet("QLabel{"
                                        f"font: 75 12pt {self.fontTitle};"
                                        f"color: {self.themePaletteColours['font.regular']};}}")
        self.classNameLbl.setFixedWidth(110)

        self.classNameLineEdit = UserInputQLineEdit(self.themePaletteColours, self.fontRegular)
        self.classNameLineEdit.setFixedWidth(262)
        self.classNameLineEdit.setCursorPosition(0)

        self.classNameFrameLayout = QHBoxLayout()
        self.classNameFrameLayout.addWidget(self.classNameLbl)
        self.classNameFrameLayout.addWidget(self.classNameLineEdit)
        self.classNameFrameLayout.setContentsMargins(0,0,0,0)
        self.ui.classNameFrame.setLayout(self.classNameFrameLayout)


    def __selectColour(self) -> None:
        """ Gets the specified colour from the colour selector dialog """
        self.selectedColour = getColour(self.themePaletteColours, self.fontRegular, self.fontTitle, self.selectedColour)
        self.ui.classColourBtn.setStyleSheet("QPushButton{"
                                             "border-radius: 4px;"
                                             f"background-color: rgb{self.selectedColour};"
                                             f"border: 3px solid {self.themePaletteColours['buttonFilled.background']};}}"
                                             f"QPushButton:hover{{border-color: {self.themePaletteColours['buttonFilled.hover']}}}")
        self.ui.classColourBtn.repaint()


    def __validateDialogInputs(self) -> bool:
        """
            Validates the text input for the dialog and returns the class name
        """
        className = self.classNameLineEdit.text()

        # Validating input
        valid = True   
        if className == "":
            self.classNameLineEdit.setStyleSheet("QLineEdit{"
                                                 f"font: 12pt {self.fontRegular};"
                                                 "border: 0px;"
                                                 f"color: {self.themePaletteColours['font.regular']};"
                                                 f"background-color: {self.themePaletteColours['userInput.background']};"
                                                 "border: 1px solid red}")
            valid = False
        else: 
            self.classNameLineEdit.setStyleSheet("QLineEdit{"
                                                 f"font: 12pt {self.fontRegular};"
                                                 "border: 0px;"
                                                 f"color: {self.themePaletteColours['font.regular']};"
                                                 f"background-color: {self.themePaletteColours['userInput.background']};"
                                                 f"border: 1px solid {self.themePaletteColours['userInput.border']}}}")

        if not valid:
            return
        
        self.className = className

        return True


    def createClass(self, numOfClasses) -> None:
        """ Creats a user specified class if inputs are valid """
        if self.__validateDialogInputs():
            classListItemWidget = ProjectClassListItemWidget(self.className, 0, numOfClasses, self.selectedColour, self.themePaletteColours, self.fontRegular) 
            self.classListWidget.addItemToListWidget(classListItemWidget)
            self.done(1)
