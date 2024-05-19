"""
    createModelDialog.py
"""

from PyQt6.QtWidgets import QDialog

from dialogs.ui.createModelDialog_ui import Ui_createModelDialog


class CreateModelDialog(QDialog):
    """
        Class that creates a dialog window to create a new model
    """
    def __init__(self, themePaletteColours: dict, fontRegular: str, fontTitle: str) -> None:
        """ init """
        super().__init__()

        self.ui = Ui_createModelDialog()
        self.ui.setupUi(self)

        self.setModal(True)
        
        self.modelName = None
        self.themePaletteColours = themePaletteColours
        self.fontRegular = fontRegular
        self.fontTitle = fontTitle

        self.__setupStyleSheet()
        self.__setupPagePalette()
        
        # Connect signals and slots
        self.ui.createModelBtn.clicked.connect(self.__createModel)
        self.ui.importModelBtn.clicked.connect(self.__importModel)
        self.show()

    def __validateUserInputs(self) -> bool:
        """ Validates all user inputs """
        if self.ui.modelLineEdit.text() == "":
            return False
        return True

    def __createModel(self) -> None:
        """ Returns new model name """
        if not self.__validateUserInputs():
            return

        self.modelName = self.ui.modelLineEdit.text()

        return self.done(1)
    
    def __importModel(self) -> None:
        """ Imports existing model """
        if not self.__validateUserInputs():
            return
        
        # TODO: open file explorer, get path from exising model, verify model type from ext.
        return

    def __setupPagePalette(self) -> None:
        """ Sets the colour palette for the page widgets """
        self.ui.mainFrame.setStyleSheet("QFrame{"
                                        f"background-color: {self.themePaletteColours['panel.background']};"
                                        f"border: 1px solid {self.themePaletteColours['panel.background']}}};")
        self.ui.modelNameLbl.setStyleSheet("QLabel{"
                                             f"font: 75 12pt {self.fontTitle};"
                                             f"color: {self.themePaletteColours['font.regular']};}}")


    def __setupStyleSheet(self) -> None:
        """ Sets up style sheet of create class dialog """
        self.ui.createModelBtn.setStyleSheet("QPushButton{"
                                             f"background-color: {self.themePaletteColours['buttonFilled.background']};"
                                             f"border : 1px solid {self.themePaletteColours['buttonFilled.background']};"
                                             "border-radius: 10px;"
                                             f"font: 75 bold 12pt {self.fontTitle};"
                                             f"color: {self.themePaletteColours['font.header']};}}"
                                             "QPushButton::hover{"
                                             f"background-color : {self.themePaletteColours['buttonFilled.hover']};"
                                             f"border : 1px solid {self.themePaletteColours['buttonFilled.hover']};}}")
        self.ui.importModelBtn.setStyleSheet("QPushButton{"
                                             f"background-color: {self.themePaletteColours['buttonFilled.background']};"
                                             f"border : 1px solid {self.themePaletteColours['buttonFilled.background']};"
                                             "border-radius: 10px;"
                                             f"font: 75 bold 12pt {self.fontTitle};"
                                             f"color: {self.themePaletteColours['font.header']};}}"
                                             "QPushButton::hover{"
                                             f"background-color : {self.themePaletteColours['buttonFilled.hover']};"
                                             f"border : 1px solid {self.themePaletteColours['buttonFilled.hover']};}}")
    
