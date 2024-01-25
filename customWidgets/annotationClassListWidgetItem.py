"""
    classListItemWidget.py
"""

from PyQt6.QtCore import Qt, QParallelAnimationGroup, QAbstractAnimation, QPropertyAnimation
from PyQt6.QtGui import QCursor 
from PyQt6.QtWidgets import (QScrollArea, QWidget, QFrame, QLabel, QHBoxLayout, QLineEdit, QProgressBar, 
                             QSpacerItem, QSizePolicy, QPushButton, QToolButton, QVBoxLayout,
                             QAbstractItemView, QListWidgetItem, QSizePolicy, QListWidget, QAbstractScrollArea)

class ClassListItemWidget (QFrame):
    """
        Class that creates a custom class item widget for class list

        params:
            className - Name of class
            numClassAnnotations  - Number of annotataions in dataset of this class type
            numOfAnnotations - Number of classes in the dataset 
            colour - Annotation colour of class in RGB format: _,_,_ 
    """
    def __init__(self, className, numClassAnnotations, numOfAnnotations, colour, parent=None):
        super(ClassListItemWidget, self).__init__(parent)

        # Hover style sheet
        self.parentSelected = False
        self.className = className
        self.setStyleSheet("QFrame{border-radius: 4px; border: 3px solid rgb(105, 105, 105)}")
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        self.setMaximumHeight(1000)

        self.classSelectionFrame = self.__setUpClassSelectionFrame()
        self.annotationFrameFrame = self.__setUpAnnotationsFrame()
        self.annotationListLayout = QVBoxLayout()
        self.annotationListLayout.addWidget(self.classSelectionFrame)
        self.annotationListLayout.addWidget(self.annotationFrameFrame)
        self.annotationListLayout.setContentsMargins(0,0,0,0)
        self.annotationListLayout.setSpacing(0)
        self.annotationListLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.toolBtn.clicked.connect(lambda checked: self.__expandFrame(checked))
        # self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.setLayout(self.annotationListLayout)
        # self.setContentsMargins(0, 0, 0, 0)
        # self.classColourButton.clicked.connect(lambda: self.selectColour())

    def __setUpClassSelectionFrame(self) -> QFrame:
        """ Sets up style sheet of item widget """
        classSelectionFrame = QFrame()
        classSelectionFrame.setFixedHeight(25)

        # Colour picker label
        self.toolBtn = QToolButton()
        self.toolBtn.setStyleSheet("QLabel{"
                                          "border-radius: 4px;"
                                          "border: 3px solid rgb(105, 105, 105)}")
        self.toolBtn.setFixedWidth(18)
        self.toolBtn.setFixedHeight(18)

        self.toolBtn.setCheckable(True)
        self.toolBtn.setChecked(False)

        # Setting layout of custom widget 
        classItemWidetLayout = QHBoxLayout()
        classItemWidetLayout.addWidget(self.toolBtn)
        classItemWidetLayout.setContentsMargins(0,0,0,0)
        classSelectionFrame.setLayout(classItemWidetLayout)

        classSelectionFrame.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        return classSelectionFrame

    def __setUpAnnotationsFrame(self) -> QFrame:
        self.annotationFrame = Expander()
        self.testLayout = QVBoxLayout()
        self.testLabel = QLabel('Hello')
        self.testLayout.addWidget(self.testLabel)
        self.testLayout.setContentsMargins(0,0,0,0)
        self.annotationFrame.setLayout(self.testLayout)
        return self.annotationFrame.expandFrame

    def __expandFrame(self, checked):
        self.annotationFrame.start_animation(checked)

        if checked: 
            self.annotationFrameFrame.setFixedHeight(self.testLayout.sizeHint().height())
            self.setFixedHeight(self.height() + self.testLayout.sizeHint().height())

        else: 
            self.annotationFrameFrame.setFixedHeight(0)
            self.setFixedHeight(self.height() - self.testLayout.sizeHint().height())

        if self.parentItem:
            self.parentItem.setSizeHint(self.sizeHint())

    def setParentItem(self, parentItem):
        self.parentItem = parentItem

    def enableEdit(self) -> None:
        """ Sets the item widget to edit mode """
        self.parentSelected = True
        # self.setStyleSheet(self.styleSheet() + "background: rgb(85, 87, 83);")
        # self.classItemLbl.setVisible(False)
        # self.classItemLineEdit.setVisible(True)
        # self.classColourLbl.setVisible(False)
        # self.classColourButton.setVisible(True)
        # self.classDeleteLbl.setVisible(False)
        # self.classDeleteButton.setVisible(True)
        # self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        
    def disableEdit(self) -> None:
        """ Disables edit mode of item widget """
        self.parentSelected = False
        # self.setStyleSheet(self.styleSheet() + "background: rgb(65, 66, 64);")
        # self.classItemLbl.setVisible(True)
        # self.classItemLineEdit.setVisible(False)
        # self.classColourLbl.setVisible(True)
        # self.classColourButton.setVisible(False)
        # self.classDeleteLbl.setVisible(True)
        # self.classDeleteButton.setVisible(False)
        # self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

