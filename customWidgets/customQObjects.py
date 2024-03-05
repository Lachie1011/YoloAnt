"""
    customQObjects.py
"""
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QBrush
from PyQt6.QtWidgets import (QDialog, QFrame, QLineEdit, QAbstractItemView, QListWidgetItem, QPushButton, QSizePolicy,
                             QSizePolicy, QListWidget, QAbstractScrollArea, QListView, QTextEdit, QGraphicsOpacityEffect)

class CustomWidgetItemQFrame(QFrame):
    """
        Class that creates a custom QFrame
    """
    def __init__(self, parentSelected, editEnabled, hoverColour, backgroundColour):
        super().__init__()
        self.hoverColour = hoverColour
        self.editEnabled = editEnabled
        self.parentSelected = parentSelected
        self.backgroundColour = backgroundColour

    def enterEvent(self, event) -> None:
        """ Sets background of widget when mouse enters item widget """
        if not self.editEnabled and not self.parentSelected:
            self.setStyleSheet(f"background: {self.hoverColour};")

    def leaveEvent(self, event) -> None:
        """ Sets background of widget when mouse leaves item widget """
        if not self.editEnabled and not self.parentSelected:
            self.setStyleSheet(f"background: {self.backgroundColour};")

class CustomQLineEdit(QLineEdit):
    """
        Class that creates a custom line edit widget
    """
    def __init__(self, themePaletteColours, fontRegular):
        super().__init__()
        self.themePaletteColours = themePaletteColours
        self.fontRegular = fontRegular
   
    def focusInEvent(self, event):
        """ Sets background colour of widget when it is focused """
        super().focusInEvent(event)
        self.setStyleSheet("QLineEdit{"
                           f"font: 12pt {self.fontRegular};"
                           f"background-color: {self.themePaletteColours['lineEdit.background']};"
                           f"border: 1px solid {self.themePaletteColours['focus.foreground']}}}")

    def focusOutEvent(self, event):
        """ Sets background colour of widget when it loses focus """
        super().focusOutEvent(event)
        self.setStyleSheet("QLineEdit{"
                           f"font: 12pt {self.fontRegular};"
                           f"background-color: {self.themePaletteColours['listItem.edit']};}}"
                           "QLineEdit:hover{"
                           f"background-color: {self.themePaletteColours['lineEdit.background']};}}")

class ListItemQLineEdit(QLineEdit):
    """
        Class that creates a custom line edit widget for application panel
    """
    def __init__(self, themePaletteColours, fontStyle):
        super().__init__()
        self.editableState = False
        self.themePaletteColours = themePaletteColours
        self.fontStyle = fontStyle
        self.__baseStyleSheet()
        self.setTextMargins(3,3,3,3)

    def __baseStyleSheet(self) -> None:
        """ Sets the style sheet for the widget """
        self.setStyleSheet("QLineEdit{"
                           f"{self.fontStyle};"
                           f"border: 1px solid transparent;"
                           f"background-color: transparent;"
                           "border-radius: 5px;"
                           f"color: {self.themePaletteColours['font.header']};}}")
        self.setReadOnly(True)
        self.setCursor(Qt.CursorShape.ArrowCursor)

    def __editableStyleSheet(self) -> None:
        """ Sets the style sheet for the widget """
        self.setStyleSheet("QLineEdit{"
                           f"{self.fontStyle};"
                           f"background-color: {self.themePaletteColours['panel.sunken']};"
                           "border-radius: 5px;"
                           f"border: 2px solid {self.themePaletteColours['userInput.border']};"
                           f"color: {self.themePaletteColours['font.header']};}}"
                           "QLineEdit:hover{"
                           f"border: 1px solid {self.themePaletteColours['focus.foreground']}}}")
        self.setReadOnly(False)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
   
    def focusInEvent(self, event):
        """ Sets background colour of widget when it is focused """
        if self.editableState:
            super().focusInEvent(event)
            self.setCursor(Qt.CursorShape.IBeamCursor)
            self.setStyleSheet("QLineEdit{"
                               f"{self.fontStyle};"
                               "border-radius: 5px;"
                               f"background-color: {self.themePaletteColours['panel.sunken']};"
                               f"border: 1px solid {self.themePaletteColours['focus.foreground']}}}")

    def focusOutEvent(self, event):
        """ Sets background colour of widget when it loses focus """
        if self.editableState:
            super().focusOutEvent(event)
            self.__editableStyleSheet()

    def setEditMode(self, toggled: bool) -> None:
        """ Sets the edit mode of the widget """
        if toggled:
            self.__editableStyleSheet()

        else:
            self.__baseStyleSheet()

        self.editableState = toggled

