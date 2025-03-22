from PyQt6.QtCore import Qt, pyqtSignal as Signal
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (QFrame, QHBoxLayout, QToolButton, QVBoxLayout)

from PyQt6.QtWidgets import (
    QApplication, QFrame, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTreeWidget, QTreeWidgetItem, QWidget, QSpacerItem, QSizePolicy, QToolButton
)
from PyQt6.QtCore import Qt
import sys
from custom_widgets.annotation_manager.classAttributesFrame import ClassAttributesFrame
from custom_widgets.customBaseObjects.customWidgetItemQFrame import CustomWidgetItemQFrame
from dialogs.keySelectionDialog import getKeyInput
from dialogs.colourSelectorDialog import getColour

class ClassItemTreeWidget(QWidget):
    """
    A QWidget representing a class item with an expand button and delete button.
    """
    def __init__(self, className, classTreeItem, classTreeWidget, colour: tuple, themePaletteColours: dict, fontRegular: str, fontTitle: str, app):
        super().__init__()

        # Member variables
        self.colour = colour
        self.className = className
        self.themePaletteColours = themePaletteColours
        self.fontRegular = fontRegular
        self.fontTitle = fontTitle
        self.app = app
        self.parentItem = None
        self.parentSelected = False
        self.editEnabled = False
        self.classTreeItem = classTreeItem
        self.classTreeWidget = classTreeWidget
        self.isExpanded = False

        # Hide default expand indicator but allow programmatic expansion
        self.__setupStyleSheet()
        self.__initializeClassAttributes()

    def toggleExpand(self):
        """Toggle the expansion of annotations under this class."""
        self.isExpanded = not self.isExpanded
        self.expandToolButton.setStyleSheet(self.__getExpandButtonStyle(self.isExpanded))
        self.classTreeItem.setExpanded(self.isExpanded)

    def enableEdit(self) -> None:
        """ Sets the list widget item into edit mode """
        self.classSelectionFrame.setEditMode(True)
        self.classAttributesFrame.setEditMode(True)

    def disableEdit(self) -> None:
        """ Disables edit mode of list widget item """
        self.classSelectionFrame.setEditMode(False)
        self.classAttributesFrame.setEditMode(False)

    def setFrameToSelectedState(self, isSelected: bool) -> None:
        """ Sets frame to selected state """
        if isSelected:
            self.classSelectionFrame.setSelected()
            # If we select an item, update the canvas
            self.app.ui.annotationCanvas.currentClassColour = QColor(self.colour[0], self.colour[1], self.colour[2])
            self.app.ui.annotationCanvas.currentClassName = self.className
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

    def __setupStyleSheet(self) -> None:
        """ Sets up style sheet for list widget item"""
        self.classSelectionFrame = self.__createClassSelectionFrame()
        layout = QVBoxLayout(self)
        layout.addWidget(self.classSelectionFrame)
        layout.setContentsMargins(0, 0, 0, 0)
        # layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    def __createClassSelectionFrame(self) -> CustomWidgetItemQFrame:
        """ Creates the selection frame for the class item. """
        self.classAttributesFrame = ClassAttributesFrame(self.themePaletteColours, self.fontRegular)
        self.expandToolButton = self.__createExpandButton()

        frame = CustomWidgetItemQFrame(self.themePaletteColours)
        frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        layout = QHBoxLayout(frame)
        layout.addWidget(self.classAttributesFrame, stretch=1)

        # Stretch = 0 → fixed size, not squished
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
        toolButton.clicked.connect(self.toggleExpand)
        return toolButton

    def __getExpandButtonStyle(self, expanded: bool) -> str:
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

    # def __setupStyleSheet(self) -> None:
    #     """ Sets up style sheet for list widget item"""
    #     self.setStyleSheet("""
    #         QFrame {
    #             background-color: #ADD8E6; /* Light Blue */
    #         }
    #     """)
    #     self.__createClassLabel()
    #     self.__setupExpandButton()
    #     layout = QHBoxLayout()
    #     layout.setContentsMargins(5, 5, 5, 5)
    #     spacer = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
    #     layout.addWidget(self.classNameLbl)
    #     layout.addItem(spacer)  # Push expand button to the right
    #     layout.addWidget(self.expand_button)
    #     self.setLayout(layout)
    #
    # def __createClassLabel(self) -> None:
    #     # classes name label
    #     self.classNameLbl = QLabel(self.className)
    #
    #     # self.classNameLbl.setStyleSheet(f"QLabel{{font: 12pt {self.fontRegular};}}")
    #     self.classNameLbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    #     self.classNameLbl.setMinimumSize(20, 30)
    #     self.classNameLbl.setMaximumSize(170, 30)

# def __setupExpandButton(self) -> None:
#     """ Creates the expand button for annotation list. """
#     # self.expandBtn = QToolButton()
#     # self.expandBtn.setFixedSize(15, 15)
#     # self.expandBtn.setCheckable(True)
#     # self.expandBtn.setChecked(False)
#     # self.expandBtn.clicked.connect(self.toggle_expand)
#     self.expand_button = QPushButton("Expand")
#     self.expand_button.setFixedSize(70, 25)
#     self.expand_button.clicked.connect(self.toggleExpand)
#
#     # self.expandBtn.hide()  # Hidden initially

    # def __setupClassSelectionFrame(self) -> None:
    #     """ Creates the selection frame for the classes item. """
    #     # self.classSelectionFrame = CustomWidgetItemQFrame(self.parentSelected)
    #     layout = QHBoxLayout(self.classSelectionFrame)
    #     layout.addWidget(self.classNameLbl)
    #     layout.addWidget(self.classAttributesFrame)
    #     layout.addWidget(self.expandBtn)
    #     layout.setContentsMargins(0, 0, 5, 0)
    #     layout.setSpacing(5)
    #
    #
    #
    # def delete_class(self):
    #     """Deletes the entire class along with its annotations."""
    #     parent = self.classTreeWidget.invisibleRootItem()  # Root of the tree
    #     index = parent.indexOfChild(self.classTreeItem)
    #     if index != -1:
    #         parent.takeChild(index)  # Remove class from tree
    #         del self.classTreeItem  # Free memory