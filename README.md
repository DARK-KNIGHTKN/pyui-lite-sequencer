# PyUI-Lite + Sequencer Demo

A lightweight PyQt6 widget library with custom UI components and a comprehensive demo application showcasing professional desktop widget development.

## Features

### Custom Widgets
- **RotaryKnob** - Interactive circular control with drag functionality (0–100 range)
- **StatusLED** - Customizable on/off indicator with color themes and blinking support  
- **ProgressRing** - Animated circular progress bar with percentage display and smooth transitions

### Demo Application
- Tabbed interface showcasing all custom widgets
- Interactive property controls for each widget
- Real-time event logging panel
- Professional UI design patterns and best practices

## Installation

### Quick Start
```bash
# Clone and install
git clone https://github.com/DARK-KNIGHTKN/pyui-lite-sequencer.git
cd pyui-lite-sequencer
pip install -e .

# Launch demo
pyui-demo
Requirements
Python 3.8+
PyQt6 6.0.0+
Usage
Running the Demo
# Method 1: CLI command (recommended)
pyui-demo

# Method 2: Python module
python -m sequencer_demo.app

# Method 3: Direct execution  
python sequencer_demo/app.py
Using Widgets in Your Code
RotaryKnob - Audio-style Circular Control
from pyui_lite.rotary_knob import RotaryKnob

knob = RotaryKnob()
knob.setRange(0, 100)
knob.setValue(75)

# Normalized values (0.0-1.0)
knob.set_normalized_value(0.5)  # 50%
percent = knob.get_normalized_value()

# Drag events
knob.dragStarted.connect(lambda: print("Drag started"))
knob.valueChanged.connect(lambda v: print(f"Value: {v}"))
StatusLED - Visual State Indicator
from pyui_lite.status_led import StatusLED

# Create colored LED
led = StatusLED(color="green", is_on=True)

# Control state
led.set_on(False)
led.toggle()

# Blinking mode
led.set_blinking(True)
led.set_blink_rate(300)  # 300ms intervals

# Available colors: green, red, blue, yellow, orange, purple, white
ProgressRing - Circular Progress Display
from pyui_lite.progress_ring import ProgressRing

# Create animated progress ring
ring = ProgressRing(
    progress=0.0,
    thickness=12,
    show_text=True,
    progress_color="#4A90E2"
)

# Update with smooth animation
ring.set_progress(0.85)  # 85%

# Customization
ring.set_bg_color("#303030")
ring.set_animation_duration(500)
Development
Code Quality Standards
Type hints on all functions and methods
Sphinx-style docstrings for documentation
Pre-commit hooks with Black, Flake8, and MyPy
Professional logging throughout
Development Setup
# Install with dev dependencies
pip install -e ".[dev]"

# Setup pre-commit hooks
pre-commit install

# Run quality checks
pre-commit run --all-files
Project Structure
pyui-lite-sequencer/
├── pyui_lite/                 # Core widget library
│   ├── __init__.py           # Package initialization + logging
│   ├── rotary_knob.py        # RotaryKnob widget
│   ├── status_led.py         # StatusLED widget  
│   └── progress_ring.py      # ProgressRing widget
├── sequencer_demo/           # Demo application
│   ├── __init__.py
│   └── app.py                # Tabbed widget showcase
├── tests/                    # Test suite
├── .pre-commit-config.yaml   # Code quality automation
├── pyproject.toml            # Project configuration
├── requirements.txt          # Dependencies
└── README.md                 # This file
Widget Features
Feature	RotaryKnob	StatusLED	ProgressRing
Customizable Colors	❌	✅	✅
Animations	❌	✅ (Blinking)	✅ (Smooth)
Event Signals	✅	✅	✅
Range Control	✅	❌	✅
Text Display	❌	❌	✅
Drag Interaction	✅	❌	❌
Contributing
Fork the repository
Create feature branch: git checkout -b feature/new-widget
Follow existing code patterns (type hints, docstrings, logging)
Ensure pre-commit hooks pass
Submit pull request with clear description
License
MIT License - Open source and free to use in personal and commercial projects.

Author
Karthik Naren - GitHub  | karthik27naren@gmail.com 

Professional PyQt6 widget development showcasing modern desktop application patterns.