"""
    classTreeItemWidget.py
"""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QToolButton, QTreeWidgetItem, QTreeWidget

from custom_widgets.annotation_manager.classAttributesFrame import ClassAttributesFrame
from custom_widgets.customBaseObjects.customWidgetItemQFrame import CustomWidgetItemQFrame
from dialogs.keySelectionDialog import getKeyInput
from dialogs.colourSelectorDialog import getColour

class ClassItem(QTreeWidgetItem):
    """ A class for creating a class item. """
    def __init__(
            self,
            className,
            classTreeWidget,
            colour: tuple,
            themePaletteColours: dict,
            fontRegular: str,
            fontTitle: str,
    ):
        super().__init__(classTreeWidget)

        # Member variables
        self.colour = colour
        self.className = className
        self.themePaletteColours = themePaletteColours
        self.fontRegular = fontRegular
        self.fontTitle = fontTitle
        self.parentItem = None
        self.editEnabled = False
        self.isExpanded = False

        self.__setupStyleSheet(classTreeWidget)
        self.__initializeClassAttributes()

    def showAnnotations(self, isVisible: bool):
        """ Shows the annotations under this class. """
        self.isExpanded = isVisible
        self.expandToolButton.setStyleSheet(self.__getExpandButtonStyle(self.isExpanded))
        self.setExpanded(self.isExpanded)
        self.expandToolButton.setChecked(self.isExpanded)

    def setEditableState(self, isEditable: bool):
        """ Sets the widget into an editable state. """
        self.classSelectionFrame.setEditMode(isEditable)
        self.classAttributesFrame.setEditMode(isEditable)

    def setFrameToSelectedState(self, isSelected: bool) -> None:
        """ Sets frame to selected state """
        if isSelected:
            self.classSelectionFrame.setSelected()
        else:
            self.classSelectionFrame.clearSelection()

    def setClassName(self, className: str) -> None:
        """ Sets the name of the class """
        self.className = className
        self.classAttributesFrame.setClassNameText(className)
        if self.classAttributesFrame.classNameLineEdit.hasFocus():
            self.classAttributesFrame.classNameLineEdit.clearFocus()

    def setHotKey(self) -> None:
        """ Gets a hotkey input from the user and sets the hotkey for the class """
        keyInput = getKeyInput()
        self.classAttributesFrame.setHotKeyText(keyInput.lower())

    def selectColour(self) -> None:
        """ Gets a selected colour from the user sets it as the class colour """
        self.colour = getColour(self.themePaletteColours, self.fontRegular, self.fontTitle, self.colour)
        self.classAttributesFrame.setClassColour(self.colour)

    def __setupStyleSheet(self, treeWidget: QTreeWidget) -> None:
        """ Sets up style sheet for list widget item"""
        self.setFlags(self.flags() & ~Qt.ItemFlag.ItemIsSelectable)
        self.setChildIndicatorPolicy(QTreeWidgetItem.ChildIndicatorPolicy.DontShowIndicatorWhenChildless)
        self.classSelectionFrame = self.__createClassSelectionFrame()
        widget = QWidget()

        layout = QVBoxLayout(widget)
        layout.addWidget(self.classSelectionFrame)
        layout.setContentsMargins(0, 0, 0, 0)
        treeWidget.setItemWidget(self, 0, widget)

    def __createClassSelectionFrame(self) -> CustomWidgetItemQFrame:
        """ Creates the selection frame for the class item. """
        self.classAttributesFrame = ClassAttributesFrame(self.themePaletteColours, self.fontRegular)
        self.expandToolButton = self.__createExpandButton()

        frame = CustomWidgetItemQFrame(self.themePaletteColours)
        frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        layout = QHBoxLayout(frame)
        layout.addWidget(self.classAttributesFrame, stretch=1)
        layout.addWidget(self.expandToolButton, stretch=0)
        layout.setContentsMargins(0, 0, 5, 0)
        layout.setSpacing(5)
        return frame

    def __initializeClassAttributes(self) -> None:
        """ Initialise class attributes """
        self.classAttributesFrame.setClassColour(self.colour)
        self.classAttributesFrame.setClassNameText(self.className)
        self.classAttributesFrame.setHotKeyText('a')
        self.classAttributesFrame.setClassAnnotationsCount('0')

    def __createExpandButton(self) -> QToolButton:
        """ Creates the expand button for annotation list. """
        toolButton = QToolButton()
        toolButton.setStyleSheet(self.__getExpandButtonStyle(False))
        toolButton.setFixedSize(15, 15)
        toolButton.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        toolButton.setCheckable(True)
        toolButton.setChecked(False)
        toolButton.clicked.connect(lambda isChecked: self.showAnnotations(isChecked))
        return toolButton

    def __getExpandButtonStyle(self, expanded: bool) -> str:
        """ Returns the stylesheet for the expand button based on state. """
        state = "down" if expanded else "left"
        return (
            f"QToolButton {{"
            f"border-image: url('icons/icons8-expand-arrow-{state}-25.png');"
            f"background-color: transparent;"
            f"}}"
            f"QToolButton:hover {{"
            f"border-image: url('icons/icons8-expand-arrow-{state}-hover-25.png');"
            f"}}"
        )