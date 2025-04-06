"""
    createProjectDialog.py
"""

import os
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtWidgets import QDialog

from dialogs.ui.createProjectDialog_ui import Ui_MainDialog


class CreateProjectDialog(QDialog):
    """
        Class that creates a dialog window to create a project
    """
    def __init__(self) -> None:
        """ init """
        super().__init__()

        self.ui = Ui_MainDialog()
        self.ui.setupUi(self)
        self.setModal(True)

        self.projectName = ""
        self.imageDirectory = ""

        # Connecting signals and slots for the dialog
        self.ui.dirSearchBtn.clicked.connect(lambda: self.__getImageDirectory())
        self.ui.createBtn.clicked.connect(lambda: self.__validateDialogInputs())

        self.show()
    
    def __getImageDirectory(self) -> None:
        """
            Opens a folder dialog and updates the text within the image directory line 
            input
        """
        folder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.ui.imageDirInput.setText(folder)

    def __validateDialogInputs(self) -> None:
        """
            Validates each of the text inputs from the dialog and returns the 
            image directory and project in a list
        """
        projectName = self.ui.nameInput.text()
        imageDirectory = self.ui.imageDirInput.text()

        # validating input
        valid = True   
        if projectName == "":
            # self.ui.nameInput.setStyleSheet("QLineEdit"
            #                     "{"
            #                     "border : 1px solid red;"
            #                     "}")
            valid = False
        # else:
            # self.ui.nameInput.setStyleSheet("QLineEdit"
            #         "{"
            #         "border : 1px solid #373737;"
            #         "}")

        if imageDirectory == "" or not os.path.isdir(imageDirectory): 
            # self.ui.imageDirInput.setStyleSheet("QLineEdit"
            #                     "{"
            #                     "border : 1px solid red;"
            #                     "}")
            valid = False
        # else:
            # self.ui.imageDirInput.setStyleSheet("QLineEdit"
            #         "{"
            #         "border : 1px solid #373737;"
            #         "}")
        if not valid:
            return
        
        self.projectName = projectName
        self.imageDirectory = imageDirectory

        return self.done(1)
