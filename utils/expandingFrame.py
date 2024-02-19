"""
    expandingFrame.py
"""
from PyQt6.QtWidgets import QWidget, QFrame
from PyQt6.QtCore import QParallelAnimationGroup, QAbstractAnimation, QPropertyAnimation


class ExpandingFrame(QFrame):
    """
        Class that creates an expanding/shrinking frame from a layout

        params:
            contentLayout - Layout that will be inside the expanding/shrinking frame
    """
    def __init__(self, contentLayout, parent=None, animationDuration=0):
        super().__init__()

        # Expanding/shrinking animation variables
        self.animationDuration = animationDuration
        self.contentLayout = contentLayout
        self.toggleAnimation = QParallelAnimationGroup()

        # Start frame collapsed
        self.setMinimumHeight(0)
        self.setMaximumHeight(0)

        # Expand and shrink frame with contents
        self.toggleAnimation.addAnimation(QPropertyAnimation(self, b"maximumHeight"))
        self.__setFrameLayout()

    def __setFrameLayout(self):
        """
            Set the layout of the expanding/shrinking frame
        """
        self.destroy()
        self.setLayout(self.contentLayout)

        collapsedHeight = 0
        contentHeight = self.contentLayout.sizeHint().height()

        for animationFrame in range(self.toggleAnimation.animationCount()-1):
            spoilerAnimation = self.toggleAnimation.animationAt(animationFrame)
            spoilerAnimation.setDuration(self.animationDuration)
            spoilerAnimation.setStartValue(collapsedHeight)
            spoilerAnimation.setEndValue(collapsedHeight + contentHeight)

        contentAnimation = self.toggleAnimation.animationAt(self.toggleAnimation.animationCount() - 1)
        contentAnimation.setDuration(self.animationDuration)
        contentAnimation.setStartValue(0)
        contentAnimation.setEndValue(contentHeight)

    def start_animation(self, checked):
        """
            Starts the expanding/shrinking animation from a checkable button
        """
        if checked:
            direction = QAbstractAnimation.Direction.Forward
        else:
            direction = QAbstractAnimation.Direction.Backward
        
        self.toggleAnimation.setDirection(direction)
        self.toggleAnimation.start()

