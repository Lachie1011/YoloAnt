"""
    createClassDialog.py
"""

from PyQt6.QtWidgets import QDialog, QLabel, QListWidget, QHBoxLayout

from dialogs.ui.createClassDialog_ui import Ui_createClassDialog
from customWidgets.customBaseObjects.customUserInputQLineEdit import CustomUserInputQLineEdit
from customWidgets.projectClassListItemWidget import ProjectClassListItemWidget
from dialogs.colourSelectorDialog import getColour

class CreateClassDialog(QDialog):
    """
        Class that creates a dialog window to create a class
    """
    def __init__(self, themePaletteColours: dict, fontRegular: str, fontTitle: str) -> None:
        """ init """
        super().__init__()

        self.ui = Ui_createClassDialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Create Class")

        self.setModal(True)

        # Member variables
        self.themePaletteColours = themePaletteColours
        self.fontRegular = fontRegular
        self.fontTitle = fontTitle

        self.selectedColour = (0,0,0)  # Defaulted to this TODO: should be able to pass None in and the getcoloutr function witll just handle  
        self.isValid = False

        self.__setupStyleSheet()
        self.__setupPagePalette()

        # Connect signals and slots
        self.ui.classColourBtn.clicked.connect(lambda: self.__selectColour())
        self.ui.createClassBtn.clicked.connect(lambda: self.__validateDialogInputs())
        
        self.show()

    def __setupPagePalette(self) -> None:
        """ Sets the colour palette for the page widgets """
        self.ui.mainFrame.setStyleSheet("QFrame{"
                                        f"background-color: {self.themePaletteColours['panel.background']};"
                                        f"border: 1px solid {self.themePaletteColours['panel.background']}}};")
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

        self.classNameLineEdit = CustomUserInputQLineEdit(self.themePaletteColours, self.fontRegular)
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
        valid = True   

        className = self.classNameLineEdit.text()

        # Validating input
        if className == "":
            valid = False
            
        self.classNameLineEdit.validTextInput(valid)

        self.isValid = valid
        if not valid:
            return
        
        self.className = className

        return self.done(1)

