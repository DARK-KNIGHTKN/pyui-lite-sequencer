from PyQt6.QtWidgets import QDial
from PyQt6.QtCore import pyqtSignal

# Import the logger from the package
from pyui_lite import logger


class RotaryKnob(QDial):
    """
    A customizable rotary knob widget that extends QDial functionality.

    This widget provides a circular control similar to physical knobs on audio
    equipment, with additional features like drag detection and enhanced logging.
    """

    # Define our custom signals
    dragStarted = pyqtSignal()  # Emitted when user starts dragging the knob
    dragStopped = pyqtSignal()  # Emitted when user releases the knob

    def __init__(self, parent=None):
        """
        Initialize the RotaryKnob widget.

        Args:
            parent: Optional parent widget
        """
        super().__init__(parent)

        # Set default range to 0-100
        self.setRange(0, 100)

        # Connect the built-in valueChanged signal to our logging method
        self.valueChanged.connect(self._on_value_changed)

        logger.debug("RotaryKnob initialized")

    def mousePressEvent(self, event) -> None:
        """
        Handle mouse press events and emit dragStarted signal.

        Args:
            event: The mouse event
        """
        # Call the parent implementation first
        super().mousePressEvent(event)
        logger.debug("RotaryKnob drag started")
        self.dragStarted.emit()

    def mouseReleaseEvent(self, event) -> None:
        """
        Handle mouse release events and emit dragStopped signal.

        Args:
            event: The mouse event
        """
        # Call the parent implementation first
        super().mouseReleaseEvent(event)
        logger.debug("RotaryKnob drag stopped")
        self.dragStopped.emit()

    def _on_value_changed(self, value: int) -> None:
        """
        Internal slot that logs when the value changes.

        Args:
            value: The new value of the knob
        """
        logger.debug(f"RotaryKnob value changed to {value}")

    def set_normalized_value(self, normalized_value: float) -> None:
        """
        Set the knob's value using a normalized value between 0.0 and 1.0.

        This is convenient for setting the knob as a percentage of its range.

        Args:
            normalized_value: A value between 0.0 and 1.0
        """
        if not 0.0 <= normalized_value <= 1.0:
            logger.warning(
                f"Normalized value {normalized_value} out of range [0.0, 1.0], clamping"
            )
            normalized_value = max(0.0, min(normalized_value, 1.0))

        min_val = self.minimum()
        max_val = self.maximum()
        range_val = max_val - min_val

        value = int(min_val + (range_val * normalized_value))
        self.setValue(value)

    def get_normalized_value(self) -> float:
        """
        Get the current value of the knob as a normalized value (0.0 to 1.0).

        Returns:
            float: Normalized value between 0.0 and 1.0
        """
        min_val = self.minimum()
        max_val = self.maximum()
        range_val = max_val - min_val

        if range_val == 0:
            return 0.0

        return (self.value() - min_val) / range_val
