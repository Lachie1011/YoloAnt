"""
    annoPageListWidgetItem.py
"""
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor 
from PyQt6.QtWidgets import (QFrame, QLabel, QHBoxLayout, QLineEdit, QSpacerItem, 
                             QSizePolicy, QPushButton, QToolButton, QVBoxLayout, QWidget)
                        
from customWidgets.customQObjects import *
from utils.expandingFrame import ExpandingFrame
from dialogs.colourSelectorDialog import getColour
from customWidgets.annotationListWidgetItem import AnnotationListWidgetItem

class AnnoPageListWidgetItem (QFrame):
    """
        Class that creates a custom class item widget for class list.

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
        self.hotkeyBtn.clicked.connect(lambda: self.setHotkey())
        self.classColourBtn.clicked.connect(lambda: self.selectColour())
        self.expandFrameBtn.clicked.connect(lambda checked: self.__expandFrame(checked))
        self.classDeleteBtn.clicked.connect(lambda: self.parent().parent().removeItemFromListWidget(self.parentItem))

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
        self.classSelectionFrame.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
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
        self.classColourBtn = QPushButton()
        self.classColourBtn.setStyleSheet("QPushButton{"
                                          f"background-color: rgb({self.r}, {self.g}, {self.b});"
                                          "border-radius: 4px;"
                                          "border: 3px solid rgb(105,105,105);}"
                                          "QPushButton:hover{border-color: rgb(165, 165, 165)}")
        self.classColourBtn.setFixedWidth(20)
        self.classColourBtn.setFixedHeight(20)
        self.classColourBtn.setVisible(False)
        self.classColourBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Class name label
        self.classItemLbl = QLabel(self.className)
        self.classItemLbl.setStyleSheet("QLabel{font: 12pt 'Gotham Rounded Light';}")
        self.classItemLbl.setMinimumSize(20, 30)
        self.classItemLbl.setMaximumSize(150, 30)
        self.classItemLbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # Class name line edit, not visible by default
        self.classItemLineEdit = CustomQLineEdit()
        self.classItemLineEdit.editingFinished.connect(lambda: self.setClassName(self.classItemLineEdit.text()))
        self.classItemLineEdit.setStyleSheet("QLineEdit{"
                                             "font: 12pt 'Gotham Rounded Light';"
                                             "background-color: transparent;}"
                                             "QLineEdit:hover{"
                                             "background-color: rgb(200, 105, 105);}")
        self.classItemLineEdit.setText(self.className)
        self.classItemLineEdit.setMinimumSize(100, 30)
        self.classItemLineEdit.setMaximumSize(150, 30)
        self.classItemLineEdit.setTextMargins(2,0,2,0)
        self.classItemLineEdit.setCursorPosition(0)
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
        self.annotationCountLbl.setStyleSheet("QLabel{"
                                              "background-color: rgb(65, 66, 64);"
                                              "border: 2px solid rgb(65, 66, 64);"
                                              "border-radius: 5px;}")
        self.annotationCountLbl.setFixedWidth(25)
        self.annotationCountLbl.setFixedHeight(20)
        self.annotationCountLbl.setText('0')
        self.annotationCountLbl.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        # Colour spacer
        self.spacerWidget = QFrame()
        self.spacerWidget.setStyleSheet("QFrame{background-color:transparent;}")
        self.spacerWidget.setFixedWidth(2)
        self.spacerWidget.setFixedHeight(5)
        self.spacerWidget.setVisible(False)

        # Horizontal spacers
        spacer1 = QSpacerItem(2, 5, QSizePolicy.Policy.Fixed)
        spacer2 = QSpacerItem(2, 5, QSizePolicy.Policy.Fixed)
        spacer3 = QSpacerItem(2, 5, QSizePolicy.Policy.Fixed)
        spacer4 = QSpacerItem(4, 5, QSizePolicy.Policy.Fixed)
        spacer5 = QSpacerItem(5, 5, QSizePolicy.Policy.Fixed)

        # Delete button
        self.classDeleteBtn = QPushButton()
        self.classDeleteBtn.setStyleSheet("QPushButton{"
                                          "border-image: url('icons/icons8-trash-can-25.png');"
                                          "background-color: transparent;}")
        self.classDeleteBtn.setFixedWidth(20)
        self.classDeleteBtn.setFixedHeight(20)
        self.classDeleteBtn.setVisible(False)
        self.classDeleteBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Expand button
        self.expandFrameBtn = QToolButton()
        self.expandFrameBtn.setStyleSheet("QToolButton{"
                                          "border-image: url('icons/icons8-expand-arrow-left-25.png');"
                                          "background-color: transparent;}"
                                          "QToolButton:hover{"
                                          "border-image: url('icons/icons8-expand-arrow-left-hover-25.png');}")
        self.expandFrameBtn.setFixedWidth(15)
        self.expandFrameBtn.setFixedHeight(15)
        self.expandFrameBtn.setCheckable(True)
        self.expandFrameBtn.setChecked(False)

        # Setting layout of custom widget 
        self.classItemWidetLayout = QHBoxLayout()
        self.classItemWidetLayout.addWidget(self.spacerWidget)
        self.classItemWidetLayout.addWidget(self.classColourLbl)
        self.classItemWidetLayout.addWidget(self.classColourBtn)
        self.classItemWidetLayout.addItem(spacer1)
        self.classItemWidetLayout.addWidget(self.classItemLbl)
        self.classItemWidetLayout.addWidget(self.classItemLineEdit)
        self.classItemWidetLayout.addItem(spacer2)
        self.classItemWidetLayout.addWidget(self.hotkeyLbl)
        self.classItemWidetLayout.addWidget(self.hotkeyBtn)
        self.classItemWidetLayout.addItem(spacer3)
        self.classItemWidetLayout.addWidget(self.annotationCountLbl)
        self.classItemWidetLayout.addItem(spacer4)
        self.classItemWidetLayout.addWidget(self.classDeleteBtn)
        self.classItemWidetLayout.addWidget(self.expandFrameBtn)
        self.classItemWidetLayout.addItem(spacer5)

        self.classItemWidetLayout.setContentsMargins(0,0,0,0)
        self.classSelectionFrame.setLayout(self.classItemWidetLayout)
        return self.classSelectionFrame

    def __setUpAnnotationsFrame(self) -> QFrame:
        """ Sets up style sheet for annotation selection frame """

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
        self.annotationFrame.setStyleSheet("QFrame{"
                                           "border-top-left-radius: 0px;"
                                           "border-top-right-radius: 0px;}")

        return self.annotationFrame

    def __expandFrame(self, checked):
        """ Expands and shrinks the annotation frame when expand arrow is toggled """
        self.annotationFrame.start_animation(checked)

        if checked: 
            self.expandFrameBtn.setStyleSheet("QToolButton{"
                                              "border-image: url('icons/icons8-expand-arrow-down-25.png');"
                                              "background-color: transparent;}"
                                              "QToolButton:hover{"
                                              "border-image: url('icons/icons8-expand-arrow-down-hover-25.png');}")
            self.classAnnotationsFrame.setFixedHeight(self.annotationListWidgetLayout.sizeHint().height())
            self.setFixedHeight(self.height() + self.annotationListWidgetLayout.sizeHint().height())

        else: 
            self.expandFrameBtn.setStyleSheet("QToolButton{"
                                              "border-image: url('icons/icons8-expand-arrow-left-25.png');"
                                              "background-color: transparent;}"
                                              "QToolButton:hover{"
                                              "border-image: url('icons/icons8-expand-arrow-left-hover-25.png');}")
            self.classAnnotationsFrame.setFixedHeight(0)
            self.setFixedHeight(self.height() - self.annotationListWidgetLayout.sizeHint().height())

        if self.parentItem:
            self.parentItem.setSizeHint(self.sizeHint())

    def enableEdit(self) -> None:
        """ Sets the item widget to edit mode """
        self.parentSelected = True
        self.spacerWidget.setVisible(True)
        self.classColourLbl.setVisible(False)
        self.classColourBtn.setVisible(True)
        self.classItemLbl.setVisible(False)
        self.classItemLineEdit.setVisible(True)
        self.hotkeyLbl.setVisible(False)
        self.hotkeyBtn.setVisible(True)
        self.annotationCountLbl.setVisible(False)
        self.classDeleteBtn.setVisible(True)
        
    def disableEdit(self) -> None:
        """ Disables edit mode of item widget """
        self.spacerWidget.setVisible(False)
        self.classColourLbl.setVisible(True)
        self.classColourBtn.setVisible(False)
        self.parentSelected = False
        self.classItemLbl.setVisible(True)
        self.classItemLineEdit.setVisible(False)
        self.hotkeyLbl.setVisible(True)
        self.hotkeyBtn.setVisible(False)
        self.annotationCountLbl.setVisible(True)
        self.classDeleteBtn.setVisible(False)

    def setClassName(self, text: str) -> None:
        """ Sets the name of the class from user input """
        self.className = text
        self.classItemLbl.setText(text)
        self.classItemLineEdit.setText(text)

        if self.classItemLineEdit.hasFocus():
            self.classItemLineEdit.clearFocus()

    def setHotkey(self) -> None:
        """ Sets the hotkey for a class """
        keyInput = getKeyInput()
        self.hotkeyLbl.setText(keyInput.lower()) 
        self.hotkeyBtn.setText(keyInput.lower()) 
        self.hotkeyLbl.repaint()
        self.hotkeyBtn.repaint()


    def selectColour(self) -> None:
        """ Gets a selected colour from the user """
        self.colour = getColour(self.colour)
        self.r, self.g, self.b = self.colour
        self.classColourLbl.setStyleSheet("QLabel{"
                                          f"background-color: rgb({self.r}, {self.g}, {self.b});"
                                          "border-radius: 4px;"
                                          "border-top-right-radius: 0px;"
                                          "border-bottom-right-radius: 0px;}")

        self.classColourBtn.setStyleSheet("QPushButton{"
                                          f"background-color: rgb({self.r}, {self.g}, {self.b});"
                                          "border-radius: 4px;"
                                          "border: 3px solid rgb(105,105,105);}"
                                          "QPushButton:hover{border-color: rgb(165, 165, 165)}")
        self.classColourLbl.repaint()
        self.classColourBtn.repaint()