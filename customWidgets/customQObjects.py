"""
    customQObjects.py
"""
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QBrush
from PyQt6.QtWidgets import (QDialog, QFrame, QLineEdit, QAbstractItemView, QListWidgetItem, 
                             QSizePolicy, QListWidget, QAbstractScrollArea, QListView)

class CustomWidgetItemQFrame(QFrame):
    """
        Class that creates a custom QFrame
    """
    def __init__(self, parentSelected, hoverColour, backgroundColour):
        super().__init__()
        self.hoverColour = hoverColour
        self.parentSelected = parentSelected
        self.backgroundColour = backgroundColour

    def enterEvent(self, event) -> None:
        """ Sets background of widget when mouse enters item widget """
        if not self.parentSelected:
            self.setStyleSheet(f"background: rgb{self.hoverColour};")

    def leaveEvent(self, event) -> None:
        """ Sets background of widget when mouse leaves item widget """
        if not self.parentSelected:
            self.setStyleSheet(f"background: rgb{self.backgroundColour};")

class CustomQLineEdit(QLineEdit):
    """
        Class that creates a custom line edit widget
    """
    def __init__(self):
        super().__init__()
   
    def focusInEvent(self, event):
        """ Sets background colour of widget when it is focused """
        super().focusInEvent(event)
        self.setStyleSheet("QLineEdit{"
                           "font: 14pt 'Gotham Rounded Light';"
                           "background-color: rgb(105,105,105);}"
                           "QLineEdit:hover{"
                           "background-color: rgb(105, 105, 105);}")

    def focusOutEvent(self, event):
        """ Sets background colour of widget when it loses focus """
        super().focusOutEvent(event)
        self.setStyleSheet("QLineEdit{"
                           "font: 14pt 'Gotham Rounded Light';"
                           "background-color: rgb(85, 87, 83);}"
                           "QLineEdit:hover{"
                           "background-color: rgb(105, 105, 105);}")

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
    def __init__(self, selectionEdit=False):
        super().__init__()

        # Member variables
        self.selectionEdit = selectionEdit

        # Setup style sheet
        self.__setupStyleSheet()

        # Store selected item in list
        self.itemSelected = None

        # Connect signals and slots
        self.itemClicked.connect(lambda item: self.__selectItem(item))
        # self.itemSelectionChanged.connect(lambda: )

    def mouseMoveEvent(object, event):
        # Disables selection with mouse click + drag
        event.ignore()   

    def __setupStyleSheet(self) -> None:
        self.setMinimumSize(0, 0)
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

    def __selectItem(self, item: QListWidgetItem) -> None:
        """ Set the chosen item to selected """
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.__clearSelection()
        self.setCurrentItem(item)
        self.itemSelected = item
        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)

        if self.selectionEdit:
            self.__enabledWidgetEditMode()

    def __clearSelection(self) -> None:
        """ clears the list of selected items """
        if self.itemSelected:
            widgetInItem = self.itemWidget(self.itemSelected)
            
            if self.selectionEdit:
                widgetInItem.disableEdit()

        self.clearSelection()

    def __enabledWidgetEditMode(self):
        """ Sets the widget in item to edit mode """
        # Change selected item to edit mode
        listItem = self.currentItem()
        widgetInItem = self.itemWidget(listItem)
        widgetInItem.enableEdit()


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