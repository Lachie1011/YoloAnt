"""
    switch.py
"""
from PyQt6.QtCore import QPropertyAnimation, QRectF, QSize, Qt, pyqtProperty, QRect 
from PyQt6.QtGui import QPainter, QImage, QColor
from PyQt6.QtWidgets import (QAbstractButton, QApplication, QHBoxLayout, QSizePolicy, QWidget)


class Switch(QAbstractButton):
    """
        Class that creates a switch button.
    """

    def __init__(self, parent=None, track_radius=8, thumb_radius=7):
        super().__init__(parent=parent)
        self.setCheckable(True)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self._track_radius = track_radius
        self._thumb_radius = thumb_radius

        self._margin = max(0, self._thumb_radius - self._track_radius)
        self._base_offset = max(self._thumb_radius, self._track_radius)
        self._end_offset = {
            True: lambda: self.width() - self._base_offset,
            False: lambda: self._base_offset,
        }
        self._offset = self._base_offset

        palette = self.palette()

        if self._thumb_radius > self._track_radius:
            self._track_color = {
                True: palette.highlight(),
                False: palette.dark(),
            }
            self._thumb_color = {
                True: palette.highlight(),
                False: palette.light(),
            }
            self._text_color = {
                True: palette.highlightedText().color(),
                False: palette.dark().color(),
            }
            self._thumb_text = {
                True: '',
                False: '',
            }
            self._track_opacity = 0.5
        else:
            self._thumb_color = {
                True: palette.highlightedText(),
                False: palette.light(),
            }
            self._track_color = {
                True: QColor('#00a1f0'),
                False: QColor('#BABDB6'),
            }
            self._text_color = {
                True: palette.highlight().color(),
                False: palette.dark().color(),
            }
            self._thumb_text = {
                # True: QImage("icons/icons8-pencil-enabled-18.png"),
                # False: QImage("icons/icons8-pencil-18.png"),
                True: '',
                False: '',
            }
            self._track_opacity = 1

    @pyqtProperty(int)
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        self._offset = value
        self.update()

    def sizeHint(self):  # pylint: disable=invalid-name
        return QSize(
            4 * self._track_radius + 2 * self._margin,
            2 * self._track_radius + 2 * self._margin,
        )

    def setChecked(self, checked):
        super().setChecked(checked)
        self.offset = self._end_offset[checked]()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.offset = self._end_offset[self.isChecked()]()

    def paintEvent(self, event):  # pylint: disable=invalid-name, unused-argument
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        p.setPen(Qt.PenStyle.NoPen)
        track_opacity = self._track_opacity
        thumb_opacity = 1.0
        text_opacity = 1.0
        if self.isEnabled():
            track_brush = self._track_color[self.isChecked()]
            thumb_brush = self._thumb_color[self.isChecked()]
            text_color = self._text_color[self.isChecked()]
        else:
            track_opacity *= 0.8
            track_brush = self.palette().shadow()
            thumb_brush = self.palette().mid()
            text_color = self.palette().shadow().color()

        p.setBrush(track_brush)
        p.setOpacity(track_opacity)
        p.drawRoundedRect(
            self._margin,
            self._margin,
            self.width() - 2 * self._margin,
            self.height() - 2 * self._margin,
            self._track_radius,
            self._track_radius,
        )
        p.setBrush(thumb_brush)
        p.setOpacity(thumb_opacity)
        p.drawEllipse(
            self.offset - self._thumb_radius,
            self._base_offset - self._thumb_radius,
            2 * self._thumb_radius,
            2 * self._thumb_radius,
        )
        # p.setPen(text_color)
        # p.setOpacity(text_opacity)
        # font = p.font()
        # font.setPixelSize(1.5 * self._thumb_radius)
        # p.setFont(font)
        # p.drawImage(
        #     QRectF(
        #         self.offset - self._thumb_radius + 2,
        #         self._base_offset - self._thumb_radius + 2,
        #         self._thumb_radius * 2 - 4,
        #         self._thumb_radius * 2 - 4,
        #     ),
        #     self._thumb_text[self.isChecked()],
        # )

    def mouseReleaseEvent(self, event):  # pylint: disable=invalid-name
        super().mouseReleaseEvent(event)
        if event.button() == Qt.MouseButton.LeftButton:
            anim = QPropertyAnimation(self, b'offset', self)
            anim.setDuration(120)
            anim.setStartValue(self.offset)
            anim.setEndValue(self._end_offset[self.isChecked()]())
            anim.start()

    def enterEvent(self, event):  # pylint: disable=invalid-name
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        super().enterEvent(event)
