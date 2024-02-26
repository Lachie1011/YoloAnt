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