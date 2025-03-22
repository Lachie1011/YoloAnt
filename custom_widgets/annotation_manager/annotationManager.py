"""
    annotationManagerold.py
"""

from PyQt6 import QtCore
from typing import Any
from PyQt6.QtCore import pyqtSignal as Signal
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QFrame, QTreeWidgetItem, QTreeWidget, QHeaderView, \
    QSizePolicy, QAbstractScrollArea

from custom_widgets.customBaseObjects.customUserInputQLineEdit import CustomUserInputQLineEdit
from custom_widgets.annotation_manager.classTreeItemWidget import ClassItemTreeWidget
from custom_widgets.annotation_manager.annotationTreeItemWidget import AnnotationTreeItemWidget

class AnnotationManager(QFrame):
    """
        A custom widget for the annotation classes selection for selecting and searching for classes
    """
    classItemSelected = Signal(str)
    annotationItemSelected = Signal(str)
    annotation_removed = Signal(str)
    annotation_hidden = Signal(str, bool)

    def __init__(self, app, ui, themePaletteColours: dict, fontRegular, fontTitle):
        super(AnnotationManager, self).__init__()

        # Member variables
        self.app = app
        self.ui = ui
        self.themePaletteColours = themePaletteColours
        self.fontRegular = fontRegular
        self.fontTitle = fontTitle

        self._classes = []
        self.classListItems = []

        # Setup stylesheet of frame
        self.__setupStyleSheet()
        self.classSelected = ""

        # Connect signals and slots
        self.classSearchLineEdit.textChanged.connect(lambda searchInput: self.__searchForClass(searchInput))

    def reset(self) -> None:
        """ Resets the widget to an empty state """
        self.classSelectionListWidget.clear()
        self._classes = []
        self.classListItems = []

    def generateClassItems(self) -> None:
        """ Generates the class items for the widget """
        for _class in self.app.project.classesDataset:
            if _class.className not in self._classes:
                self.generateClassItem(_class.className, _class.classColour)

    def generateClassItem(self, className: str, classColour: tuple) -> None:
        """ Generates a class item """
        if className not in self._classes:
            self.addClassSelectionListItem(className, classColour)
            self._classes.append(className)

    def addClassSelectionListItem(self, className: str, classColour: tuple) -> None:
        """ Adds a classes item to the classes selection list widget """
        classItem = QTreeWidgetItem(self.classTreeWidget)
        classItem.setFlags(classItem.flags() & ~Qt.ItemFlag.ItemIsSelectable)
        classItem.setChildIndicatorPolicy(QTreeWidgetItem.ChildIndicatorPolicy.DontShowIndicatorWhenChildless)
        classWidget = ClassItemTreeWidget(
            className,
            classItem,
            self.classTreeWidget,
            classColour,
            self.themePaletteColours,
            self.fontRegular,
            self.fontTitle,
            app=self
        )

        self.classTreeWidget.setItemWidget(classItem, 0, classWidget)

    def getClass(self, className: str) -> Any:
        """ Finds an ML Class """
        for _class in self.app.project.classesDataset:
            if _class.className == className:
                return _class

    def generateAnnotationItems(self, image: Any) -> None:
        """ Generates annotation items for an image"""
        for annotation in image.boundingBoxes:
            self.generateAnnotationItem(annotation)

    def generateAnnotationItem(self, annotation: Any) -> None:
        """ Generates an annotation item """
        # Finding the annotation's class
        if annotation.className not in self._classes:
            # An annotation is dependent on its class item being present
            _class = self.getClass(annotation.className)
            self.generateClassItem(_class.className, _class.classColour)

        self.addAnnotationToClassItem(annotation.className, annotation.id)

    def addAnnotationToClassItem(self, className: str, annotationID: str) -> None:
        """ Adds an annotation item to a classes item """
        classItem = self.__findClassItem(className)
        annotationItem = QTreeWidgetItem(classItem)
        annotationWidget = AnnotationTreeItemWidget(str(annotationID), classItem, self.classTreeWidget, self.themePaletteColours)
        self.classTreeWidget.setItemWidget(annotationItem, 0, annotationWidget)

    def __setupStyleSheet(self) -> None:
        """ Configures the main layout of the annotation class selection frame. """
        self.utilityWidgetsFrame = self.__createUtilityWidgetsFrame()
        self.classSelectionFrame = self.__createClassSelectionFrame()
        layout = QVBoxLayout(self.ui.annotationClassSelectionFrame)
        layout.addWidget(self.utilityWidgetsFrame)
        layout.addWidget(self.classSelectionFrame)
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)

    def __createUtilityWidgetsFrame(self) -> QFrame:
        """ Configures the layout for the class selection utility frame. """
        frame = QFrame()
        frame.setMinimumSize(0, 30)
        frame.setMaximumSize(16777215, 30)

        self.classSearchLineEdit = self.__createSearchUtilityLineEdit()
        self.classAddAnnoPageBtn = self.__createAddClassButton()

        layout = QHBoxLayout(frame)
        layout.addWidget(self.classSearchLineEdit)
        layout.addWidget(self.classAddAnnoPageBtn)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)
        return frame

    def __createSearchUtilityLineEdit(self) -> CustomUserInputQLineEdit:
        """ Initializes the search bar for filtering class items. """
        lineEdit = CustomUserInputQLineEdit(self.themePaletteColours, self.fontRegular)
        lineEdit.setPlaceholderText('Search class...')
        lineEdit.setFixedSize(170, 25)
        lineEdit.setTextMargins(5, 0, 5, 0)
        lineEdit.editingFinished.connect(lambda: lineEdit.clearFocus())
        return lineEdit

    def __createAddClassButton(self) -> QPushButton:
        """ Initializes the button for adding new annotation classes. """
        pushButton = QPushButton("+ Class")
        pushButton.setFixedHeight(25)
        pushButton.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        pushButton.setStyleSheet(
            "QPushButton{"
            f"font: 75 bold 11pt {self.fontTitle};"
            f"background-color: {self.themePaletteColours['buttonFilled.background']};"
            "border-radius: 8px;}"
            "QPushButton::hover{"
            f"background-color : {self.themePaletteColours['buttonFilled.hover']};"
            f"color: {self.themePaletteColours['font.header']};}}"
        )
        return pushButton

    def __createClassSelectionFrame(self) -> QFrame:
        """ Initializes the list widget for class selection. """
        frame = QFrame()
        # frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        frame.setStyleSheet(
            "QFrame{"
            f"background: {self.themePaletteColours['panel.sunken']};}}"
        )

        self.classTreeWidget = self.__createClassTreeWidget()
        layout = QVBoxLayout(frame)
        layout.addWidget(self.classTreeWidget)
        layout.setContentsMargins(3,3,3,3)
        return frame

    def __createClassTreeWidget(self) -> QTreeWidget:
        treeWidget = QTreeWidget()
        treeWidget.setHeaderHidden(True)
        treeWidget.header().setMinimumSectionSize(0)
        treeWidget.setStyleSheet("""
            QTreeView::branch { background: transparent; }
            QTreeView::item {
                padding-left: -20px;
            }
        """)
        treeWidget.setExpandsOnDoubleClick(False)
        treeWidget.itemClicked.connect(self.__emitSelectionSignal)

        return treeWidget

    def __findClassItem(self, className: str) -> QTreeWidgetItem:
        classItem = None
        for i in range(self.classTreeWidget.topLevelItemCount()):  # Iterate over top-level items
            item = self.classTreeWidget.topLevelItem(i)
            classWidget = self.classTreeWidget.itemWidget(item, 0)
            if classWidget.className == className:
                classItem = item
                break  # Stop once we find the correct class

        # Step 2: If classItem is not found, return (or optionally create the class)
        if classItem is None:
            print(f"Class '{className}' not found!")  # Debugging

        return classItem

    def __emitSelectionSignal(self, item: QTreeWidgetItem):
        """Determine item type and emit appropriate signal."""
        if item.parent() is None:
            self.classItemSelected.emit(self.__getClassNameFromItem(item))
            self.__setClassItemToSelected(item)
        else:
            self.annotationItemSelected.emit(self.__getAnnotationNameFromItem(item))

    def __setClassItemToSelected(self, item) -> None:
        classWidget = self.classTreeWidget.itemWidget(item, 0)
        classWidget.setFrameToSelectedState(True)
        oldSelectedItem = self.__findClassItem(self.classSelected)
        if oldSelectedItem is not None:
            oldSelectedWidget = self.classTreeWidget.itemWidget(oldSelectedItem, 0)
            oldSelectedWidget.setFrameToSelectedState(False)
        self.classSelected = self.__getClassNameFromItem(item)

    def __getClassNameFromItem(self, item: QTreeWidgetItem) -> str:
        classWidget = self.classTreeWidget.itemWidget(item, 0)
        return classWidget.className

    def __getAnnotationNameFromItem(self, item: QTreeWidgetItem) -> str:
        annotationWidget = self.classTreeWidget.itemWidget(item, 0)
        return annotationWidget.annotationName

    def __searchForClass(self, searchInput: str) -> None:
        """ Searches and shows the class items that correspond to the text """
        for i in range(self.classTreeWidget.topLevelItemCount()):
            classItem = self.classTreeWidget.topLevelItem(i)
            classWidget = self.classTreeWidget.itemWidget(classItem, 0)

            if not classWidget:
                continue  # Just in case the item has no widget

            if not searchInput:
                classItem.setHidden(False)
            elif searchInput.lower() in classWidget.className.lower():
                classItem.setHidden(False)
            else:
                classItem.setHidden(True)