class PanelQLineEdit(QLineEdit):
    """
        Class that creates a custom line edit widget for application panel
    """
    def __init__(self, themePaletteColours, fontStyle):
        super().__init__()
        self.editableState = False
        self.themePaletteColours = themePaletteColours
        self.fontStyle = fontStyle
        self.__baseStyleSheet()
        self.setTextMargins(3,3,3,3)

    def __baseStyleSheet(self) -> None:
        """ Sets the style sheet for the widget """
        self.setStyleSheet("QLineEdit{"
                           f"{self.fontStyle};"
                           f"border: 1px solid {self.themePaletteColours['panel.background']};"
                           f"background-color: {self.themePaletteColours['panel.background']};"
                           "border-radius: 5px;"
                           f"color: {self.themePaletteColours['font.header']};}}")
        self.setReadOnly(True)
        self.setCursor(Qt.CursorShape.ArrowCursor)

    def __editableStyleSheet(self) -> None:
        """ Sets the style sheet for the widget """
        self.setStyleSheet("QLineEdit{"
                           f"{self.fontStyle};"
                           f"background-color: {self.themePaletteColours['panel.sunken']};"
                           "border-radius: 5px;"
                           f"border: 2px solid {self.themePaletteColours['userInput.border']};"
                           f"color: {self.themePaletteColours['font.header']};}}"
                           "QLineEdit:hover{"
                           f"border: 1px solid {self.themePaletteColours['focus.foreground']}}}")
        self.setReadOnly(False)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
   
    def focusInEvent(self, event):
        """ Sets background colour of widget when it is focused """
        if self.editableState:
            super().focusInEvent(event)
            self.setCursor(Qt.CursorShape.IBeamCursor)
            self.setStyleSheet("QLineEdit{"
                               f"{self.fontStyle};"
                               "border-radius: 5px;"
                               f"background-color: {self.themePaletteColours['panel.sunken']};"
                               f"border: 1px solid {self.themePaletteColours['focus.foreground']}}}")

    def focusOutEvent(self, event):
        """ Sets background colour of widget when it loses focus """
        if self.editableState:
            super().focusOutEvent(event)
            self.__editableStyleSheet()

    def setEditMode(self, toggled: bool) -> None:
        """ Sets the edit mode of the widget """
        if toggled:
            self.__editableStyleSheet()

        else:
            self.__baseStyleSheet()

        self.editableState = toggled

