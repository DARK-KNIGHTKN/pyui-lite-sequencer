from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import (
    Qt,
    QRectF,
    QPropertyAnimation,
    pyqtProperty,
    QEasingCurve,
    pyqtSignal,
    QPointF,
)
from PyQt6.QtGui import QPainter, QColor, QPen, QFont
from typing import Union

from pyui_lite import logger


class ProgressRing(QWidget):
    """
    A customizable circular progress indicator.

    This widget displays progress as a circular ring, with options for
    colors, thickness, text display, and smooth animations.
    """

    progressChanged = pyqtSignal(float)

    def __init__(
        self,
        parent=None,
        progress: float = 0.0,
        bg_color: Union[QColor, str] = "#303030",
        progress_color: Union[QColor, str] = "#4A90E2",
        thickness: int = 10,
        show_text: bool = True,
        animate: bool = True,
        animation_duration: int = 250,
    ):
        """
        Initialize the ProgressRing widget.

        Args:
            parent: Optional parent widget
            progress: Initial progress value (0.0 to 1.0)
            bg_color: Background ring color
            progress_color: Progress ring color
            thickness: Thickness of the ring in pixels
            show_text: Whether to show percentage text in the center
            animate: Whether to animate progress changes
            animation_duration: Duration of animations in milliseconds
        """
        super().__init__(parent)

        # Convert string colors to QColor if needed
        if isinstance(bg_color, str):
            self._bg_color = QColor(bg_color)
        else:
            self._bg_color = bg_color

        if isinstance(progress_color, str):
            self._progress_color = QColor(progress_color)
        else:
            self._progress_color = progress_color

        self._thickness = thickness
        self._show_text = show_text
        self._animate = animate
        self._animation_duration = animation_duration

        # Internal progress value (0.0 to 1.0)
        self._progress = max(0.0, min(1.0, progress))

        # Initialize animated progress before creating the animation
        self._animated_progress = self._progress

        # Animation for smooth progress changes
        self._animation = QPropertyAnimation(self, b"animatedProgress")
        self._animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._animation.setDuration(animation_duration)

        # Set minimum size for good visibility
        self.setMinimumSize(40, 40)

        logger.debug(f"ProgressRing initialized with progress={progress}")

    def paintEvent(self, event) -> None:
        """
        Draw the progress ring on the widget.

        Args:
            event: The paint event
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Calculate the ring size, centered in widget
        size = min(self.width(), self.height()) - self._thickness
        rect = QRectF(0, 0, size, size)

        # Convert QPoint to QPointF for moveCenter
        center_point = self.rect().center()
        center_point_f = QPointF(center_point)

        rect.moveCenter(center_point_f)

        # Draw parameters
        start_angle = 90 * 16  # Start from the top (0 is at 3 o'clock position)
        # Convert to integer for drawArc
        span_angle = int(
            -self._animated_progress * 360 * 16
        )  # Negative for clockwise, in 1/16 degrees

        # Draw background circle (gray ring)
        painter.setPen(QPen(self._bg_color, self._thickness, Qt.PenStyle.SolidLine))
        painter.drawEllipse(rect)

        # Draw progress arc
        if self._animated_progress > 0:
            painter.setPen(
                QPen(self._progress_color, self._thickness, Qt.PenStyle.SolidLine)
            )
            painter.drawArc(rect, start_angle, span_angle)

        # Draw text if enabled
        if self._show_text:
            percent = int(self._animated_progress * 100)
            text = f"{percent}%"

            font = QFont()
            # Convert to integer for setPixelSize
            font.setPixelSize(int(size / 5))
            painter.setFont(font)

            painter.setPen(Qt.GlobalColor.white)
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, text)

    def set_progress(self, progress: float) -> None:
        """
        Set the current progress value.

        Args:
            progress: Progress value between 0.0 and 1.0
        """
        # Clamp to valid range
        progress = max(0.0, min(1.0, progress))

        if self._progress != progress:
            old_progress = self._progress
            self._progress = progress

            # Log the change
            logger.debug(
                f"ProgressRing progress changed from {old_progress:.2f} "
                f"to {progress:.2f}"
            )

            if self._animate:
                # Stop any running animation
                self._animation.stop()

                # Set up the new animation
                self._animation.setStartValue(self._animated_progress)
                self._animation.setEndValue(progress)
                self._animation.start()
            else:
                # Update immediately without animation
                self._animated_progress = progress
                self.update()

            # Emit the signal
            self.progressChanged.emit(progress)

    def get_progress(self) -> float:
        """
        Get the current progress value.

        Returns:
            float: Current progress (0.0 to 1.0)
        """
        return self._progress

    def set_bg_color(self, color: Union[QColor, str]) -> None:
        """
        Set the background ring color.

        Args:
            color: A QColor or string color name
        """
        if isinstance(color, str):
            self._bg_color = QColor(color)
        else:
            self._bg_color = color

        self.update()
        logger.debug(f"ProgressRing background color set to {self._bg_color.name()}")

    def get_bg_color(self) -> QColor:
        """
        Get the current background ring color.

        Returns:
            QColor: Current background color
        """
        return self._bg_color

    def set_progress_color(self, color: Union[QColor, str]) -> None:
        """
        Set the progress ring color.

        Args:
            color: A QColor or string color name
        """
        if isinstance(color, str):
            self._progress_color = QColor(color)
        else:
            self._progress_color = color

        self.update()
        logger.debug(
            f"ProgressRing progress color set to {self._progress_color.name()}"
        )

    def get_progress_color(self) -> QColor:
        """
        Get the current progress ring color.

        Returns:
            QColor: Current progress color
        """
        return self._progress_color

    def set_thickness(self, thickness: int) -> None:
        """
        Set the thickness of the progress ring.

        Args:
            thickness: Ring thickness in pixels
        """
        if thickness < 1:
            thickness = 1

        self._thickness = thickness
        self.update()
        logger.debug(f"ProgressRing thickness set to {thickness}")

    def get_thickness(self) -> int:
        """
        Get the current ring thickness.

        Returns:
            int: Current thickness in pixels
        """
        return self._thickness

    def set_show_text(self, show: bool) -> None:
        """
        Set whether to show percentage text in the center.

        Args:
            show: True to show text, False to hide
        """
        self._show_text = show
        self.update()
        logger.debug(f"ProgressRing text display set to {show}")

    def get_show_text(self) -> bool:
        """
        Check if percentage text is being shown.

        Returns:
            bool: True if showing text, False otherwise
        """
        return self._show_text

    def set_animate(self, animate: bool) -> None:
        """
        Set whether progress changes should be animated.

        Args:
            animate: True to animate changes, False for immediate updates
        """
        self._animate = animate
        logger.debug(f"ProgressRing animation set to {animate}")

    def get_animate(self) -> bool:
        """
        Check if progress changes are animated.

        Returns:
            bool: True if animating, False otherwise
        """
        return self._animate

    def set_animation_duration(self, duration: int) -> None:
        """
        Set the duration of progress change animations.

        Args:
            duration: Animation duration in milliseconds
        """
        if duration < 50:
            duration = 50  # Don't allow extremely short durations

        self._animation_duration = duration
        self._animation.setDuration(duration)
        logger.debug(f"ProgressRing animation duration set to {duration}ms")

    def get_animation_duration(self) -> int:
        """
        Get the current animation duration.

        Returns:
            int: Animation duration in milliseconds
        """
        return self._animation_duration

    # These methods are used for the animatedProgress property
    def get_animated_progress(self) -> float:
        """
        Get the current animated progress value (for internal animation use).

        Returns:
            float: Current animated progress (0.0 to 1.0)
        """
        return self._animated_progress

    def set_animated_progress(self, progress: float) -> None:
        """
        Set the current animated progress value (for internal animation use).

        Args:
            progress: Animated progress value between 0.0 and 1.0
        """
        self._animated_progress = progress
        self.update()  # Trigger a repaint

    # Define properties to make the widget more Qt-like
    progress = pyqtProperty(float, get_progress, set_progress)
    bgColor = pyqtProperty(QColor, get_bg_color, set_bg_color)
    progressColor = pyqtProperty(QColor, get_progress_color, set_progress_color)
    thickness = pyqtProperty(int, get_thickness, set_thickness)
    showText = pyqtProperty(bool, get_show_text, set_show_text)
    animate = pyqtProperty(bool, get_animate, set_animate)
    animationDuration = pyqtProperty(
        int, get_animation_duration, set_animation_duration
    )
    animatedProgress = pyqtProperty(float, get_animated_progress, set_animated_progress)
