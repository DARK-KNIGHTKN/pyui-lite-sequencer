from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, pyqtProperty, QTimer, pyqtSignal, QRect
from PyQt6.QtGui import QPainter, QColor, QPen
from typing import Union

from pyui_lite import logger


class StatusLED(QWidget):
    """
    A customizable LED indicator widget.

    This widget displays a colored circle that can be used to indicate
    status (on/off), different conditions via colors, and can optionally
    blink to draw attention.
    """

    # Define a signal for state changes
    stateChanged = pyqtSignal(bool)

    def __init__(
        self, parent=None, color: Union[QColor, str] = "green", is_on: bool = False
    ):
        """
        Initialize the StatusLED widget.

        Args:
            parent: Optional parent widget
            color: Initial color of the LED (default: green)
            is_on: Initial state of the LED (default: off)
        """
        super().__init__(parent)

        if isinstance(color, str):
            self._color = QColor(color)
        else:
            self._color = color

        self._is_on = is_on
        self._is_blinking = False
        self._blink_rate = 500  # ms
        self._blink_timer = QTimer()
        self._blink_timer.timeout.connect(self._toggle_blink)

        # Set some sensible defaults
        self.setMinimumSize(16, 16)
        self.setFixedSize(24, 24)  # Default size that works well

        logger.debug("StatusLED initialized")

    def paintEvent(self, event) -> None:
        """
        Draw the LED on the widget.

        Args:
            event: The paint event
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Calculate the LED size based on widget size
        size = min(self.width(), self.height())
        rect = QRect(0, 0, size - 1, size - 1)
        rect.moveCenter(self.rect().center())

        # Draw the LED border/background
        painter.setPen(QPen(Qt.GlobalColor.black, 1))
        painter.setBrush(QColor(50, 50, 50))  # Dark gray background
        painter.drawEllipse(rect)

        # Draw the colored LED if it's on
        if self._is_on:
            painter.setPen(QPen(self._color.darker(150), 1))
            painter.setBrush(self._color)
            painter.drawEllipse(rect.adjusted(2, 2, -2, -2))

    def set_on(self, is_on: bool) -> None:
        """
        Set the LED state to on or off.

        Args:
            is_on: True to turn the LED on, False to turn it off
        """
        if self._is_on != is_on:
            self._is_on = is_on
            self.update()  # Trigger a repaint
            self.stateChanged.emit(is_on)
            logger.debug(f"StatusLED set to {'on' if is_on else 'off'}")

    def is_on(self) -> bool:
        """
        Get the current state of the LED.

        Returns:
            bool: True if the LED is on, False otherwise
        """
        return self._is_on

    def set_color(self, color: Union[QColor, str, Qt.GlobalColor]) -> None:
        """
        Set the color of the LED.

        Args:
            color: A QColor, string color name, or Qt.GlobalColor
        """
        if isinstance(color, str):
            self._color = QColor(color)
        else:
            self._color = QColor(color)

        self.update()  # Trigger a repaint
        logger.debug(f"StatusLED color set to {self._color.name()}")

    def get_color(self) -> QColor:
        """
        Get the current color of the LED.

        Returns:
            QColor: The current LED color
        """
        return self._color

    def set_blinking(self, is_blinking: bool) -> None:
        """
        Set whether the LED should blink.

        Args:
            is_blinking: True to make the LED blink, False to stop blinking
        """
        if self._is_blinking == is_blinking:
            return  # No change

        self._is_blinking = is_blinking

        if is_blinking:
            self._blink_timer.start(self._blink_rate)
            logger.debug(f"StatusLED blinking started at {self._blink_rate}ms rate")
        else:
            self._blink_timer.stop()
            logger.debug("StatusLED blinking stopped")

    def is_blinking(self) -> bool:
        """
        Check if the LED is currently in blinking mode.

        Returns:
            bool: True if the LED is blinking, False otherwise
        """
        return self._is_blinking

    def set_blink_rate(self, rate_ms: int) -> None:
        """
        Set the rate at which the LED blinks.

        Args:
            rate_ms: Blink rate in milliseconds
        """
        if rate_ms < 50:
            rate_ms = 50  # Don't allow extremely fast blinking
            logger.warning(f"Blink rate {rate_ms}ms too fast, limited to 50ms")

        self._blink_rate = rate_ms

        # Update the timer if it's running
        if self._is_blinking:
            self._blink_timer.setInterval(rate_ms)
            logger.debug(f"StatusLED blink rate updated to {rate_ms}ms")

    def get_blink_rate(self) -> int:
        """
        Get the current blink rate.

        Returns:
            int: The blink rate in milliseconds
        """
        return self._blink_rate

    def _toggle_blink(self) -> None:
        """
        Internal method to toggle the LED state during blinking.
        """
        self._is_on = not self._is_on
        self.update()  # Trigger a repaint

    # Define properties to make the widget more Qt-like
    color = pyqtProperty(QColor, get_color, set_color)
    on = pyqtProperty(bool, is_on, set_on)
    blinking = pyqtProperty(bool, is_blinking, set_blinking)
    blinkRate = pyqtProperty(int, get_blink_rate, set_blink_rate)
