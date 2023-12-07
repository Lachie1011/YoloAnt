"""
    infoDialog.py
"""

import os
import yaml
from PyQt6.QtGui import QPixmap 
from PyQt6.QtWidgets import QApplication, QWidget, QDialog

from dialogs.ui.infoDialog_ui import Ui_MainDialog


class InfoDialog(QDialog):
    """
        Class that creates a dialog window to inform user of information about YoloAnt
    """
    def __init__(self) -> None:
        """ init """
        super().__init__()

        self.ui = Ui_MainDialog()
        self.ui.setupUi(self)
        self.__populateWidgets()

        self.show()

    def __populateWidgets(self) -> None:
        """
            Populates widgets with YoloAnt information and sets image
        """

        # Load yoloAnt data for information dialog
        with open('information.yaml', 'r') as file:
            self.informationData = yaml.safe_load(file)

        self.ui.versionTxt.setText(self.informationData["info"]["version"])
        self.ui.githubTxt.setText(self.informationData["info"]["githubURL"])
        self.ui.documentsTxt.setText(self.informationData["info"]["documentsURL"])
        self.ui.developersTxt.setText(self.informationData["info"]["developers"])
        self.ui.antHeadLbl.setPixmap(QPixmap("icons/icons8-ant-head-96.png"))