"""
    colourSelectorDialog.py
"""

""" Source: https://github.com/nlfmt/pyqt-colorpicker """

import colorsys
from typing import Union

from PyQt6.QtGui import QColor
from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtWidgets import QApplication, QDialog, QGraphicsDropShadowEffect, QHBoxLayout
from customWidgets.customBaseObjects.customUserInputQLineEdit import CustomUserInputQLineEdit
from dialogs.ui.colourSelector_ui import Ui_colourSelector

class ColourSelectorDialog(QDialog):

    def __init__(self, themePaletteColours: dict, fontRegular: str, fontTitle: str):
        """ Class that creates a colour selector dialog instance """

        super(ColourSelectorDialog, self).__init__()
        self.ui = Ui_colourSelector()
        self.ui.setupUi(self)
        self.themePaletteColours = themePaletteColours
        self.fontRegular = fontRegular
        self.fontTitle = fontTitle

        # Remove frame from dialog
        self.setWindowTitle("Colour Selector")
        self.setWindowFlags(Qt.WindowType.Tool | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Setup style sheet
        self.__setupStyleSheet()

        # Add DropShadow
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(17)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 150))
        self.ui.colourSelectorFrame.setGraphicsEffect(self.shadow)

        # Connect update functions
        self.ui.hue.mousePressEvent = self.moveHueSelector
        self.ui.hue.mouseMoveEvent = self.moveHueSelector
        self.redLineEdit.textEdited.connect(self.rgbChanged)
        self.greenLineEdit.textEdited.connect(self.rgbChanged)
        self.blueLineEdit.textEdited.connect(self.rgbChanged)
        self.hexLineEdit.textEdited.connect(self.hexChanged)

        # # Connect window dragging functions
        self.ui.colourSelectorFrame.mouseMoveEvent = self.moveWindow
        self.ui.colourSelectorFrame.mousePressEvent = self.setDragPos

        # Connect selector moving function
        self.ui.black_overlay.mouseMoveEvent = self.moveSVSelector
        self.ui.black_overlay.mousePressEvent = self.moveSVSelector

        # Connect Ok|Cancel Button Box and X Button
        self.ui.acceptButton.clicked.connect(self.accept)
        self.ui.cancelButton.clicked.connect(self.reject)

        self.lastColour = (0, 0, 0)
        self.color = (0, 0, 0)
        self.alpha = 100

    def __setupStyleSheet(self) -> None:
        """ Sets the style sheet for the page """
        self.ui.colourSelectorFrame.setStyleSheet("QFrame{"
                                                  f"background-color: {self.themePaletteColours['panel.background']};"
                                                  "border-radius: 10px;}")

        self.redLineEdit = CustomUserInputQLineEdit(self.themePaletteColours, self.fontRegular)
        self.redLineEdit.setCursorPosition(0)
        self.redLineEdit.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.redLineEditFrameLayout = QHBoxLayout()
        self.redLineEditFrameLayout.addWidget(self.redLineEdit)
        self.redLineEditFrameLayout.setContentsMargins(0,0,0,0)
        self.ui.redLineEditFrame.setLayout(self.redLineEditFrameLayout)

        self.greenLineEdit = CustomUserInputQLineEdit(self.themePaletteColours, self.fontRegular)
        self.greenLineEdit.setCursorPosition(0)
        self.greenLineEdit.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.greenLineEditFrameLayout = QHBoxLayout()
        self.greenLineEditFrameLayout.addWidget(self.greenLineEdit)
        self.greenLineEditFrameLayout.setContentsMargins(0,0,0,0)
        self.ui.greenLineEditFrame.setLayout(self.greenLineEditFrameLayout)

        self.blueLineEdit = CustomUserInputQLineEdit(self.themePaletteColours, self.fontRegular)
        self.blueLineEdit.setCursorPosition(0)
        self.blueLineEdit.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.blueLineEditFrameLayout = QHBoxLayout()
        self.blueLineEditFrameLayout.addWidget(self.blueLineEdit)
        self.blueLineEditFrameLayout.setContentsMargins(0,0,0,0)
        self.ui.blueLineEditFrame.setLayout(self.blueLineEditFrameLayout)

        self.hexLineEdit = CustomUserInputQLineEdit(self.themePaletteColours, self.fontRegular)
        self.hexLineEdit.setCursorPosition(0)
        self.hexLineEdit.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.hexLineEditFrameLayout = QHBoxLayout()
        self.hexLineEditFrameLayout.addWidget(self.hexLineEdit)
        self.hexLineEditFrameLayout.setContentsMargins(0,0,0,0)
        self.ui.hexLineEditFrame.setLayout(self.hexLineEditFrameLayout)

        self.ui.redLbl.setStyleSheet("QLabel{"
                                     f"color: {self.themePaletteColours['font.header']};"
                                     f"font: 75 bold 12pt {self.fontTitle};}}")
        
        self.ui.greenLbl.setStyleSheet("QLabel{"
                                     f"color: {self.themePaletteColours['font.header']};"
                                     f"font: 75 bold 12pt {self.fontTitle};}}")
        
        self.ui.blueLbl.setStyleSheet("QLabel{"
                                     f"color: {self.themePaletteColours['font.header']};"
                                     f"font: 75 bold 12pt {self.fontTitle};}}")
        
        self.ui.hexLbl.setStyleSheet("QLabel{"
                                     f"color: {self.themePaletteColours['font.header']};"
                                     f"font: 75 bold 12pt {self.fontTitle};}}")

        self.ui.cancelButton.setStyleSheet("QPushButton{"
                                           f"background-color: {self.themePaletteColours['cancelButton.background']};"
                                           f"border : 1px solid {self.themePaletteColours['cancelButton.background']};"
                                           "border-radius: 10px;"
                                           f"font: 75 bold 12pt {self.fontTitle};"
                                           f"color: {self.themePaletteColours['font.header']};}}"
                                           "QPushButton::hover{"
                                           f"background-color : {self.themePaletteColours['cancelButton.hover']};"
                                           f"border : 1px solid {self.themePaletteColours['cancelButton.hover']};}}")

        self.ui.acceptButton.setStyleSheet("QPushButton{"
                                           f"background-color: {self.themePaletteColours['buttonFilled.background']};"
                                           f"border : 1px solid {self.themePaletteColours['buttonFilled.background']};"
                                           "border-radius: 10px;"
                                           f"font: 75 bold 12pt {self.fontTitle};"
                                           f"color: {self.themePaletteColours['font.header']};}}"
                                           "QPushButton::hover{"
                                           f"background-color : {self.themePaletteColours['buttonFilled.hover']};"
                                           f"border : 1px solid {self.themePaletteColours['buttonFilled.hover']};}}")



    def getColour(self, themePaletteColours: dict, fontRegular: str, fontTitle: str, lastColour: tuple = None):
        """Open the UI and get a color from the user.

        :param lastColour: The color to show as previous color.
        :return: The selected color.
        """
        
        if lastColour != None:
         lastColour = lastColour
        if lastColour == None: lastColour = self.lastColour
        else: self.lastColour = lastColour

        self.setHSV(self.lastColour)
        self.setRGB(lastColour)
        self.rgbChanged()
        r,g,b = lastColour

        if self.exec():
            r, g, b = hsv2rgb(self.color)
            self.lastColour = (r,g,b)
            return (r,g,b)

        else:
            return self.lastColour

    # Update Functions
    def hsvChanged(self):
        h,s,v = (100 - self.ui.hue_selector.y() / 1.85, (self.ui.selector.x() + 6) / 2.0, (194 - self.ui.selector.y()) / 2.0)
        r,g,b = hsv2rgb(h,s,v)
        self.color = (h,s,v)
        self.setRGB((r,g,b))
        self.setHex(hsv2hex(self.color))
        self.ui.color_vis.setStyleSheet(f"background-color: rgb({r},{g},{b})")
        self.ui.color_view.setStyleSheet(f"border-radius: 5px;background-color: qlineargradient(x1:1, x2:0, stop:0 hsl({h}%,100%,50%), stop:1 #fff);")

    def rgbChanged(self):
        r,g,b = self.i(self.redLineEdit.text()), self.i(self.greenLineEdit.text()), self.i(self.blueLineEdit.text())
        cr,cg,cb = self.clampRGB((r,g,b))

        if r!=cr or (r==0 and self.redLineEdit.hasFocus()):
            self.setRGB((cr,cg,cb))
            self.redLineEdit.selectAll()
        if g!=cg or (g==0 and self.greenLineEdit.hasFocus()):
            self.setRGB((cr,cg,cb))
            self.greenLineEdit.selectAll()
        if b!=cb or (b==0 and self.blueLineEdit.hasFocus()):
            self.setRGB((cr,cg,cb))
            self.blueLineEdit.selectAll()

        self.color = rgb2hsv(r,g,b)
        self.setHSV(self.color)
        self.setHex(rgb2hex((r,g,b)))
        self.ui.color_vis.setStyleSheet(f"background-color: rgb({r},{g},{b})")

    def hexChanged(self):
        hex = self.hexLineEdit.text()
        try:
            int(hex, 16)
        except ValueError:
            hex = "000000"
            self.hexLineEdit.setText("")
        r, g, b = hex2rgb(hex)
        self.color = hex2hsv(hex)
        self.setHSV(self.color)
        self.setRGB((r, g, b))
        self.ui.color_vis.setStyleSheet(f"background-color: rgb({r},{g},{b})")

    def alphaChanged(self):
        alpha = self.i(self.ui.alpha.text())
        oldalpha = alpha
        if alpha < 0: alpha = 0
        if alpha > 100: alpha = 100
        if alpha != oldalpha or alpha == 0:
            self.ui.alpha.setText(str(alpha))
            self.ui.alpha.selectAll()
        self.alpha = alpha

    # Internal setting functions
    def setRGB(self, c):
        r,g,b = c
        self.redLineEdit.setText(str(self.i(r)))
        self.greenLineEdit.setText(str(self.i(g)))
        self.blueLineEdit.setText(str(self.i(b)))

    def setHSV(self, c):
        self.ui.hue_selector.move(7, int((100 - c[0]) * 1.85))
        self.ui.color_view.setStyleSheet(f"border-radius: 5px;background-color: qlineargradient(x1:1, x2:0, stop:0 hsl({c[0]}%,100%,50%), stop:1 #fff);")
        self.ui.selector.move(int(c[1] * 2 - 6), int((200 - c[2] * 2) - 6))

    def setHex(self, c):
        self.hexLineEdit.setText(c)

    def setAlpha(self, a):
        self.ui.alpha.setText(str(a))

    # Dragging Functions
    def setDragPos(self, event):
        self.dragPos = event.globalPosition().toPoint()

    def moveWindow(self, event):
        # MOVE WINDOW
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
            self.dragPos = event.globalPosition().toPoint()
            event.accept()

    def moveSVSelector(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            pos = event.pos()
            if pos.x() < 0: pos.setX(0)
            if pos.y() < 0: pos.setY(0)
            if pos.x() > 200: pos.setX(200)
            if pos.y() > 200: pos.setY(200)
            self.ui.selector.move(pos - QPoint(6,6))
            self.hsvChanged()

    def moveHueSelector(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            pos = event.pos().y() - 7
            if pos < 0: pos = 0
            if pos > 185: pos = 185
            self.ui.hue_selector.move(QPoint(7, pos))
            self.hsvChanged()

    # Utility

    # Custom int() function, that converts invalid strings to 0
    def i(self, text):
        try: return int(text)
        except ValueError: return 0

    # clamp function to remove near-zero values
    def clampRGB(self, rgb):
        r, g, b = rgb
        if r<0.0001: r=0
        if g<0.0001: g=0
        if b<0.0001: b=0
        if r>255: r=255
        if g>255: g=255
        if b>255: b=255
        return r, g, b


# Color Utility
def hsv2rgb(h_or_color: Union[tuple, int], s: int = 0, v: int = 0, a: int = None) -> tuple:
    """Convert hsv color to rgb color.

    :param h_or_color: The 'hue' value or a color tuple.
    :param s: The 'saturation' value.
    :param v: The 'value' value.
    :param a: The 'alpha' value.
    :return: The converted rgb tuple color.
    """

    if type(h_or_color).__name__ == "tuple":
        if len(h_or_color) == 4:
            h, s, v, a = h_or_color
        else:
            h, s, v = h_or_color
    else: h = h_or_color
    r, g, b = colorsys.hsv_to_rgb(h / 100.0, s / 100.0, v / 100.0)
    if a is not None: return r * 255, g * 255, b * 255, a
    return r * 255, g * 255, b * 255


def rgb2hsv(r_or_color: Union[tuple, int], g: int = 0, b: int = 0, a: int = None) -> tuple:
    """Convert rgb color to hsv color.

    :param r_or_color: The 'red' value or a color tuple.
    :param g: The 'green' value.
    :param b: The 'blue' value.
    :param a: The 'alpha' value.
    :return: The converted hsv tuple color.
    """

    if type(r_or_color).__name__ == "tuple":
        if len(r_or_color) == 4:
            r, g, b, a = r_or_color
        else:
            r, g, b = r_or_color
    else: r = r_or_color
    h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
    if a is not None: return h * 100, s * 100, v * 100, a
    return h * 100, s * 100, v * 100


def hex2rgb(hex: str) -> tuple:
    """Convert hex color to rgb color.

    :param hex: The hexadecimal string ("xxxxxx").
    :return: The converted rgb tuple color.
    """

    if len(hex) < 6: hex += "0"*(6-len(hex))
    elif len(hex) > 6: hex = hex[0:6]
    rgb = tuple(int(hex[i:i+2], 16) for i in (0,2,4))
    return rgb


def rgb2hex(r_or_color: Union[tuple, int], g: int = 0, b: int = 0, a: int = 0) -> str:
    """Convert rgb color to hex color.

    :param r_or_color: The 'red' value or a color tuple.
    :param g: The 'green' value.
    :param b: The 'blue' value.
    :param a: The 'alpha' value.
    :return: The converted hexadecimal color.
    """

    if type(r_or_color).__name__ == "tuple": r, g, b = r_or_color[:3]
    else: r = r_or_color
    hex = '%02x%02x%02x' % (int(r), int(g), int(b))
    return hex


def hex2hsv(hex: str) -> tuple:
    """Convert hex color to hsv color.

    :param hex: The hexadecimal string ("xxxxxx").
    :return: The converted hsv tuple color.
    """

    return rgb2hsv(hex2rgb(hex))


def hsv2hex(h_or_color: Union[tuple, int], s: int = 0, v: int = 0, a: int = 0) -> str:
    """Convert hsv color to hex color.

    :param h_or_color: The 'hue' value or a color tuple.
    :param s: The 'saturation' value.
    :param v: The 'value' value.
    :param a: The 'alpha' value.
    :return: The converted hexadecimal color.
    """

    if type(h_or_color).__name__ == "tuple": h, s, v = h_or_color[:3]
    else: h = h_or_color
    return rgb2hex(hsv2rgb(h, s, v))


# toplevel functions

__instance = None
__lightTheme = False
__useAlpha = False


def useAlpha(value=True) -> None:
    """Set if the ColourSelectorDialog should display an alpha field.

    :param value: True for alpha field, False for no alpha field. Defaults to True
    :return:
    """
    global __useAlpha
    __useAlpha = value


def useLightTheme(value=True) -> None:
    """Set if the ColourSelectorDialog should use the light theme.

    :param value: True for light theme, False for dark theme. Defaults to True
    :return: None
    """

    global __lightTheme
    __lightTheme = value


def getColour (themePaletteColours: dict, fontRegular: str, fontTitle: str, lastColour: tuple = None) -> tuple:
    """Shows the ColourSelectorDialog and returns the picked color.

    :param lastColour: The color to display as previous color.
    :return: The picked color.
    """

    global __instance

    if __instance is None:
        __instance = ColourSelectorDialog(themePaletteColours, fontRegular, fontTitle)

    return __instance.getColour(fontRegular, fontTitle, lastColour)