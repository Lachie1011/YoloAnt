from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import (
    QFrame, QLabel, QPushButton, QHBoxLayout, QSizePolicy
)

from custom_widgets.customBaseObjects.customListItemQLineEdit import CustomListItemQLineEdit


class ClassAttributesFrame(QFrame):
    """
    Frame that contains widgets for class attributes in view/edit mode.
    """

    def __init__(self, themePaletteColours, fontRegular):
        super().__init__()
        self.themePaletteColours = themePaletteColours
        self.fontRegular = fontRegular

        self.__initWidgets()
        self.__buildLayouts()
        self.setEditMode(False)

    def __initWidgets(self):
        """Initialize all widget components."""

        # --- View Mode Widgets ---
        self.classColourLbl = QLabel()
        self.classColourLbl.setFixedWidth(20)
        self.classColourLbl.setStyleSheet("""
            QLabel {
                background-color: transparent;
                border-radius: 4px;
                border-top-right-radius: 0px;
                border-bottom-right-radius: 0px;
            }
        """)

        self.classNameLbl = QLabel()
        self.classNameLbl.setStyleSheet(f"font: 12pt {self.fontRegular};")
        self.classNameLbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.classHotKeyLbl = QLabel()
        self.classHotKeyLbl.setFixedSize(25, 25)
        self.classHotKeyLbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.classHotKeyLbl.setStyleSheet(f"""
            QLabel {{
                background-color: transparent;
                border: 2px solid {self.themePaletteColours['buttonFilled.background']};
                border-radius: 5px;
            }}
        """)

        self.classAnnotationsCountLbl = QLabel()
        self.classAnnotationsCountLbl.setFixedSize(25, 20)
        self.classAnnotationsCountLbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.classAnnotationsCountLbl.setStyleSheet(f"""
            QLabel {{
                background-color: {self.themePaletteColours['panel.sunken']};
                border: 2px solid {self.themePaletteColours['panel.sunken']};
                border-radius: 5px;
            }}
        """)

        # --- Edit Mode Widgets ---
        self.classColourBtn = QPushButton()
        self.classColourBtn.setFixedSize(20, 20)
        self.classColourBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.classNameLineEdit = CustomListItemQLineEdit(
            self.themePaletteColours, f"font: 75 12pt {self.fontRegular};"
        )
        self.classNameLineEdit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.classNameLineEdit.setTextMargins(2, 0, 2, 0)
        self.classNameLineEdit.setCursorPosition(0)
        self.classNameLineEdit.setEditMode(True)

        self.classHotKeyBtn = QPushButton()
        self.classHotKeyBtn.setFixedSize(25, 25)
        self.classHotKeyBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.classDeleteBtn = QPushButton()
        self.classDeleteBtn.setFixedSize(20, 20)
        self.classDeleteBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    def __buildLayouts(self):
        """Builds and attaches layouts for view and edit modes."""

        # View mode layout
        self.viewLayout = QHBoxLayout()
        self.viewLayout.setContentsMargins(0, 0, 0, 0)
        self.viewLayout.setSpacing(6)
        self.viewLayout.addWidget(self.classColourLbl)
        self.viewLayout.addWidget(self.classNameLbl, stretch=1)
        self.viewLayout.addWidget(self.classHotKeyLbl)
        self.viewLayout.addWidget(self.classAnnotationsCountLbl)

        self.viewFrame = QFrame()
        self.viewFrame.setLayout(self.viewLayout)

        # Edit mode layout
        self.editLayout = QHBoxLayout()
        self.editLayout.setContentsMargins(0, 0, 0, 0)
        self.editLayout.setSpacing(6)
        self.editLayout.addWidget(self.classColourBtn)
        self.editLayout.addWidget(self.classNameLineEdit, stretch=1)
        self.editLayout.addWidget(self.classHotKeyBtn)
        self.editLayout.addWidget(self.classDeleteBtn)

        self.editFrame = QFrame()
        self.editFrame.setLayout(self.editLayout)

        # Combine both into main layout
        self.mainLayout = QHBoxLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.addWidget(self.viewFrame)
        self.mainLayout.addWidget(self.editFrame)
        self.setLayout(self.mainLayout)

    # --- Public Setters ---
    def setClassNameText(self, className: str):
        self.classNameLbl.setText(className)
        self.classNameLineEdit.setText(className)

    def setHotKeyText(self, hotKeyChar: str):
        self.classHotKeyLbl.setText(hotKeyChar)
        self.classHotKeyBtn.setText(hotKeyChar)

    def setClassColour(self, colour: tuple):
        rgb = f"rgb{colour}"

        self.classColourLbl.setStyleSheet(f"""
            QLabel {{
                background-color: {rgb};
                border-radius: 4px;
                border-top-right-radius: 0px;
                border-bottom-right-radius: 0px;
            }}
        """)

        self.classColourBtn.setStyleSheet(f"""
            QPushButton {{
                background-color: {rgb};
                border-radius: 4px;
                border: 3px solid {self.themePaletteColours['buttonFilled.background']};
            }}
            QPushButton:hover {{
                border: 3px solid {self.themePaletteColours['buttonFilled.hover']};
            }}
        """)

    def setClassAnnotationsCount(self, numberOfAnnotations: int):
        self.classAnnotationsCountLbl.setText(str(numberOfAnnotations))

    def setEditMode(self, toggled: bool):
        self.viewFrame.setVisible(not toggled)
        self.editFrame.setVisible(toggled)
