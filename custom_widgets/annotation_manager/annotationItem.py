"""
    annotationTreeItemWidget.py
"""
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QFrame, QHBoxLayout,
    QVBoxLayout, QSpacerItem, QSizePolicy, QTreeWidgetItem, QTreeWidget
)
from PyQt6.QtCore import pyqtSignal as Signal
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt

from custom_widgets.annotation_manager.classItem import ClassItem


class AnnotationItem(QTreeWidgetItem):
    """ A class for creating an annotation item """
    annotationRemovedSignal = Signal(str)
    annotationHiddenSignal = Signal(str, bool)

    def __init__(
            self,
            annotationID: int,
            classItem: ClassItem,
            treeWidget: QTreeWidget,
            themePaletteColours
    ):
        super().__init__(classItem)
        self.annotationID = annotationID
        self.treeWidget = treeWidget
        self.classItem = classItem
        self.themePaletteColours = themePaletteColours
        self.isSelected = False

        self.__setupStyleSheet(treeWidget)
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

    def connectSignals(self, onRemove, onHide):
        """
        Allows external code to connect callbacks to the delete and hide buttons.
        Usage:
            annotationItem.connectSignals(lambda id: ..., lambda id, hidden: ...)
        """
        self.onDelete = onRemove
        self.onHide = onHide

    def __setupStyleSheet(self, treeWidget: QTreeWidget) -> None:
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

        widget = QWidget()
        widget.setStyleSheet(f"""
            QWidget{{
                background: {self.themePaletteColours['app.sunken']};
            }}
        """)
        widget.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        widget.setFixedHeight(60)
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.frame)
        treeWidget.setItemWidget(self, 0, widget)

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
        label = QLabel(str(self.annotationID))
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
        if hasattr(self, "onHide"):
            self.onHide(str(self.annotationID), self.hideAnnotationBtn.isChecked())

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
        if hasattr(self, "onRemove"):
            self.onDelete(str(self.annotationID))
        self.classItem.removeChild(self)
        if self.classItem.childCount() == 0:
            self.classItem.setExpanded(False)

