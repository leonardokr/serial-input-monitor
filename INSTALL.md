# Installation Guide

## Quick Start

### Option 1: Basic Installation (Core features only)
```bash
pip install -r requirements.txt
```

### Option 2: Full Installation (With Windows shortcuts)
```bash
# Install core dependencies
pip install -r requirements.txt

# Install Windows optional dependencies
pip install winshell pywin32
```

### Option 3: Development Installation
```bash
# Install with modern setup
pip install -e .[windows,dev]
```

## Dependencies Explained

### Core Dependencies (Required)
- **PySide6**: Modern Qt6-based GUI framework
- **pyserial**: Serial communication with Arduino
- **keyboard**: Global hotkey detection
- **configparser**: Configuration file handling

### Optional Dependencies
- **winshell**: Windows desktop shortcut creation
- **pywin32**: Windows COM interface for shortcuts

### Development Dependencies (Optional)
- **pytest**: Unit testing framework
- **black**: Code formatting
- **flake8**: Code linting
- **mypy**: Static type checking

## Running the Application

After installation, run:
```bash
python src/main.py
```

Or if using modern setup:
```bash
serial-control
```

## Notes

- The application works perfectly without optional dependencies
- Windows shortcuts are convenience features only
- All core functionality is available with basic installation
- Optional dependencies are only needed for `setup.py` desktop shortcut creation
