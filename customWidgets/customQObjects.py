"""
    customQObjects.py
"""
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QBrush, QCursor
from PyQt6.QtWidgets import (QDialog, QFrame, QLineEdit, QAbstractItemView, QListWidgetItem, QPushButton, QSizePolicy,
                             QSizePolicy, QListWidget, QAbstractScrollArea, QListView, QTextEdit, QGraphicsOpacityEffect,
                             QLabel, QHBoxLayout)

class CustomWidgetItemQFrame(QFrame):
    """
        Class that creates a custom QFrame
    """
    def __init__(self, themePaletteColours, parentSelected):
        """ init """
        super().__init__()
        self.themePaletteColours = themePaletteColours
        self.parentSelected = parentSelected
        self.__baseStyleSheet()

    def enterEvent(self, event) -> None:
        """ Sets background of widget when mouse enters item widget """
        if not self.parentSelected:
            self.setStyleSheet(f"background: {self.themePaletteColours['app.hover']};")

    def leaveEvent(self, event) -> None:
        """ Sets background of widget when mouse leaves item widget """
        if not self.parentSelected:
            self.setStyleSheet(f"background: {self.themePaletteColours['listItem.background']};")

    def __baseStyleSheet(self) -> None:
        """ Sets the base style sheet for the widget """
        self.setStyleSheet(f"QFrame{{background-color: {self.themePaletteColours['listItem.background']};}}")
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setFixedHeight(60)

    def __editStyleSheet(self) -> None:
        """ Sets the edit style sheet for the widget """
        self.setStyleSheet(f"QFrame{{background-color: {self.themePaletteColours['listItem.edit']};}}")
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

    def setSelected(self) -> None:
        """ Changes stylesheet of widgets to reflect being selected """
        self.setStyleSheet(f"QFrame{{background-color: {self.themePaletteColours['app.selected']};}}")
        self.parentSelected = True

    def clearSelection(self) -> None:
        """ Changes stylesheet of widgets to reflect being selected """
        self.__baseStyleSheet()

    def setEditMode(self, toggled: bool) -> None:
        """ Sets the edit mode of the widget """
        if toggled:
            self.__editStyleSheet()

        else:
            self.__baseStyleSheet()

class CustomQLineEdit(QLineEdit):
    """
        Class that creates a custom line edit widget
    """
    def __init__(self, themePaletteColours, fontRegular):
        """ init """
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

class CustomListItemQLineEdit(QLineEdit):
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

class CustomPanelQLineEdit(QLineEdit):
    """
        Class that creates a custom line edit widget for application panel
    """
    def __init__(self, themePaletteColours, fontStyle):
        """ init """
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

class CustomPanelQTextEdit(QTextEdit):
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

class CustomUserInputQLineEdit(QLineEdit):
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

class CustomClassQListWidget(QListWidget):
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
