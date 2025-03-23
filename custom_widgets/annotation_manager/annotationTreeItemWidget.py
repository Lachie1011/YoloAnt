"""
    annotationTreeItemWidget.py
"""
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QFrame, QHBoxLayout,
    QVBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import pyqtSignal as Signal
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt


class AnnotationTreeItemWidget(QWidget):
    """ The QWidget that is for a annotation tree item. """
    annotationRemovedSignal = Signal(str)
    annotationHiddenSignal = Signal(str, bool)

    def __init__(self, annotationName, parentTreeItem, treeWidget, themePaletteColours):
        super().__init__()
        self.annotationName = annotationName
        self.parentTreeItem = parentTreeItem
        self.treeWidget = treeWidget
        self.themePaletteColours = themePaletteColours
        self.isSelected = False

        self.__setupStyleSheet()
        self.hideAnnotationBtn.clicked.connect(lambda: self.__hideAnnotation())

    def enterEvent(self, event) -> None:
        """ Overrides enterEvent to change stylesheet on hover. """
        if not self.isSelected:
            self.frame.setStyleSheet(self.__getFrameStyle(hover=True, selected=False))

    def leaveEvent(self, event) -> None:
        """ Overrides leaveEvent to change stylesheet on hover. """
        if not self.isSelected:
            self.frame.setStyleSheet(self.__getFrameStyle(hover=False, selected=False))

    def setFrameToSelectedState(self, isSelected: bool) -> None:
        """ Sets frame to selected state """
        self.isSelected = isSelected
        self.frame.setStyleSheet(self.__getFrameStyle(hover=False, selected=isSelected))

    def __setupStyleSheet(self):
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setFixedHeight(60)

        self.frame = QFrame()
        self.frame.setObjectName("annotationFrame")
        self.frame.setStyleSheet(self.__getFrameStyle())

        self.annotationNameLbl = self.__createAnnotationNameLabel()
        self.hideAnnotationBtn = self.__createHideButton()
        self.annotationDeleteButton = self.__createDeleteButton()
        spacer1 = QSpacerItem(15, 5, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        spacer2 = QSpacerItem(15, 5, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        frameLayout = QHBoxLayout(self.frame)
        frameLayout.setContentsMargins(10, 5, 10, 5)
        frameLayout.setSpacing(8)
        frameLayout.addItem(spacer1)
        frameLayout.addWidget(self.annotationNameLbl)
        frameLayout.addItem(spacer2)
        frameLayout.addWidget(self.hideAnnotationBtn)
        frameLayout.addWidget(self.annotationDeleteButton)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.frame)

    def __getFrameStyle(self, hover=False, selected=False) -> str:
        border = f"2px solid {self.themePaletteColours['focus.foreground']}" if hover or selected else "none"
        return f"""
            QFrame#annotationFrame {{
                background-color: transparent;
                border: {border};
                border-radius: 6px;
            }}
        """

    def __createAnnotationNameLabel(self) -> QLabel:
        """ Creates the annotation label. """
        label = QLabel(self.annotationName)
        label.setStyleSheet(f"color: {self.themePaletteColours['font.regular']};")
        label.setMinimumSize(100, 30)
        return label

    def __createHideButton(self) -> QPushButton:
        """ Creates the hide annotation button. """
        button = QPushButton()
        button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border-image: url('icons/icons8-eye-open-25.png');
            }
            QPushButton:hover {
                border-image: url('icons/icons8-eye-open-hover-25.png');
            }
        """)
        button.setFixedSize(20, 20)
        button.setCheckable(True)
        button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        return button

    def __hideAnnotation(self) -> None:
        """ Changes the icon depending on checked status and emits signal. """
        self.annotationHiddenSignal.emit(
            self.annotationName,
            self.hideAnnotationBtn.isChecked()
        )
        if self.hideAnnotationBtn.isChecked():
            self.hideAnnotationBtn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border-image: url('icons/icons8-eye-closed-25.png');
                }
                QPushButton:hover {
                    border-image: url('icons/icons8-eye-closed-hover-25.png');
                }
            """)
        else:
            self.hideAnnotationBtn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border-image: url('icons/icons8-eye-open-25.png');
                }
                QPushButton:hover {
                    border-image: url('icons/icons8-eye-open-hover-25.png');
                }
            """)


    def __createDeleteButton(self) -> QPushButton:
        """ Creates the delete annotation button. """
        button = QPushButton()
        button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border-image: url('icons/icons8-trash-can-25.png');
            }
        """)
        button.setFixedSize(18, 18)
        button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        button.clicked.connect(self.__deleteAnnotation)
        return button

    def __deleteAnnotation(self):
        """ Emits the delete signal and removes this item from the tree widget. """
        self.annotationRemovedSignal.emit(self.annotationName)

        if self.parentTreeItem is not None:
            for i in range(self.parentTreeItem.childCount()):
                child_item = self.parentTreeItem.child(i)
                widget = self.treeWidget.itemWidget(child_item, 0)
                if widget == self:
                    self.parentTreeItem.removeChild(child_item)
                    del child_item
                    break
            if self.parentTreeItem.childCount() == 0:
                self.parentTreeItem.setExpanded(False)
