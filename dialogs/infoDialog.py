"""
    infoDialog.py
"""

import yaml
from PyQt6.QtGui import QPixmap 
from PyQt6.QtWidgets import QDialog

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
        with open('yoloAnt.yaml', 'r') as file:
            try:
                self.informationData = yaml.safe_load(file)
                self.ui.versionTxt.setText(self.informationData["info"]["version"])
                self.ui.githubTxt.setText(self.informationData["info"]["githubURL"])
                self.ui.developersTxt.setText(self.informationData["info"]["developers"])
                # Label image is set here too, as the dialog loses designer pathing
                self.ui.antHeadLbl.setPixmap(QPixmap("icons/icons8-ant-head-96.png")) 
            except Exception as exc:
                print(exc)