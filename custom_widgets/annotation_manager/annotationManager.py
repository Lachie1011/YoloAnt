"""
    annotationManager.py
"""

from PyQt6 import QtCore
from typing import Any
from PyQt6.QtCore import pyqtSignal as Signal, Qt
from PyQt6.QtGui import QCursor, QColor
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QFrame, QTreeWidgetItem, QTreeWidget
from custom_widgets.customBaseObjects.customUserInputQLineEdit import CustomUserInputQLineEdit
from custom_widgets.annotation_manager.classTreeItemWidget import ClassTreeItemWidget
from custom_widgets.annotation_manager.annotationTreeItemWidget import AnnotationTreeItemWidget

class AnnotationManager(QFrame):
    """ A custom widget for the annotation class selection for selecting and searching for classes """
    classItemSelectedSignal = Signal(str)
    annotationItemSelectedSignal = Signal(str)
    annotationRemovedSignal = Signal(str)
    annotationHiddenSignal = Signal(str, bool)

    def __init__(self, app, ui, themePaletteColours: dict, fontRegular, fontTitle):
        super(AnnotationManager, self).__init__()

        # Member variables
        self.app = app
        self.ui = ui
        self.themePaletteColours = themePaletteColours
        self.fontRegular = fontRegular
        self.fontTitle = fontTitle

        self._classes = []
        self.classSelected = ""
        self.annotationSelected = ""

        # Setup stylesheet of frame
        self.__setupStyleSheet()

        # Connect signals and slots
        self.classSearchLineEdit.textChanged.connect(lambda searchInput: self.__searchForClass(searchInput))

    def reset(self) -> None:
        """ Clears all class and annotation items from the tree widget. """
        self.classTreeWidget.clear()
        self._classes = []

    def generateClassItems(self) -> None:
        """ Generates the class items for the widget """
        for _class in self.app.project.classesDataset:
            if _class.className not in self._classes:
                self.generateClassItem(_class.className, _class.classColour)

    def generateClassItem(self, className: str, classColour: tuple) -> None:
        """ Generates a class item """
        if className not in self._classes:
            self.addClass(className, classColour)
            self._classes.append(className)

    def addClass(self, className: str, classColour: tuple) -> None:
        """ Adds a class item to the class QTreeWidget """
        classItem = QTreeWidgetItem(self.classTreeWidget)
        classItem.setFlags(classItem.flags() & ~Qt.ItemFlag.ItemIsSelectable)
        classItem.setChildIndicatorPolicy(QTreeWidgetItem.ChildIndicatorPolicy.DontShowIndicatorWhenChildless)
        classWidget = ClassTreeItemWidget(
            className,
            classItem,
            self.classTreeWidget,
            classColour,
            self.themePaletteColours,
            self.fontRegular,
            self.fontTitle
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

        self.addAnnotationToClass(annotation.className, annotation.id)

    def addAnnotationToClass(self, className: str, annotationName: str) -> None:
        """ Adds an annotation item to a classes item """
        classItem = self.__findClassItem(className)
        annotationItem = QTreeWidgetItem(classItem)
        annotationWidget = AnnotationTreeItemWidget(
            str(annotationName),
            classItem,
            self.classTreeWidget,
            self.themePaletteColours
        )
        annotationWidget.annotationRemovedSignal.connect(self.annotationRemovedSignal.emit)
        annotationWidget.annotationHiddenSignal.connect(self.annotationHiddenSignal.emit)
        self.classTreeWidget.setItemWidget(annotationItem, 0, annotationWidget)

    def setEditMode(self, isEditable: bool) -> None:
        """ Sets the annotation manager to an editable state. """
        for classTreeItemIndex in range(self.classTreeWidget.topLevelItemCount()):
            classTreeItem = self.classTreeWidget.topLevelItem(classTreeItemIndex)
            classWidget = self.classTreeWidget.itemWidget(classTreeItem, 0)
            classWidget.setEditableState(isEditable)

    def __setupStyleSheet(self) -> None:
        """ Configures the layout of the annotation manager. """
        self.utilityWidgetsFrame = self.__createUtilityWidgetsFrame()
        self.classSelectionFrame = self.__createClassSelectionFrame()
        layout = QVBoxLayout(self.ui.annotationClassSelectionFrame)
        layout.addWidget(self.utilityWidgetsFrame)
        layout.addWidget(self.classSelectionFrame)
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)

    def __createUtilityWidgetsFrame(self) -> QFrame:
        """ Creates the Utility Widgets Frame. """
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
        """Creates the QLineEdit used to filter class items."""
        lineEdit = CustomUserInputQLineEdit(self.themePaletteColours, self.fontRegular)
        lineEdit.setPlaceholderText('Search class...')
        lineEdit.setFixedSize(170, 25)
        lineEdit.setTextMargins(5, 0, 5, 0)
        lineEdit.editingFinished.connect(lambda: lineEdit.clearFocus())
        return lineEdit

    def __createAddClassButton(self) -> QPushButton:
        """ Creates the add class button. """
        pushButton = QPushButton("+ Class")
        pushButton.setFixedHeight(25)
        pushButton.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        pushButton.setStyleSheet(f"""
            QPushButton {{
                font: 75 bold 11pt {self.fontTitle};
                background-color: {self.themePaletteColours['buttonFilled.background']};
                border-radius: 8px;
            }}
            QPushButton::hover {{
                background-color: {self.themePaletteColours['buttonFilled.hover']};
                color: {self.themePaletteColours['font.header']};
            }}
        """)
        return pushButton

    def __createClassSelectionFrame(self) -> QFrame:
        """ Creates the class selection frame. """
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background: {self.themePaletteColours['panel.sunken']};
            }}
        """)

        self.classTreeWidget = self.__createClassTreeWidget()
        layout = QVBoxLayout(frame)
        layout.addWidget(self.classTreeWidget)
        layout.setContentsMargins(3,3,3,3)
        return frame

    def __createClassTreeWidget(self) -> QTreeWidget:
        """ Creates the QTreeWidget used to show class and annotation items. """
        treeWidget = QTreeWidget()
        treeWidget.setHeaderHidden(True)
        treeWidget.setIndentation(0)
        treeWidget.header().setMinimumSectionSize(0)
        treeWidget.setStyleSheet("""
            QTreeView::branch {
                background: transparent;
            }

            QTreeView::item {
                background: transparent;
                selection-background-color: transparent;
            }

            QScrollBar:vertical {
                border: none;
                width: 10px;
                margin: 15px 0 15px 0;
                border-radius: 0px;
            }

            QScrollBar::handle:vertical {
                background-color: rgb(80, 80, 80);
                min-height: 30px;
                border-radius: 4px;
            }

            QScrollBar::handle:vertical:pressed {
                background-color: rgb(185, 0, 92);
            }

            QScrollBar::sub-line:vertical,
            QScrollBar::add-line:vertical {
                border: none;
                background: none;
                color: none;
            }
        """)

        treeWidget.setExpandsOnDoubleClick(False)
        treeWidget.itemClicked.connect(self.__emitSelectionSignal)
        return treeWidget

    def __findClassItem(self, className: str) -> QTreeWidgetItem:
        """ Returns the classTreeItem. """
        for classTreeItemIndex in range(self.classTreeWidget.topLevelItemCount()):
            classTreeItem = self.classTreeWidget.topLevelItem(classTreeItemIndex)
            classWidget = self.classTreeWidget.itemWidget(classTreeItem, 0)
            if classWidget and classWidget.className == className:
                return classTreeItem
        return None

    def __findAnnotationItem(self, annotationName: str) -> QTreeWidgetItem:
        """ Searches all class items for a child annotation item with the given name. """

        def searchClassAnnotations(classTreeItem):
            """ Recursively searches for the annotation item among the children. """
            for i in range(classTreeItem.childCount()):
                annotationTreeItem = classTreeItem.child(i)
                annotationWidget = self.classTreeWidget.itemWidget(annotationTreeItem, 0)
                if annotationWidget and annotationWidget.annotationName == annotationName:
                    return annotationTreeItem
                # Recursively search in the child's children
                result = searchClassAnnotations(annotationTreeItem)
                if result:
                    return result
            return None

        for classTreeItemIndex in range(self.classTreeWidget.topLevelItemCount()):
            classTreeItem = self.classTreeWidget.topLevelItem(classTreeItemIndex)
            result = searchClassAnnotations(classTreeItem)
            if result:
                return result
        return None

    def __emitSelectionSignal(self, item: QTreeWidgetItem):
        """ Determine tree item type and emit appropriate signal. """
        if item.parent() is None:
            className = self.__getClassNameFromItem(item)
            classColour = self.__getClassColourFromItem(item)
            if self.classSelected != className:
                self.classItemSelectedSignal.emit(self.__getClassNameFromItem(item))
                self.__setClassItemToSelected(item)
                self.app.ui.annotationCanvas.currentClassName = className
                self.app.ui.annotationCanvas.currentClassColour = QColor(
                    int(classColour[0]), int(classColour[1]), int(classColour[2])
                )

        else:
            annotationName = self.__getAnnotationNameFromItem(item)
            if self.annotationSelected != annotationName:
                self.annotationItemSelectedSignal.emit(self.__getAnnotationNameFromItem(item))
                self.__setAnnotationItemToSelected(item)

    def __setClassItemToSelected(self, item) -> None:
        """ Updates class selection visuals and internal state. """
        classWidget = self.classTreeWidget.itemWidget(item, 0)
        classWidget.setFrameToSelectedState(True)

        oldClassSelectedItem = self.__findClassItem(self.classSelected)
        if oldClassSelectedItem:
            oldClassSelectedWidget = self.classTreeWidget.itemWidget(oldClassSelectedItem, 0)
            oldClassSelectedWidget.setFrameToSelectedState(False)
        className = self.__getClassNameFromItem(item)
        self.classSelected = className

    def __getClassNameFromItem(self, item: QTreeWidgetItem) -> str:
        """ Returns class name of class tree widget item. """
        return self.classTreeWidget.itemWidget(item, 0).className

    def __getClassColourFromItem(self, item: QTreeWidgetItem) -> tuple:
        """ Returns class name of class tree widget item. """
        return self.classTreeWidget.itemWidget(item, 0).colour

    def __setAnnotationItemToSelected(self, item) -> None:
        """ Updates annotation selection visuals and internal state. """
        annotationWidget = self.classTreeWidget.itemWidget(item, 0)
        annotationWidget.setFrameToSelectedState(True)

        oldAnnotationSelectedItem = self.__findAnnotationItem(self.annotationSelected)
        if oldAnnotationSelectedItem is not None:
            oldAnnotationSelectedWidget = self.classTreeWidget.itemWidget(oldAnnotationSelectedItem, 0)
            oldAnnotationSelectedWidget.setFrameToSelectedState(False)
        annotationName = self.__getAnnotationNameFromItem(item)
        self.annotationSelected = annotationName

    def __getAnnotationNameFromItem(self, item: QTreeWidgetItem) -> str:
        """ Returns annotation name of annotation tree widget item. """
        return self.classTreeWidget.itemWidget(item, 0).annotationName

    def __searchForClass(self, searchInput: str) -> None:
        """ Filters class items based on search input. """
        for classTreeItemIndex in range(self.classTreeWidget.topLevelItemCount()):
            classTreeItem = self.classTreeWidget.topLevelItem(classTreeItemIndex)
            classWidget = self.classTreeWidget.itemWidget(classTreeItem, 0)

            if not searchInput:
                classTreeItem.setHidden(False)
            elif searchInput.lower() in classWidget.className.lower():
                classTreeItem.setHidden(False)
            else:
                classTreeItem.setHidden(True)

