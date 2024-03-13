"""
    classSelectionListWidget.py
"""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QAbstractItemView, QListWidgetItem, QSizePolicy,
                             QAbstractScrollArea, QListView)

from customWidgets.commonWidgets.selectableQListWidget import SelectableQListWidget

class ClassSelectionListWidget(SelectableQListWidget):
    """
        Class that creates a list widget that holds all classes for creating annotations
    """
    def __init__(self, themePaletteColours):
        super().__init__()

        # Member variables
        self.themePaletteColours = themePaletteColours
        self.editableState = False

        # Setup style sheet
        self.__setupStyleSheet()

    def __setupStyleSheet(self) -> None:
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
        
        self.setMinimumSize(0, 0)
        self.setSelectionRectVisible(False)
        self.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.setResizeMode(QListView.ResizeMode.Adjust)
        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setSpacing(3)

    def selectItemFromList(self, listItem: QListWidgetItem) -> None:
        if not self.editableState:
            super().selectItemFromList(listItem)

    def setEditMode(self, toggled):
        """ Sets the edit mode of the list widget """
        self.editableState = toggled

        # Change all items in list to state of list widget
        for listItemIndex in range(0,self.count()):
            listItem = self.item(listItemIndex)
            widgetInItem = self.itemWidget(listItem)

            if toggled:
                widgetInItem.enableEdit()
            
            else:
                widgetInItem.disableEdit()

                if self.currentItemSelected is not None:
                    self.itemWidget(self.currentItemSelected).setSelected()