"""
    annotationManager.py
"""

from PyQt6 import QtCore
from typing import Any, cast
from PyQt6.QtCore import pyqtSignal as Signal, Qt
from PyQt6.QtGui import QCursor, QColor
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QFrame, QTreeWidgetItem, QTreeWidget
from custom_widgets.customBaseObjects.customUserInputQLineEdit import CustomUserInputQLineEdit
from custom_widgets.annotation_manager.classItem import ClassItem
from custom_widgets.annotation_manager.annotationItem import AnnotationItem
from ui.annotationManager_ui import Ui_annotationManagerFrame

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
        self.classItemSelected = None
        self.annotationItemSelected = None

        # Setup stylesheet of frame
        self.annotationManagerFrame = Ui_annotationManagerFrame()
        self.annotationManagerFrame.setupUi(self)
        self.classSearchLineEdit = self.annotationManagerFrame.classSearchLineEdit
        self.classSearchLineEdit.setPlaceholderText('Search class...')
        self.classAddAnnoPageBtn = self.annotationManagerFrame.annoManagerCreateClassBtn
        self.classTreeWidget = self.annotationManagerFrame.classSelectionTreeWidget
        # self.__setupStyleSheet()

        # Connect signals and slots
        self.classSearchLineEdit.textChanged.connect(lambda searchInput: self.__searchForClass(searchInput))

    def reset(self) -> None:
        """ Clears all class and annotation items from the tree widget. """
        self.classItemSelected = None
        self.annotationItemSelected = None
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
            # self.addClassItem(className, classColour)
            self._classes.append(className)

    def addClassItem(self, className: str, classColour: tuple) -> None:
        """ Adds a class item to the class QTreeWidget """
        ClassItem(
            className,
            self.classTreeWidget,
            classColour,
            self.themePaletteColours,
            self.fontRegular,
            self.fontTitle
        )

    def getClass(self, className: str) -> Any:
        """ Finds an ML Class """
        for _class in self.app.project.classesDataset:
            if _class.className == className:
                return _class

    def clearClassSelection(self) -> None:
        self.classItemSelected.setFrameToSelectedState(False)
        self.classItemSelected = None

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

        self.addAnnotationItem(annotation.className, annotation.id)

    def addAnnotationItem(self, className: str, annotationID: int) -> None:
        """ Adds an annotation item to a classes item """
        classItem = self.__findClassItem(className)
        annotationItem = AnnotationItem(
            annotationID,
            classItem,
            self.classTreeWidget,
            self.themePaletteColours
        )
        annotationItem.connectSignals(
            lambda id: self.annotationRemovedSignal.emit(id),
            lambda id, hidden: self.annotationHiddenSignal.emit(id, hidden)
        )

    def setAnnotationToSelected(self, className: str, annotationID: int) -> None:
        """ Sets a specific annotation as selected by class and annotation ID. """
        classItem = self.__findClassItem(className)
        if not classItem:
            print(f"[AnnotationManager] Class '{className}' not found.")
            return

        for annotationItemIndex in range(classItem.childCount()):
            annotationItem = classItem.child(annotationItemIndex)
            if annotationItem.annotationID == annotationID:
                if self.annotationItemSelected != annotationItem:
                    self.__setAnnotationItemToSelected(annotationItem)
                    classItem.showAnnotations(True)
                return

        print(f"[AnnotationManager] Annotation ID '{annotationID}' not found under class '{className}'.")

    def clearAnnotationSelection(self) -> None:
        self.annotationItemSelected.setFrameToSelectedState(False)
        self.annotationItemSelected = None

    def setEditMode(self, isEditable: bool) -> None:
        """ Sets the annotation manager to an editable state. """
        for classTreeItemIndex in range(self.classTreeWidget.topLevelItemCount()):
            classTreeItem = self.classTreeWidget.topLevelItem(classTreeItemIndex)
            classWidget = self.classTreeWidget.itemWidget(classTreeItem, 0)
            classWidget.setEditableState(isEditable)

    def __setupStyleSheet(self) -> None:
        """ Configures the layout of the annotation manager. """
        self.utilityWidgetsFrame = self.__createUtilityFrame()
        self.classSelectionFrame = self.__createClassSelectionFrame()
        layout = QVBoxLayout(self.ui.annotationClassSelectionFrame)
        layout.addWidget(self.utilityWidgetsFrame)
        layout.addWidget(self.classSelectionFrame)
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)

    # def __loadUiFile(self) -> None:
    #     """ Loads in the utility frame. """



    def __createClassSelectionFrame(self) -> QFrame:
        """ Creates the class selection frame. """
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.NoFrame)
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

    def __findClassItem(self, className: str) -> ClassItem:
        """ Returns the classTreeItem. """
        for classItemIndex in range(self.classTreeWidget.topLevelItemCount()):
            classItem = self.classTreeWidget.topLevelItem(classItemIndex)
            if classItem.className == className:
                return cast(ClassItem, classItem)
        return None

    def __emitSelectionSignal(self, item: QTreeWidgetItem):
        """ Determine tree item type and emit appropriate signal. """
        self.ensurePolished()
        if item.parent() is None:
            classItem = cast(ClassItem, item)
            if self.classItemSelected != classItem:
                self.__setClassItemToSelected(classItem)
                self.classItemSelectedSignal.emit(classItem.className)

                # Update annotation canvas
                colour = classItem.colour
                self.app.ui.annotationCanvas.currentClassName = classItem.className
                self.app.ui.annotationCanvas.currentClassColour = QColor(
                    int(colour[0]), int(colour[1]), int(colour[2])
                )

        else:
            annotationItem = cast(AnnotationItem, item)
            if self.annotationItemSelected != annotationItem:
                self.__setAnnotationItemToSelected(annotationItem)
                self.annotationItemSelectedSignal.emit(str(annotationItem.annotationID))

    def __setClassItemToSelected(self, item: ClassItem) -> None:
        """ Updates class selection visuals and internal state. """
        if self.classItemSelected:
            self.classItemSelected.setFrameToSelectedState(False)
        self.classItemSelected = item
        item.setFrameToSelectedState(True)

    def __setAnnotationItemToSelected(self, item: AnnotationItem) -> None:
        """ Updates annotation selection visuals and internal state. """
        if self.annotationItemSelected:
            self.annotationItemSelected.setFrameToSelectedState(False)
        self.annotationItemSelected = item
        item.setFrameToSelectedState(True)

    def __searchForClass(self, searchInput: str) -> None:
        """ Filters class items based on search input. """
        for classItemIndex in range(self.classTreeWidget.topLevelItemCount()):
            classItem = self.classTreeWidget.topLevelItem(classItemIndex)

            if not searchInput:
                classItem.setHidden(False)
            elif searchInput.lower() in classItem.className.lower():
                classItem.setHidden(False)
            else:
                classItem.setHidden(True)

