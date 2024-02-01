"""
    annoPageListWidgetItem.py
"""
from PyQt6.QtGui import QCursor 
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QFrame, QLabel, QHBoxLayout, QLineEdit, QSpacerItem, 
                             QSizePolicy, QPushButton, QToolButton, QVBoxLayout)
                        
from customWidgets.customQObjects import *
from utils.expandingFrame import ExpandingFrame
from customWidgets.annotationListWidgetItem import AnnotationListWidgetItem

class AnnoPageListWidgetItem (QFrame):
    """
        Class that creates a custom class item widget for class list

        params:
            className - Name of class
            colour - Annotation colour of class in RGB format: _,_,_ 
    """
    def __init__(self, className: str, colour: tuple, parent=None):
        super().__init__()

        # Member variables
        self.colour = colour
        self.className = className

        self.parentItem = None
        self.parentSelected = False
        self.r, self.g, self.b = self.colour

        # Setup widget
        self.__setupWidgetItem()

        # Connect signals and slots
        self.expandFrameBtn.clicked.connect(lambda checked: self.__expandFrame(checked))
        # self.classColourButton.clicked.connect(lambda: self.selectColour())

    def __setupWidgetItem(self) -> None:
        """ Sets up style sheet for widget item """

        # Setup widget item contents
        self.classSelectionFrame = self.__setupClassSelectionFrame()
        self.classAnnotationsFrame = self.__setUpAnnotationsFrame()

        # Apply contents to widget item
        self.widgetItemLayout = QVBoxLayout()
        self.widgetItemLayout.setSpacing(0)
        self.widgetItemLayout.setContentsMargins(0,0,0,0)
        self.widgetItemLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.widgetItemLayout.addWidget(self.classSelectionFrame)
        self.widgetItemLayout.addWidget(self.classAnnotationsFrame)
        self.setLayout(self.widgetItemLayout)


    def __setupClassSelectionFrame(self) -> QFrame:
        """ Sets up style sheet for class selection frame """

        # Class selection frame
        self.classSelectionFrame = CustomWidgetItemQFrame(self.parentSelected, (105, 105, 105), (80, 80, 80))
        self.classSelectionFrame.setStyleSheet("QFrame{background-color: rgb(80,80,80);}")
        self.classSelectionFrame.setFixedHeight(60)

        # Colour picker label
        self.classColourLbl = QLabel()
        self.classColourLbl.setStyleSheet("QLabel{"
                                          f"background-color: rgb({self.r}, {self.g}, {self.b});"
                                          "border-radius: 4px;"
                                          "border-top-right-radius: 0px;"
                                          "border-bottom-right-radius: 0px;}")
        self.classColourLbl.setFixedWidth(20)

        # Colour picker button
        self.classColourButton = QPushButton()
        self.classColourButton.setStyleSheet("QPushButton{"
                                             f"background-color: rgb({self.r}, {self.g}, {self.b});"
                                             "border-radius: 4px;"
                                             "border: 3px solid rgb(105,105,105);}"
                                             "QPushButton:hover{border-color: rgb(165, 165, 165)}")
        self.classColourButton.setFixedWidth(20)
        self.classColourButton.setFixedHeight(60)
        self.classColourButton.setVisible(False)
        self.classColourButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Class name label
        self.classItemLbl = QLabel(self.className)
        self.classItemLbl.setStyleSheet("QLabel{font: 12pt 'Gotham Rounded Light';}")
        self.classItemLbl.setMinimumSize(100, 30)
        self.classItemLbl.setContentsMargins(2,0,2,0)
        self.classItemLbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # Class name line edit, not visible by default
        self.classItemLineEdit = CustomQLineEdit()
        self.classItemLineEdit.editingFinished.connect(lambda: self.setClassName(self.classItemLineEdit.text()))
        self.classItemLineEdit.setStyleSheet("QLineEdit{"
                                             "font: 12pt 'Gotham Rounded Light';}"
                                             "QLineEdit:hover{"
                                             "background-color: rgb(105, 105, 105);}")
        self.classItemLineEdit.setText(self.className)
        # self.classItemLineEdit.setTextMargins(20,0,5,0)
        self.classItemLineEdit.setMinimumSize(100, 30)
        self.classItemLineEdit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.classItemLineEdit.setVisible(False)

        # Hotkey label
        self.hotkeyLbl = QLabel()
        self.hotkeyLbl.setStyleSheet("QLabel{"
                                     "background-color: transparent;"
                                     "border: 2px solid rgb(105, 105, 105);"
                                     "border-radius: 5px;}")
        self.hotkeyLbl.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.hotkeyLbl.setFixedWidth(25)
        self.hotkeyLbl.setFixedHeight(25)
        self.hotkeyLbl.setText('a')

        # Hotkey button
        self.hotkeyBtn = QPushButton()
        self.hotkeyBtn.setStyleSheet("QPushButton{"
                                     "background-color: transparent;"
                                     "border: 2px solid rgb(105, 105, 105);"
                                     "border-radius: 5px;}"
                                     "QPushButton:hover{border-color: rgb(165, 165, 165);}")
        self.hotkeyBtn.setFixedWidth(25)
        self.hotkeyBtn.setFixedHeight(25)
        self.hotkeyBtn.setVisible(False)
        self.hotkeyBtn.setText('a')
        self.hotkeyBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Annotation count label
        self.annotationCountLbl = QLabel()
        self.annotationCountLbl.setStyleSheet("QLabel{background-color: rgb(65, 66, 64);"
                                              "border: 2px solid rgb(65, 66, 64);"
                                              "border-radius: 5px;}")
        self.annotationCountLbl.setFixedWidth(30)
        self.annotationCountLbl.setFixedHeight(25)
        self.annotationCountLbl.setText('0')
        self.annotationCountLbl.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        # Horizontal spacer
        spacer = QSpacerItem(3, 5, QSizePolicy.Policy.Fixed)
        spacerExpanding = QSpacerItem(0, 5, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)


        # # Delete Label placeholder picker label
        # self.classDeleteLbl = QLabel()
        # self.classDeleteLbl.setStyleSheet("QLabel{"
        #                                   "background-color: transparent;}")
        # self.classDeleteLbl.setFixedWidth(15)
        # self.classDeleteLbl.setFixedHeight(15)

        # Delete button
        self.classDeleteButton = QPushButton()
        self.classDeleteButton.setStyleSheet("QPushButton{"
                                             "background-color: rgb(232, 93, 84);}"
                                             "QPushButton:hover{background-color: rgb(255, 43, 28)}")
        self.classDeleteButton.setFixedWidth(15)
        self.classDeleteButton.setFixedHeight(15)
        self.classDeleteButton.setVisible(False)
        self.classDeleteButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Expand button
        self.expandFrameBtn = QToolButton()
        self.expandFrameBtn.setStyleSheet("QToolButton{"
                                          "border-radius: 4px;"
                                          "border: 3px solid rgb(255, 255, 255)}")
        self.expandFrameBtn.setFixedWidth(25)
        self.expandFrameBtn.setFixedHeight(25)

        self.expandFrameBtn.setCheckable(True)
        self.expandFrameBtn.setChecked(False)

        # Setting layout of custom widget 
        self.classItemWidetLayout = QHBoxLayout()
        self.classItemWidetLayout.addWidget(self.classColourLbl)
        self.classItemWidetLayout.addWidget(self.classColourButton)
        self.classItemWidetLayout.addItem(spacer)
        self.classItemWidetLayout.addWidget(self.classItemLbl)
        self.classItemWidetLayout.addWidget(self.classItemLineEdit)
        self.classItemWidetLayout.addItem(spacer)
        self.classItemWidetLayout.addWidget(self.hotkeyLbl)
        self.classItemWidetLayout.addWidget(self.hotkeyBtn)
        self.classItemWidetLayout.addItem(spacer)
        self.classItemWidetLayout.addWidget(self.annotationCountLbl)
        self.classItemWidetLayout.addItem(spacer)
        # self.classItemWidetLayout.addWidget(self.classDeleteLbl)
        self.classItemWidetLayout.addWidget(self.classDeleteButton)
        self.classItemWidetLayout.addWidget(self.expandFrameBtn)


        self.classItemWidetLayout.setContentsMargins(0,0,0,0)
        self.classSelectionFrame.setLayout(self.classItemWidetLayout)

        self.classSelectionFrame.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        return self.classSelectionFrame

    def __setUpAnnotationsFrame(self) -> QFrame:

        self.annotationListWidgetLayout = QVBoxLayout()
        self.annotationListWidget = CustomClassQListWidget()
        annotationListItemWidget = AnnotationListWidgetItem("Dog (1)") 
        annotationListItemWidget2 = AnnotationListWidgetItem("Dog (1)") 
        annotationListItemWidget3 = AnnotationListWidgetItem("Dog (1)") 
        annotationListItemWidget4 = AnnotationListWidgetItem("Dog (1)") 
        self.annotationListWidget.addItemToListWidget(annotationListItemWidget)
        self.annotationListWidget.addItemToListWidget(annotationListItemWidget2)
        self.annotationListWidget.addItemToListWidget(annotationListItemWidget3)
        self.annotationListWidget.addItemToListWidget(annotationListItemWidget4)

        self.annotationListWidgetLayout.addWidget(self.annotationListWidget)
        self.annotationListWidgetLayout.setContentsMargins(0,0,0,0)
        self.annotationFrame = ExpandingFrame(self.annotationListWidgetLayout)
        self.annotationFrame.setStyleSheet("QFrame{border-top-left-radius: 0px;"
                                           "border-top-right-radius: 0px;}")

        return self.annotationFrame

    def __expandFrame(self, checked):
        self.annotationFrame.start_animation(checked)

        if checked: 
            self.classAnnotationsFrame.setFixedHeight(self.annotationListWidgetLayout.sizeHint().height())
            self.setFixedHeight(self.height() + self.annotationListWidgetLayout.sizeHint().height())

        else: 
            self.classAnnotationsFrame.setFixedHeight(0)
            self.setFixedHeight(self.height() - self.annotationListWidgetLayout.sizeHint().height())

        if self.parentItem:
            self.parentItem.setSizeHint(self.sizeHint())

    def enableEdit(self) -> None:
        """ Sets the item widget to edit mode """
        self.parentSelected = True
        self.classColourLbl.setVisible(False)
        self.classColourButton.setVisible(True)
        self.classItemLbl.setVisible(False)
        self.classItemLineEdit.setVisible(True)
        self.hotkeyLbl.setVisible(False)
        self.hotkeyBtn.setVisible(True)
        # self.classDeleteLbl.setVisible(False)
        # self.classDeleteButton.setVisible(True)
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        
    def disableEdit(self) -> None:
        """ Disables edit mode of item widget """
        self.classColourLbl.setVisible(True)
        self.classColourButton.setVisible(False)
        self.parentSelected = False
        self.classItemLbl.setVisible(True)
        self.classItemLineEdit.setVisible(False)
        self.hotkeyLbl.setVisible(True)
        self.hotkeyBtn.setVisible(False)
        # self.classDeleteLbl.setVisible(True)
        # self.classDeleteButton.setVisible(False)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    def setClassName(self, text: str) -> None:
        self.className = text
        self.classItemLbl.setText(text)
        self.classItemLineEdit.setText(text)

        if self.classItemLineEdit.hasFocus():
            self.classItemLineEdit.clearFocus()

    def setHotkey(self, text: str) -> None:
        self.hotkeyLbl.setText(text) 

        if self.hotkeyLineEdit.hasFocus():
            self.hotkeyLineEdit.clearFocus()

    def selectColour(self) -> None:
        self.colour = getColour(self.colour)
        self.r, self.g, self.b = self.colour

        self.classColourLbl.setStyleSheet("QLabel{"
                                    f"background-color: rgb({self.r}, {self.g}, {self.b});"
                                    "border-radius: 4px;"
                                    "border: 3px solid rgb(105, 105, 105)}")

        self.classColourButton.setStyleSheet("QPushButton{"
                                        f"background-color: rgb({self.r}, {self.g}, {self.b});"
                                        "border-radius: 4px;"
                                        "border: 3px solid rgb(105, 105, 105)}"
                                        "QPushButton:hover{border-color: rgb(165, 165, 165)}"
                                        )
        self.classColourLbl.repaint()
        self.classColourButton.repaint()
