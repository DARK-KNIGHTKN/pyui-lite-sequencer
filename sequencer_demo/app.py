#!/usr/bin/env python3
import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QSlider,
    QPushButton,
    QTextEdit,
    QTabWidget,
    QComboBox,
    QGroupBox,
    QFormLayout,
    QCheckBox,
)
from PyQt6.QtCore import Qt

# Import custom widgets
from pyui_lite.rotary_knob import RotaryKnob
from pyui_lite.status_led import StatusLED
from pyui_lite import logger
from pyui_lite.progress_ring import ProgressRing


class SequencerDemo(QMainWindow):
    """Demo application for PyUI Lite components."""

    def __init__(self):
        """Initialize the demo application."""
        super().__init__()

        self.setWindowTitle("PyUI Lite - Components Demo")
        self.setGeometry(100, 100, 600, 500)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        # Create the event log FIRST so it can be used by other methods
        # Add a text area to show events at the bottom of the window
        self.event_log = QTextEdit()
        self.event_log.setReadOnly(True)
        self.event_log.setMaximumHeight(100)

        # Create tabs for different widgets
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # Create tab for RotaryKnob
        self.knob_tab = QWidget()
        self.tabs.addTab(self.knob_tab, "Rotary Knob")
        self.setup_knob_tab()

        # Create tab for StatusLED
        self.led_tab = QWidget()
        self.tabs.addTab(self.led_tab, "Status LED")
        self.setup_led_tab()

        # Create tab for ProgressRing
        self.progress_tab = QWidget()
        self.tabs.addTab(self.progress_tab, "Progress Ring")
        self.setup_progress_ring_tab()

        # Now add the event log to the layout
        main_layout.addWidget(self.event_log)

        # Log a message to show we're up and running
        logger.info("Demo application started")
        self.log_event("Application started")

    def setup_knob_tab(self):
        """Set up the RotaryKnob demo tab."""
        layout = QVBoxLayout(self.knob_tab)

        # Add a title
        title = QLabel("RotaryKnob Widget Demo")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)

        # Create our RotaryKnob widget
        self.knob = RotaryKnob()
        self.knob.setFixedSize(150, 150)

        # Create a label to display the current value
        self.value_label = QLabel("Value: 0")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create a label for drag status
        self.drag_status = QLabel("Drag Status: Idle")
        self.drag_status.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create layout for the knob and related info
        knob_layout = QVBoxLayout()
        knob_layout.addWidget(self.knob, alignment=Qt.AlignmentFlag.AlignCenter)
        knob_layout.addWidget(self.value_label)
        knob_layout.addWidget(self.drag_status)

        layout.addLayout(knob_layout)

        # Add a slider to control the knob
        slider_layout = QHBoxLayout()
        slider_label = QLabel("Control via slider:")
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 100)
        slider_layout.addWidget(slider_label)
        slider_layout.addWidget(self.slider)

        layout.addLayout(slider_layout)

        # Add buttons for normalized values
        button_layout = QHBoxLayout()
        zero_btn = QPushButton("Set to 0%")
        half_btn = QPushButton("Set to 50%")
        full_btn = QPushButton("Set to 100%")

        button_layout.addWidget(zero_btn)
        button_layout.addWidget(half_btn)
        button_layout.addWidget(full_btn)

        layout.addLayout(button_layout)

        # Connect signals
        self.knob.valueChanged.connect(self.update_knob_value)
        self.knob.dragStarted.connect(self.on_knob_drag_started)
        self.knob.dragStopped.connect(self.on_knob_drag_stopped)
        self.slider.valueChanged.connect(self.knob.setValue)

        zero_btn.clicked.connect(lambda: self.knob.set_normalized_value(0.0))
        half_btn.clicked.connect(lambda: self.knob.set_normalized_value(0.5))
        full_btn.clicked.connect(lambda: self.knob.set_normalized_value(1.0))

        # Initialize value
        self.update_knob_value(self.knob.value())

    def setup_led_tab(self):
        """Set up the StatusLED demo tab."""
        layout = QVBoxLayout(self.led_tab)

        # Add a title
        title = QLabel("StatusLED Widget Demo")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)

        # Create a row of LEDs with different colors
        led_colors_layout = QHBoxLayout()

        # Create LEDs with different colors
        self.leds = {}
        for color in ["green", "red", "blue", "yellow", "orange", "purple"]:
            led_group = QGroupBox(color.capitalize())
            led_layout = QVBoxLayout(led_group)

            # Create the LED
            led = StatusLED(color=color, is_on=True)
            led.setFixedSize(30, 30)  # Make it slightly larger for the demo
            self.leds[color] = led

            # Add toggle button
            toggle_btn = QPushButton("Toggle")
            toggle_btn.clicked.connect(lambda: self.toggle_led(led))

            # Add to layout
            led_layout.addWidget(led, alignment=Qt.AlignmentFlag.AlignCenter)
            led_layout.addWidget(toggle_btn)

            led_colors_layout.addWidget(led_group)

        layout.addLayout(led_colors_layout)

        # Create controls for a primary LED with more options
        control_group = QGroupBox("LED Controls")
        control_layout = QVBoxLayout(control_group)

        # Main LED with full controls
        self.main_led = StatusLED(color="green", is_on=True)
        self.main_led.setFixedSize(50, 50)  # Make it larger

        # Add controls
        form_layout = QFormLayout()

        # On/Off toggle
        on_off_btn = QPushButton("Toggle On/Off")
        on_off_btn.clicked.connect(lambda: self.toggle_led(self.main_led))
        form_layout.addRow("State:", on_off_btn)

        # Color selector
        color_combo = QComboBox()
        colors = ["green", "red", "blue", "yellow", "orange", "purple", "white"]
        color_combo.addItems(colors)
        color_combo.currentTextChanged.connect(self.set_main_led_color)
        form_layout.addRow("Color:", color_combo)

        # Blinking controls
        blink_btn = QPushButton("Toggle Blinking")
        blink_btn.clicked.connect(self.toggle_main_led_blinking)
        form_layout.addRow("Blinking:", blink_btn)

        # Blink rate slider
        blink_rate_slider = QSlider(Qt.Orientation.Horizontal)
        blink_rate_slider.setRange(50, 1000)  # 50ms to 1000ms
        blink_rate_slider.setValue(500)  # Default 500ms
        blink_rate_slider.valueChanged.connect(self.set_main_led_blink_rate)
        form_layout.addRow("Blink Rate:", blink_rate_slider)

        # Status label
        self.led_status_label = QLabel("LED is ON")
        form_layout.addRow("Status:", self.led_status_label)

        # Main layout for LED section
        main_led_layout = QHBoxLayout()
        main_led_layout.addWidget(self.main_led, alignment=Qt.AlignmentFlag.AlignCenter)
        main_led_layout.addLayout(form_layout)

        control_layout.addLayout(main_led_layout)
        layout.addWidget(control_group)

        # Connect main LED events
        self.main_led.stateChanged.connect(self.update_led_status)

    def toggle_led(self, led):
        """Toggle an LED on/off."""
        led.set_on(not led.is_on())
        self.log_event(f"LED toggled to {'ON' if led.is_on() else 'OFF'}")

    def set_main_led_color(self, color_name):
        """Set the color of the main LED."""
        self.main_led.set_color(color_name)
        self.log_event(f"LED color set to {color_name}")

    def toggle_main_led_blinking(self):
        """Toggle blinking of the main LED."""
        new_state = not self.main_led.is_blinking()
        self.main_led.set_blinking(new_state)
        self.log_event(f"LED blinking {'started' if new_state else 'stopped'}")

    def set_main_led_blink_rate(self, rate_ms):
        """Set the blink rate of the main LED."""
        self.main_led.set_blink_rate(rate_ms)
        self.log_event(f"LED blink rate set to {rate_ms}ms")

    def update_led_status(self, is_on):
        """Update the LED status label."""
        self.led_status_label.setText(f"LED is {'ON' if is_on else 'OFF'}")

    def update_knob_value(self, value):
        """Update the displayed value when the knob changes."""
        self.value_label.setText(f"Value: {value}")
        self.slider.blockSignals(True)
        self.slider.setValue(value)
        self.slider.blockSignals(False)
        self.log_event(f"Knob value changed to {value}")

    def on_knob_drag_started(self):
        """Handle the dragStarted signal."""
        self.drag_status.setText("Drag Status: Dragging")
        self.log_event("Knob drag started")

    def on_knob_drag_stopped(self):
        """Handle the dragStopped signal."""
        self.drag_status.setText("Drag Status: Released")
        self.log_event("Knob drag stopped")

    def log_event(self, message):
        """Add a message to the event log."""
        self.event_log.append(f"> {message}")

    def setup_progress_ring_tab(self):
        """Set up the ProgressRing demo tab."""
        layout = QVBoxLayout(self.progress_tab)

        # Add a title
        title = QLabel("ProgressRing Widget Demo")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)

        # Create a row of progress rings with different styles
        rings_layout = QHBoxLayout()

        # Standard progress ring
        standard_group = QGroupBox("Standard")
        standard_layout = QVBoxLayout(standard_group)
        self.standard_ring = ProgressRing(progress=0.65, show_text=True)
        self.standard_ring.setFixedSize(100, 100)
        standard_layout.addWidget(
            self.standard_ring, alignment=Qt.AlignmentFlag.AlignCenter
        )
        rings_layout.addWidget(standard_group)

        # Thin ring without text
        thin_group = QGroupBox("Thin")
        thin_layout = QVBoxLayout(thin_group)
        self.thin_ring = ProgressRing(
            progress=0.4, thickness=5, show_text=False, progress_color="orange"
        )
        self.thin_ring.setFixedSize(100, 100)
        thin_layout.addWidget(self.thin_ring, alignment=Qt.AlignmentFlag.AlignCenter)
        rings_layout.addWidget(thin_group)

        # Thick ring with custom colors
        thick_group = QGroupBox("Thick")
        thick_layout = QVBoxLayout(thick_group)
        self.thick_ring = ProgressRing(
            progress=0.85, thickness=20, bg_color="#444", progress_color="#2ECC71"
        )
        self.thick_ring.setFixedSize(100, 100)
        thick_layout.addWidget(self.thick_ring, alignment=Qt.AlignmentFlag.AlignCenter)
        rings_layout.addWidget(thick_group)

        layout.addLayout(rings_layout)

        # Create controls for a main progress ring with all options
        control_group = QGroupBox("Progress Ring Controls")
        control_layout = QVBoxLayout(control_group)

        # Main progress ring with full controls
        main_ring_layout = QHBoxLayout()
        self.main_ring = ProgressRing(thickness=15, progress=0.5)
        self.main_ring.setFixedSize(150, 150)
        main_ring_layout.addWidget(
            self.main_ring, alignment=Qt.AlignmentFlag.AlignCenter
        )

        # Controls for the main ring
        form_layout = QFormLayout()

        # Progress slider
        progress_slider = QSlider(Qt.Orientation.Horizontal)
        progress_slider.setRange(0, 100)
        progress_slider.setValue(50)  # Match initial progress (0.5)
        progress_slider.valueChanged.connect(
            lambda value: self.set_main_ring_progress(value / 100.0)
        )
        form_layout.addRow("Progress:", progress_slider)

        # Thickness slider
        thickness_slider = QSlider(Qt.Orientation.Horizontal)
        thickness_slider.setRange(1, 30)
        thickness_slider.setValue(15)  # Match initial thickness
        thickness_slider.valueChanged.connect(self.main_ring.set_thickness)
        form_layout.addRow("Thickness:", thickness_slider)

        # Animation duration slider
        animation_slider = QSlider(Qt.Orientation.Horizontal)
        animation_slider.setRange(50, 1000)
        animation_slider.setValue(250)  # Match initial animation duration
        animation_slider.valueChanged.connect(self.main_ring.set_animation_duration)
        form_layout.addRow("Animation Duration:", animation_slider)

        # Color selectors
        bg_color_combo = QComboBox()
        for color_name, color in [
            ("Dark Gray", "#303030"),
            ("Light Gray", "#808080"),
            ("Blue", "#2C3E50"),
            ("Red", "#7F0000"),
        ]:
            bg_color_combo.addItem(color_name, color)
        bg_color_combo.currentIndexChanged.connect(
            lambda index: self.main_ring.set_bg_color(bg_color_combo.currentData())
        )
        form_layout.addRow("Background Color:", bg_color_combo)

        progress_color_combo = QComboBox()
        for color_name, color in [
            ("Blue", "#4A90E2"),
            ("Green", "#2ECC71"),
            ("Red", "#E74C3C"),
            ("Orange", "#F39C12"),
            ("Purple", "#9B59B6"),
        ]:
            progress_color_combo.addItem(color_name, color)
        progress_color_combo.currentIndexChanged.connect(
            lambda index: self.main_ring.set_progress_color(
                progress_color_combo.currentData()
            )
        )
        form_layout.addRow("Progress Color:", progress_color_combo)

        # Checkbox options
        show_text_check = QCheckBox("Show Percentage")
        show_text_check.setChecked(True)
        show_text_check.toggled.connect(self.main_ring.set_show_text)
        form_layout.addRow("", show_text_check)

        animate_check = QCheckBox("Animate Changes")
        animate_check.setChecked(True)
        animate_check.toggled.connect(self.main_ring.set_animate)
        form_layout.addRow("", animate_check)

        # Add buttons for preset values
        button_layout = QHBoxLayout()
        for value, label in [
            (0.0, "0%"),
            (0.25, "25%"),
            (0.5, "50%"),
            (0.75, "75%"),
            (1.0, "100%"),
        ]:
            btn = QPushButton(label)
            btn.clicked.connect(lambda checked, v=value: self.set_main_ring_progress(v))
            button_layout.addWidget(btn)

        form_layout.addRow("Quick Set:", button_layout)

        # Add the form layout to the main ring layout
        main_ring_layout.addLayout(form_layout)

        control_layout.addLayout(main_ring_layout)
        layout.addWidget(control_group)

        # Connect main ring events
        self.main_ring.progressChanged.connect(
            lambda value: self.log_event(f"Progress changed to {value:.0%}")
        )

    def set_main_ring_progress(self, value):
        """Set the main progress ring value and log it."""
        self.main_ring.set_progress(value)
        self.log_event(f"Set progress to {value:.0%}")


def main():
    """Main function to start the demo app."""
    app = QApplication(sys.argv)
    window = SequencerDemo()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