class PanelQTextEdit(QTextEdit):
    """
        Class that creates a custom text edit widget for application panel
    """
    def __init__(self, themePaletteColours, fontType):
        super().__init__()
        self.editableState = False
        self.themePaletteColours = themePaletteColours
        self.fontType = fontType
        self.__baseStyleSheet()
        self.setViewportMargins(3,3,3,3)

    def __baseStyleSheet(self) -> None:
        """ Sets the style sheet for the widget """
        self.setStyleSheet("QTextEdit{"
                           f"font: 75 12pt {self.fontType};"
                           f"border: 1px solid {self.themePaletteColours['panel.background']};"
                           f"background-color: {self.themePaletteColours['panel.background']};"
                           "border-radius: 5px;"
                           f"color: {self.themePaletteColours['font.header']};}}")
        self.setReadOnly(True)
        self.viewport().setCursor(Qt.CursorShape.ArrowCursor)

    def __editableStyleSheet(self) -> None:
        """ Sets the style sheet for the widget """
        self.setStyleSheet("QTextEdit{"
                           f"font: 75 12pt {self.fontType};"
                           f"background-color: {self.themePaletteColours['panel.sunken']};"
                           "border-radius: 5px;"
                           f"border: 2px solid {self.themePaletteColours['userInput.border']};"
                           f"color: {self.themePaletteColours['font.header']};}}"
                           "QTextEdit:hover{"
                           f"border: 1px solid {self.themePaletteColours['focus.foreground']}}}")
        self.setReadOnly(False)
        self.viewport().setCursor(Qt.CursorShape.PointingHandCursor)
   
    def focusInEvent(self, event):
        """ Sets background colour of widget when it is focused """
        if self.editableState:
            super().focusInEvent(event)
            self.viewport().setCursor(Qt.CursorShape.IBeamCursor)
            self.setStyleSheet("QTextEdit{"
                               f"font: 75 12pt {self.fontType};"
                               "border-radius: 5px;"
                               f"background-color: {self.themePaletteColours['panel.sunken']};"
                               f"border: 1px solid {self.themePaletteColours['focus.foreground']}}}")

    def focusOutEvent(self, event):
        """ Sets background colour of widget when it loses focus """
        if self.editableState:
            super().focusOutEvent(event)
            self.__editableStyleSheet()

    def setEditMode(self, toggled) -> None:
        """ Sets the edit mode of the widget """
        if toggled:
            self.__editableStyleSheet()

        else:
            self.__baseStyleSheet()

        self.editableState = toggled

class ProjectImageQPushButton(QPushButton):
    """
        Class that creates a custom text edit widget for application panel
    """
    def __init__(self, themePaletteColours):
        super().__init__()
        self.editableState = False
        self.themePaletteColours = themePaletteColours
        self.__baseStyleSheet()
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def __baseStyleSheet(self) -> None:
        """ Sets the style sheet for the widget """
        self.setStyleSheet("QPushButton{"
                           f"border: 1px solid {self.themePaletteColours['userInput.border']};"
                           "background-color: #FFFFFF;" 
                           "border-radius: 5px;}")
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.opacityEffect = QGraphicsOpacityEffect()
        self.opacityEffect.setOpacity(0.99)
        self.setGraphicsEffect(self.opacityEffect)
        self.setAutoFillBackground(True)

    def __editableStyleSheet(self) -> None:
        """ Sets the style sheet for the widget """
        self.setStyleSheet("QPushButton{"
                           "background-color: #FFFFFF;" 
                           f"border: 1px solid {self.themePaletteColours['userInput.border']};"
                           "border-radius: 5px;}")
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def enterEvent(self, event) -> None:
        """ Sets background of widget when mouse enters item widget """
        if self.editableState:
            self.setStyleSheet("QPushButton{"
                               "background-color: #FFFFFF;" 
                               f"border: 1px solid {self.themePaletteColours['focus.foreground']};"
                               "border-radius: 5px;}")
            self.opacityEffect.setOpacity(0.5)

    def leaveEvent(self, event) -> None:
        """ Sets background of widget when mouse leaves item widget """
        if self.editableState:
            self.setStyleSheet("QPushButton{"
                                "background-color: #FFFFFF;" 
                                f"border: 1px solid {self.themePaletteColours['userInput.border']};"
                                "border-radius: 5px;}")
            self.opacityEffect.setOpacity(0.99)

    def setEditMode(self, toggled) -> None:
        """ Sets the edit mode of the widget """
        if toggled:
            self.__editableStyleSheet()

        else:
            self.__baseStyleSheet()

        self.editableState = toggled

