"""
    yoloAnt.py
    WIP: main entry point for the yoloant application
"""

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
from yoloAnt_ui import Ui_MainWindow


class YoloAnt(QMainWindow):
    """
        Class the creates and runs the yoloant application
    """
    def __init__(self):
        """ init """
        super().__init__()

        self.ui = Ui_MainWindow()       
        self.ui.setupUi(self)       
        
        self.show()

def main() -> None:
    """
        main entry point
    """
    app = QApplication(sys.argv)
    main_window = YoloAnt()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()