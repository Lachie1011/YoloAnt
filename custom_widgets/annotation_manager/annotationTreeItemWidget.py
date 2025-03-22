from PyQt6.QtWidgets import (
    QApplication, QFrame, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTreeWidget, QTreeWidgetItem, QWidget, QSpacerItem, QSizePolicy
)
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt
import sys

class AnnotationTreeItemWidget(QWidget):
    """
    A QWidget representing an annotation item with a delete button.
    """
    def __init__(self, annotationName, parentTreeItem, treeWidget, themePaletteColours):
        super().__init__()
        self.annotationName = annotationName
        self.parentTreeItem = parentTreeItem
        self.treeWidget = treeWidget
        self.themePaletteColours = themePaletteColours
        self.__setupStyleSheet()

    def enterEvent(self, event) -> None:
        """ Sets background of widget when mouse enters item widget """
        if not self.parentItem.isSelected():
            self.annotationNameLbl.setStyleSheet("QLabel{"
                                                 f"color: {self.themePaletteColours['font.hover']};}}")

    def leaveEvent(self, event) -> None:
        """ Sets background of widget when mouse leaves item widget """
        if not self.parentItem.isSelected():
            self.annotationNameLbl.setStyleSheet("QLabel{"
                                                 f"color: {self.themePaletteColours['font.regular']};}}")

    def setSelected(self) -> None:
        """ Sets list widget item to selected state """
        self.annotationNameLbl.setStyleSheet("QLabel{"
                                             f"color: {self.themePaletteColours['font.hover']};}}")
        self.parentSelected = True
        self.selected.emit(self.annotationName)

    def clearSelected(self) -> None:
        """ Clears selected state of list widget item """
        self.annotationNameLbl.setStyleSheet("QLabel{"
                                             f"color: {self.themePaletteColours['font.regular']};}}")
        self.parentSelected = False

    def deleteAnnotation(self):
        """Deletes this annotation from the parent class."""
        if self.parentTreeItem is not None:
            for i in range(self.parentTreeItem.childCount()):
                child_item = self.parentTreeItem.child(i)
                widget = self.treeWidget.itemWidget(child_item, 0)  # Get widget associated with item
                if widget == self:
                    self.parentTreeItem.removeChild(child_item)  # Remove from tree structure
                    del child_item  # Free memory
                    break  # Exit loop after deletion

            # If no more annotations exist under the class, collapse it
            if self.parentTreeItem.childCount() == 0:
                self.parentTreeItem.setExpanded(False)


    def __setupStyleSheet(self) -> None:
        """ Sets up style sheet for annotation selection frame """
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setFixedHeight(60)

        self.annotationNameLbl = self.__createAnnotationNameLabel()
        self.hideAnnotationBtn = self.__createHideButton()
        self.annotationDeleteButton = self.__createDeleteButton()

        # Horizontal spacers
        spacer1 = QSpacerItem(15, 5, QSizePolicy.Policy.Fixed)
        spacer2 = QSpacerItem(15, 5, QSizePolicy.Policy.Fixed)

        # Setting layout of custom widget
        layout = QHBoxLayout(self)
        layout.addItem(spacer1)
        layout.addWidget(self.annotationNameLbl)
        layout.addItem(spacer2)
        layout.addWidget(self.hideAnnotationBtn)
        layout.addWidget(self.annotationDeleteButton)

    def __createAnnotationNameLabel(self) -> QLabel:
        """ Creates the annotation name label. """
        label = QLabel(self.annotationName)
        label.setStyleSheet("QLabel{"
                                             f"color: {self.themePaletteColours['font.regular']};}}")
        label.setMinimumSize(100, 30)
        return label

    def __createHideButton(self) -> QPushButton:
        button = QPushButton()
        button.setStyleSheet("QPushButton{"
                                             "background-color: transparent;"
                                             "border-image: url('icons/icons8-eye-open-25.png');}"
                                             "QPushButton:hover{"
                                             "border-image: url('icons/icons8-eye-open-hover-25.png');}")
        button.setFixedWidth(20)
        button.setFixedHeight(20)
        button.setCheckable(True)
        button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        return button

    def __displayedHideAnnotationIcon(self) -> None:
        """ Changes the icon depending on checked status """
        if self.hideAnnotationBtn.isChecked():
            self.hideAnnotationBtn.setStyleSheet("QPushButton{"
                                                 "background-color: transparent;"
                                                 "border-image: url('icons/icons8-eye-closed-25.png');}"
                                                 "QPushButton:hover{"
                                                 "border-image: url('icons/icons8-eye-closed-hover-25.png');}")

        else:
            self.hideAnnotationBtn.setStyleSheet("QPushButton{"
                                                 "background-color: transparent;"
                                                 "border-image: url('icons/icons8-eye-open-25.png');}"
                                                 "QPushButton:hover{"
                                                 "border-image: url('icons/icons8-eye-open-hover-25.png');}")

    def __createDeleteButton(self) -> QPushButton:
        button = QPushButton()
        button.setStyleSheet("QPushButton{"
                                                  "border-image: url('icons/icons8-trash-can-25.png');}")
        button.setFixedWidth(18)
        button.setFixedHeight(18)
        button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        button.clicked.connect(self.deleteAnnotation)
        return button