class UserInputQLineEdit(QLineEdit):
    """
        Class that creates a user input line edit widget
    """
    def __init__(self, themePaletteColours, fontRegular):
        super().__init__()
        self.themePaletteColours = themePaletteColours
        self.fontRegular = fontRegular
        self.__baseStyleSheet()
        self.setTextMargins(3,3,3,3)

    def __baseStyleSheet(self) -> None:
        """ Sets the style sheet for the widget """
        self.setStyleSheet("QLineEdit{"
                           f"font: 12pt {self.fontRegular};"
                           "border-radius: 5px;"
                           f"color: {self.themePaletteColours['font.regular']};"
                           f"background-color: {self.themePaletteColours['panel.sunken']};"
                           f"border: 1px solid {self.themePaletteColours['userInput.border']}}}")

    def validTextInput(self, valid) -> None:
        if not valid:
            self.setStyleSheet("QLineEdit{"
                               f"font: 12pt {self.fontRegular};"
                               "border-radius: 5px;"
                               f"color: {self.themePaletteColours['font.regular']};"
                               f"background-color: {self.themePaletteColours['panel.sunken']};"
                               "border: 1px solid red}")

        else:
            self.__baseStyleSheet()

    def focusInEvent(self, event):
        """ Sets background colour of widget when it is focused """
        super().focusInEvent(event)
        self.setStyleSheet("QLineEdit{"
                           f"font: 12pt {self.fontRegular};"
                           "border-radius: 5px;"
                           f"color: {self.themePaletteColours['font.regular']};"
                           f"background-color: {self.themePaletteColours['panel.sunken']};"
                           f"border: 1px solid {self.themePaletteColours['focus.foreground']};}}")

    def focusOutEvent(self, event):
        """ Sets background colour of widget when it loses focus """
        super().focusOutEvent(event)
        self.setStyleSheet("QLineEdit{"
                           f"font: 12pt {self.fontRegular};"
                           "border-radius: 5px;"
                           f"color: {self.themePaletteColours['font.regular']};"
                           f"background-color: {self.themePaletteColours['panel.sunken']};"
                           f"border: 1px solid {self.themePaletteColours['userInput.border']};}}")

