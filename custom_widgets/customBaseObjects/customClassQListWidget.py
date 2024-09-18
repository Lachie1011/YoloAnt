"""
    customClassQListWidget.py
"""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QAbstractItemView, QListWidgetItem, QSizePolicy,
                             QListWidget, QAbstractScrollArea, QListView)


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