class WidgetItemLineEdit(QLineEdit):
    def __init__(self):
        super().__init__()
   
    def focusInEvent(self, event):
        """ Sets background colour of widget when it is focused """
        super(WidgetItemLineEdit, self).focusInEvent(event)
        self.setStyleSheet("QLineEdit{"
                           "font: 14pt 'Gotham Rounded Light';"
                           "background-color: rgb(105,105,105);}"
                           "QLineEdit:hover{"
                           "background-color: rgb(105, 105, 105);}")

    def focusOutEvent(self, event):
        """ Sets background colour of widget when it loses focus """
        super(WidgetItemLineEdit, self).focusOutEvent(event)
        self.setStyleSheet("QLineEdit{"
                           "font: 14pt 'Gotham Rounded Light';"
                           "background-color: rgb(85, 87, 83);}"
                           "QLineEdit:hover{"
                           "background-color: rgb(105, 105, 105);}")

class ClassListWidget (QListWidget):
    """
        Class that creates a custom list widget
    """
    def __init__(self):
        super().__init__()

        # Setup list widget
        self.setMinimumSize(0, 0)
        self.setFixedHeight(50)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
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


class Expander(QWidget):
    def __init__(self, parent=None, animationDuration=100):
        super().__init__()

        self.animationDuration = animationDuration
        self.toggleAnimation = QParallelAnimationGroup()
        self.expandFrame = QFrame()

        # Start collapsed
        self.expandFrame.setMinimumHeight(0)
        self.expandFrame.setMaximumHeight(0)

        # Expand and shrink with contents

        # toggleAnimation.addAnimation(QPropertyAnimation(self, b"minimumHeight"))
        # toggleAnimation.addAnimation(QPropertyAnimation(self, b"maximumHeight"))
        self.toggleAnimation.addAnimation(QPropertyAnimation(self.expandFrame, b"maximumHeight"))

    def start_animation(self, checked):
        # arrow_type = QtCore.Qt.ArrowType.DownArrow if checked else QtCore.Qt.ArrowType.RightArrow
        direction = QAbstractAnimation.Direction.Forward if checked else QAbstractAnimation.Direction.Backward
        # toggleButton.setArrowType(arrow_type)
        self.toggleAnimation.setDirection(direction)
        self.toggleAnimation.start()

    def setLayout(self, contentLayout):
        """
        Set the layout container that you would like to expand/collapse.
        This should be called after all styles are set.
        """
        self.contentLayout = contentLayout
        self.expandFrame.destroy()
        self.expandFrame.setLayout(contentLayout)
        collapsedHeight = 0
        contentHeight = contentLayout.sizeHint().height()
        for i in range(self.toggleAnimation.animationCount()-1):
            spoilerAnimation = self.toggleAnimation.animationAt(i)
            spoilerAnimation.setDuration(self.animationDuration)
            spoilerAnimation.setStartValue(collapsedHeight)
            spoilerAnimation.setEndValue(collapsedHeight + contentHeight)
        contentAnimation = self.toggleAnimation.animationAt(self.toggleAnimation.animationCount() - 1)
        contentAnimation.setDuration(self.animationDuration)
        contentAnimation.setStartValue(0)
        contentAnimation.setEndValue(contentHeight)



class AnnotationMenuTest(QMainWindow):
    """
        Class that creates the yoloant application
    """
    def __init__(self) -> None:
        """ init """
        super().__init__()

        self.ui = Ui_MainWindow()        
        self.ui.setupUi(self)

        self.classListWidget = ClassListWidget()
        self.classListWidget.setObjectName("classListProjectPageWidget")
        self.classListLayout = QVBoxLayout()
        self.classListLayout.addWidget(self.classListWidget)
        self.ui.classesFrame.setLayout(self.classListLayout)

        self.classListWidget.addItemToListWidget("Test", 10, 30, (0, 201, 52))
        self.classListWidget.addItemToListWidget("Test", 10, 30, (0, 201, 52))