class CustomKeySelectionDialog(QDialog):
    """
        Class that creates a nearly invisiable dialog to read keyboard input
    """
    def __init__(self):
        super().__init__()
        self.setModal(True)
        self.show()
        self.setWindowFlags(Qt.WindowType.Tool | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedHeight(1)
        self.setFixedWidth(1)

    def getKeyInput(self):
        self.exec()
        return self.keyInput

    def keyPressEvent(self, event):
        """ Read key input from user """
        try:
            if event.key() == Qt.Key.Key_Escape:
                self.keyInput = None
                self.done(1)

            self.keyInput = chr(event.key())
            self.done(1)

        except Exception as exc:
                print("Not a valid hotkey.")
                self.done(1)

def getKeyInput() -> chr:
    """ Sets application to modal and gets a key input """
    __customKeySelectionDialog = CustomKeySelectionDialog()

    return __customKeySelectionDialog.getKeyInput()

def ClassSelectionQFrame(QFrame):
    """
        Class that creates a class selection frame
    """

    def __init__(self, parentSelected, editEnabled, hoverColour, backgroundColour):
        super().__init__()
        self.hoverColour = hoverColour
        self.editEnabled = editEnabled
        self.parentSelected = parentSelected
        self.backgroundColour = backgroundColour
        self.__setupStyleSheet()

    def __setupStyleSheet(self) -> None:
        """ Sets up the style sheet of frame """
        self.setStyleSheet(f"QFrame{{background-color: {self.themePaletteColours['listItem.background']};}}")
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setFixedHeight(60)

        # Class attributes frame
        self.classAttributesFrame = QFrame()
        self.classAttributesLayout = QHBoxLayout()
        self.classAttributesLayout.addWidget(self.__baseStyleSheet())
        self.classAttributesLayout.addWidget(self.__editableStyleSheet())
        self.classItemWidetLayout.setContentsMargins(0,0,0,0)
        self.classAttributesFrame.setLayout(classItemWidetLayout)

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


        # Set layout of frame
        self.classSelectionQFrameLayout = QHBoxLayout()
        self.classSelectionQFrameLayout.addWidget(self.classAttributesFrame)
        self.classSelectionQFrameLayout.addWidget(self.expandFrameBtn)
        self.classItemWidetLayout.setContentsMargins(0,0,5,0)
        self.setLayout(classSelectionQFrameLayout)


    def __baseStyleSheet(self):
        """ Sets up the base style sheet for the frame """ 

        # Colour picker label
        self.classColourLbl = QLabel()
        self.classColourLbl.setStyleSheet("QLabel{"
                                            f"background-color: rgb({self.r}, {self.g}, {self.b});"
                                            "border-radius: 4px;"
                                            "border-top-right-radius: 0px;"
                                            "border-bottom-right-radius: 0px;}")
        self.classColourLbl.setFixedWidth(20)

        # Class name label
        self.classItemLbl = QLabel(self.className)
        self.classItemLbl.setStyleSheet(f"QLabel{{font: 12pt {self.fontRegular};}}")
        self.classItemLbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.classItemLbl.setMinimumSize(20, 30)
        self.classItemLbl.setMaximumSize(150, 30)

        # Hotkey label
        self.hotkeyLbl = QLabel()
        self.hotkeyLbl.setStyleSheet("QLabel{"
                                    "background-color: transparent;"
                                    f"border: 2px solid {self.themePaletteColours['buttonFilled.background']};"
                                    "border-radius: 5px;}")
        self.hotkeyLbl.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.hotkeyLbl.setFixedWidth(25)
        self.hotkeyLbl.setFixedHeight(25)

        # Annotation count label
        self.annotationCountLbl = QLabel()
        self.annotationCountLbl.setStyleSheet("QLabel{"
                                            f"background-color: {self.themePaletteColours['panel.sunken']};"
                                            f"border: 2px solid {self.themePaletteColours['panel.sunken']};"
                                            "border-radius: 5px;}")
        self.annotationCountLbl.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.annotationCountLbl.setFixedWidth(25)
        self.annotationCountLbl.setFixedHeight(20)

        # Horizontal spacers
        spacer1 = QSpacerItem(2, 5, QSizePolicy.Policy.Fixed)
        spacer2 = QSpacerItem(2, 5, QSizePolicy.Policy.Fixed)
        spacer3 = QSpacerItem(2, 5, QSizePolicy.Policy.Fixed)
        spacer4 = QSpacerItem(4, 5, QSizePolicy.Policy.Fixed)
        spacer5 = QSpacerItem(5, 5, QSizePolicy.Policy.Fixed)




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


    def __editableStyleSheet(self):
        """ Sets up the style sheet when frame is in edit mode """  
        if self.editFrameLayout is None:
            # Colour picker button
            self.classColourBtn = QPushButton()
            self.classColourBtn.setStyleSheet("QPushButton{"
                                            f"background-color: rgb({self.r}, {self.g}, {self.b});"
                                            "border-radius: 4px;"
                                            f"border: 3px solid {self.themePaletteColours['buttonFilled.background']};}}"
                                            f"QPushButton:hover{{border: 3px solid {self.themePaletteColours['buttonFilled.hover']};}}")
            self.classColourBtn.setFixedWidth(20)
            self.classColourBtn.setFixedHeight(20)
            self.classColourBtn.setVisible(False)
            self.classColourBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

            # Class name line edit
            self.classItemLineEdit = ListItemQLineEdit(self.themePaletteColours, f"font: 75 12pt {self.fontRegular};")
            self.classItemLineEdit.editingFinished.connect(lambda: self.setClassName(self.classItemLineEdit.text()))
            self.classItemLineEdit.setText(self.className)
            self.classItemLineEdit.setMinimumSize(100, 30)
            self.classItemLineEdit.setMaximumSize(150, 30)
            self.classItemLineEdit.setTextMargins(2,0,2,0)
            self.classItemLineEdit.setCursorPosition(0)
            self.classItemLineEdit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

            # Hotkey button
            self.hotkeyBtn = QPushButton()
            self.hotkeyBtn.setStyleSheet("QPushButton{"
                                        f"background-color: {self.themePaletteColours['buttonFilled.background']};"
                                        f"border: 2px solid {self.themePaletteColours['buttonFilled.background']};"
                                        "border-radius: 5px;}"
                                        "QPushButton:hover{"
                                        f"background-color: {self.themePaletteColours['buttonFilled.hover']};"
                                        f"border: 2px solid {self.themePaletteColours['buttonFilled.hover']};}}")
            self.hotkeyBtn.setFixedWidth(25)
            self.hotkeyBtn.setFixedHeight(25)
            self.hotkeyBtn.setVisible(False)
            self.hotkeyBtn.setText('a')
            self.hotkeyBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

            # Delete button
            self.classDeleteBtn = QPushButton()
            self.classDeleteBtn.setStyleSheet("QPushButton{"
                                            "border-image: url('icons/icons8-trash-can-25.png');"
                                            "background-color: transparent;}")
            self.classDeleteBtn.setFixedWidth(20)
            self.classDeleteBtn.setFixedHeight(20)
            self.classDeleteBtn.setVisible(False)
            self.classDeleteBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

            # Colour spacer
            self.spacerWidget = QFrame()
            self.spacerWidget.setStyleSheet("QFrame{background-color:transparent;}")
            self.spacerWidget.setFixedWidth(2)
            self.spacerWidget.setFixedHeight(5)
            self.spacerWidget.setVisible(False)



class CustomClassQListWidget (QListWidget):
    """
        Class that creates a custom list widget for classes
    """
    def __init__(self, themePaletteColours, selectableList = True):
        super().__init__()

        # Member variables
        self.themePaletteColours = themePaletteColours
        self.editableState = False

        # Setup style sheet
        self.__setupStyleSheet()

        # Store selected item in list
        self.itemSelected = None

        # Connect signals and slots
        if selectableList:
            self.itemClicked.connect(lambda item: self.__selectItem(item))

    def mouseMoveEvent(object, event):
        # Disables selection with mouse click + drag
        event.ignore()   

    def __setupStyleSheet(self) -> None:
        self.setMinimumSize(0, 0)
        # self.setDragEnabled(True)
        self.setSelectionRectVisible(False)
        self.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.setResizeMode(QListView.ResizeMode.Adjust)
        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setStyleSheet("QScrollBar:vertical{"
                           "border: none;"
                           "width: 10px;"
                           "margin: 15px 0 15px 0;"
                           "border-radius: 0px;}"
                           "QScrollBar::handle:vertical{"
                           "background-color: rgb(80,80,80);"
                           "min-height:30px;"
                           "border-radius: 4px;}"
                           "QScrollBar::handle:vertical:pressed{"	
	                       "background-color: rgb(185, 0, 92);}"
                           "QScrollBar::sub-line:vertical{"
                           "border: none;"
                           "background: none;"
                           "color: none;}"
                           "QScrollBar::add-line:vertical{"
                           "border: none;"
                           "background: none;"
                           "color: none;}")  

    def __selectItem(self, listItem: QListWidgetItem) -> None:
        """ Set the chosen item to selected """
        if not self.editableState:
            self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
            self.clearListSelection(self.itemSelected)
            self.itemWidget(listItem).setSelected()
            self.itemSelected = listItem
            self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)


    def setEditMode(self, toggled):
        """ Sets the widget in item to edit mode """
        # Change selected item to edit mode
        for listItemIndex in range(0,self.count()):
            listItem = self.item(listItemIndex)
            widgetInItem = self.itemWidget(listItem)

            if toggled:
                self.editableState = True
                widgetInItem.enableEdit()
            
            else:
                self.editableState = False
                widgetInItem.disableEdit()

                if self.itemSelected:
                    self.itemWidget(self.itemSelected).setSelected()

    def addItemToListWidget(self, listWidgetItem: QListWidgetItem) -> None:
        """ Adds item widget to list widget """ 

        # Create class item for list 
        listItem = QListWidgetItem(self)
        listItem.setSizeHint(listWidgetItem.sizeHint())
        listWidgetItem.parentItem = listItem
        
        # Add class item to list
        self.addItem(listItem)
        self.setItemWidget(listItem, listWidgetItem)

    def removeItemFromListWidget(self, item: QListWidgetItem) -> None:
        """ Removes item widget from list widget""" 
        self.takeItem(self.row(item))
        self.itemSelected = None

    def clearListSelection(self, listItem: QListWidgetItem) -> None:
        """ Clears the list of selections made """
        if self.itemSelected:
            self.itemWidget(listItem).clearSelected()
        self.clearSelection()