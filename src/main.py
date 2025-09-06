"""
Serial Input Monitor
Main interface for communication with Arduino via serial port.
Uses UI file created with Qt Designer.

Author: Leonardo Klein
"""

import sys
import logging
import configparser
import re
import time
from pathlib import Path
from typing import Optional
from PySide6.QtWidgets import QApplication, QDialog, QMessageBox
from PySide6.QtCore import QThread, Signal, QEvent, Qt
from PySide6.QtGui import QFont
import serial
import serial.tools.list_ports
import keyboard

from ui.main_ui import Ui_main_ui
from key_mappings import (
    get_technical_key_name,
    get_friendly_key_name,
    get_keyboard_module_name,
)


class SerialWorker(QThread):
    """
    Worker thread for non-blocking serial communication.
    """

    data_received = Signal(str)
    error_occurred = Signal(str)
    port_opened = Signal()
    port_closed = Signal()
    baud_rate_detected = Signal(int)

    COMMON_BAUD_RATES = [9600, 115200, 57600, 38400, 19200, 14400, 4800, 2400, 1200]

    def __init__(self, keyboard_emulator=None, mouse_emulator=None, config_manager=None):
        super().__init__()
        self.serial_connection: Optional[serial.Serial] = None
        self.running = False
        self.port_name = ""
        self.baud_rate = 9600
        self.auto_detect_baud = True
        self.keyboard_emulator = keyboard_emulator
        self.mouse_emulator = mouse_emulator
        self.config_manager = config_manager

    def get_prioritized_baud_rates(self, preferred_rate: int) -> list:
        """
        Get baud rates list with preferred rate first.

        :param preferred_rate: Previously detected or configured rate
        :return: Prioritized list of baud rates
        """
        rates = self.COMMON_BAUD_RATES.copy()
        if preferred_rate in rates:
            rates.remove(preferred_rate)
            rates.insert(0, preferred_rate)
        return rates

    def set_port_config(
        self, port_name: str, baud_rate: int = 9600, auto_detect: bool = True
    ):
        """
        Configure serial port parameters.

        :param port_name: COM port name
        :param baud_rate: Transmission rate (used as fallback if auto-detect fails)
        :param auto_detect: Whether to auto-detect baud rate
        """
        self.port_name = port_name
        self.baud_rate = baud_rate
        self.auto_detect_baud = auto_detect

    def detect_baud_rate(self) -> int:
        """
        Auto-detect the correct baud rate by testing common rates.

        :return: Detected baud rate or fallback rate
        """
        if not self.auto_detect_baud:
            return self.baud_rate

        self.data_received.emit("Auto-detecting baud rate...")

        prioritized_rates = self.get_prioritized_baud_rates(self.baud_rate)

        for i, baud_rate in enumerate(prioritized_rates):
            try:
                self.data_received.emit(
                    f"Testing baud rate {baud_rate}... ({i + 1}/{len(prioritized_rates)})"
                )

                timeout_val = 1.0
                if self.config_manager:
                    timeout_val = self.config_manager.get_serial_timeout()
                test_serial = serial.Serial(
                    port=self.port_name, baudrate=baud_rate, timeout=timeout_val
                )

                test_serial.reset_input_buffer()
                self.msleep(50)

                data_count = 0
                valid_data_received = False
                any_data_received = False

                for _ in range(3):
                    if test_serial.in_waiting > 0:
                        try:
                            data = (
                                test_serial.readline()
                                .decode("utf-8", errors="ignore")
                                .strip()
                            )
                            if data:
                                data_count += 1
                                any_data_received = True
                                self.data_received.emit(f"  Data received: {data}")
                                if self.is_valid_data_format(data):
                                    valid_data_received = True
                                    break
                        except Exception:
                            pass
                    self.msleep(50)

                test_serial.close()

                if valid_data_received:
                    self.data_received.emit(
                        f"Baud rate {baud_rate} detected (valid data received)"
                    )
                    self.baud_rate_detected.emit(baud_rate)
                    return baud_rate
                elif any_data_received:
                    self.data_received.emit(
                        f"Baud rate {baud_rate} accepted (data detected)"
                    )
                    self.baud_rate_detected.emit(baud_rate)
                    return baud_rate

                if i < 2:
                    self.data_received.emit(
                        f"Baud rate {baud_rate} - no data, trying next..."
                    )
                else:
                    self.data_received.emit(f"Baud rate {baud_rate} - no data received")

            except Exception as e:
                self.data_received.emit(f"Baud rate {baud_rate} failed: {str(e)}")
                continue

        self.data_received.emit(
            f"Auto-detection completed, using rate {self.baud_rate}"
        )
        return self.baud_rate

    def is_valid_data_format(self, data: str) -> bool:
        """
        Check if received data matches expected Arduino format.

        :param data: Data string to validate
        :return: True if data appears to be in expected format
        """
        parts = data.strip().split()

        if len(parts) >= 2:
            try:
                device = int(parts[0])
                event = int(parts[1])
                if device in [0, 1] and 0 <= event <= 20:
                    return True
            except ValueError:
                pass

        if len(parts) >= 3:
            try:
                device = int(parts[0])
                event = int(parts[1])
                if device in [0, 1] and 0 <= event <= 20:
                    try:
                        int(parts[2])
                        return True
                    except ValueError:
                        try:
                            int(parts[2], 16)
                            return True
                        except ValueError:
                            pass
            except ValueError:
                pass

        if len(parts) == 1:
            try:
                value = int(parts[0])
                if 0 <= value <= 65535:
                    return True
            except ValueError:
                pass

        return False

    def open_port(self):
        """Open serial connection with auto baud rate detection."""
        try:
            self.data_received.emit(f"Opening port {self.port_name}...")

            detected_baud = self.baud_rate

            if self.auto_detect_baud:
                self.data_received.emit("Starting baud rate detection...")
                detected_baud = self.detect_baud_rate()
            else:
                self.data_received.emit(f"Using configured baud rate: {self.baud_rate}")

            timeout_val = 1.0
            if self.config_manager:
                timeout_val = self.config_manager.get_serial_timeout()
            self.serial_connection = serial.Serial(
                port=self.port_name, baudrate=detected_baud, timeout=timeout_val
            )
            self.running = True
            self.data_received.emit(
                f"Port {self.port_name} opened successfully at {detected_baud} baud"
            )
            self.port_opened.emit()
            self.start()
        except Exception as e:
            error_msg = f"Error opening port {self.port_name}: {str(e)}"
            self.error_occurred.emit(error_msg)
            logging.exception(error_msg)

    def close_port(self):
        """Close serial connection."""
        self.running = False
        if self.serial_connection and self.serial_connection.is_open:
            try:
                self.serial_connection.close()
                self.data_received.emit(f"Port {self.port_name} closed")
                self.port_closed.emit()
            except Exception as e:
                error_msg = f"Error closing port: {str(e)}"
                self.error_occurred.emit(error_msg)
                logging.exception(error_msg)
        self.wait()

    def run(self):
        """Main serial reading loop."""
        while (
            self.running and self.serial_connection and self.serial_connection.is_open
        ):
            try:
                if self.serial_connection.in_waiting > 0:
                    data = self.serial_connection.readline().decode("utf-8").strip()
                    if data:
                        self.parse_received_data(data)
                self.msleep(10)
            except Exception as e:
                if self.running:
                    error_msg = f"Serial reading error: {str(e)}"
                    self.error_occurred.emit(error_msg)
                    logging.exception(error_msg)
                break

    def parse_received_data(self, data: str):
        """
        Parse data received from Arduino and emit formatted logs.

        :param data: Data received from serial port
        """
        try:
            data = data.strip()
            if not data:
                return

            if data.startswith("#"):
                comment_msg = f"<span style='color:#888888; font-style:italic;'>Comment: {data[1:].strip()}</span>"
                self.data_received.emit(comment_msg)
                return

            parts = data.split()

            if len(parts) >= 3:
                device = parts[0]
                event = parts[1]
                key_code = parts[2]

                try:
                    device_num = int(device)
                    event_num = int(event)
                except ValueError:
                    formatted_data = self.format_unknown_data(data)
                    self.data_received.emit(formatted_data)
                    return

                if device_num == 1:
                    if event_num in [0, 1]:
                        key_name = get_technical_key_name(key_code)
                        friendly_name = get_friendly_key_name(key_code)
                        action = "pressed" if event_num == 1 else "released"
                        log_msg = f"{friendly_name} (0x{key_code.upper()} {key_name}) {action}"
                        self.data_received.emit(log_msg)
                        
                        if event_num == 1:
                            if self.keyboard_emulator:
                                self.keyboard_emulator.press_key(key_code)
                        else:
                            if self.keyboard_emulator:
                                self.keyboard_emulator.release_key(key_code)
                    else:
                        self.data_received.emit(
                            f"Invalid keyboard event (event={event_num}, key={key_code})"
                        )

                elif device_num == 0:
                    self.parse_mouse_event(event, parts[2:])

                else:
                    formatted_data = self.format_unknown_data(data)
                    self.data_received.emit(formatted_data)

            else:
                formatted_data = self.format_unknown_data(data)
                self.data_received.emit(formatted_data)

        except Exception:
            logging.exception(f"Error parsing data: {data}")
            try:
                formatted_data = self.format_unknown_data(data)
                self.data_received.emit(formatted_data)
            except Exception:
                self.data_received.emit(f"Critical error parsing data: {data}")

    def format_unknown_data(self, data: str) -> str:
        """
        Format unknown data with friendly description.

        :param data: Raw data string
        :return: Formatted message with friendly description
        """
        data = data.strip()
        parts = data.split()

        if len(parts) == 1:
            try:
                num_value = int(parts[0])
                if 0 <= num_value <= 255:
                    return f"Sensor reading (value={num_value}) detected"
                elif num_value > 1000:
                    return f"Large sensor value (value={num_value}) detected"
                else:
                    return f"Numeric data (value={num_value}) received"
            except ValueError:
                if parts[0].isalnum():
                    return f"Alphanumeric code ({parts[0]}) received"
                else:
                    return f"Text data ({parts[0]}) received"

        elif len(parts) == 2:
            device, event = parts
            try:
                dev_num = int(device)
                evt_num = int(event)
                if dev_num == 0:
                    return (
                        f"Mouse event incomplete (event={evt_num}) - missing parameters"
                    )
                elif dev_num == 1:
                    action = (
                        "pressed"
                        if evt_num == 1
                        else "released"
                        if evt_num == 0
                        else f"action_{evt_num}"
                    )
                    return (
                        f"Keyboard event incomplete (key {action}) - missing key code"
                    )
                else:
                    return f"Unknown device {dev_num} event {evt_num} - incomplete data"
            except ValueError:
                return f"Non-numeric device data ({device}, {event}) received"

        elif len(parts) == 3:
            device, event, code = parts
            try:
                dev_num = int(device)
                evt_num = int(event)
                if dev_num == 1:
                    action = (
                        "pressed"
                        if evt_num == 1
                        else "released"
                        if evt_num == 0
                        else f"action_{evt_num}"
                    )
                    return f"Unknown keyboard key (code={code}) {action}"
                elif dev_num == 0:
                    return (
                        f"Unknown mouse event (type={evt_num}, param={code}) detected"
                    )
                else:
                    return f"Unknown device {dev_num} input (event={evt_num}, code={code}) received"
            except ValueError:
                return f"Malformed device data ({device}, {event}, {code}) received"

        elif len(parts) > 3:
            if parts[0] == "0":
                return f"Complex mouse data ({' '.join(parts[1:])}) received"
            else:
                return f"Multi-parameter data ({' '.join(parts)}) received"

        else:
            if not data:
                return "Empty data packet received"
            else:
                return f"Unrecognized data format ({data}) received"

    def parse_mouse_event(self, event: str, params: list):
        """
        Parse mouse events.

        :param event: Mouse event type
        :param params: Event parameters
        """
        event_map = {
            "0": "RIGHT BUTTON",
            "1": "RIGHT BUTTON",
            "2": "LEFT BUTTON",
            "3": "LEFT BUTTON",
            "4": "MIDDLE BUTTON",
            "5": "MIDDLE BUTTON",
            "6": "SCROLL WHEEL",
            "7": "CURSOR POSITION",
            "8": "CURSOR MOVEMENT",
        }

        action_map = {
            "0": "pressed",
            "1": "released",
            "2": "pressed",
            "3": "released",
            "4": "pressed",
            "5": "released",
            "6": "scrolled",
            "7": "positioned",
            "8": "moved",
        }

        event_name = event_map.get(event, "UNKNOWN MOUSE EVENT")
        action = action_map.get(event, "detected")

        # Execute mouse actions if emulator is available and enabled
        if self.mouse_emulator and self.mouse_emulator.enabled:
            try:
                if event == "2":  # Left button pressed
                    self.mouse_emulator.click_left()
                elif event == "0":  # Right button pressed
                    self.mouse_emulator.click_right()
                elif event == "4":  # Middle button pressed (not implemented in MouseEmulator)
                    pass
                elif event == "6" and len(params) >= 1:  # Scroll wheel
                    delta = int(params[0])
                    self.mouse_emulator.scroll(delta)
                elif event in ["7", "8"] and len(params) >= 2:  # Position/Movement
                    x, y = int(params[0]), int(params[1])
                    if event == "7":  # Position
                        self.mouse_emulator.set_position(x, y)
                    else:  # Movement (relative)
                        self.mouse_emulator.move_relative(x, y)
            except Exception as e:
                self.data_received.emit(f"Mouse emulation error: {str(e)}")

        if len(params) >= 2 and event in ["7", "8"]:
            log_msg = (
                f"Mouse {event_name.lower()} (X={params[0]}, Y={params[1]}) {action}"
            )
        elif len(params) >= 1 and event == "6":
            direction = (
                "up"
                if int(params[0]) > 0
                else "down"
                if int(params[0]) < 0
                else "neutral"
            )
            log_msg = (
                f"Mouse {event_name.lower()} (delta={params[0]}) scrolled {direction}"
            )
        else:
            log_msg = f"Mouse {event_name.lower()} {action}"

        self.data_received.emit(log_msg)


class MouseEmulator:
    """
    Class for emulating mouse events on Windows using ctypes.
    """

    def __init__(self):
        self.enabled = False

    def set_enabled(self, enabled: bool):
        """Enable/disable mouse emulation."""
        self.enabled = enabled

    def click_left(self):
        """Perform left mouse click."""
        if not self.enabled:
            return
        try:
            import ctypes
            ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0, 0)  # LEFTDOWN
            ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0, 0)  # LEFTUP
        except Exception as e:
            logging.exception(f"Error with left click: {e}")

    def click_right(self):
        """Perform right mouse click."""
        if not self.enabled:
            return
        try:
            import ctypes
            ctypes.windll.user32.mouse_event(0x0008, 0, 0, 0, 0)  # RIGHTDOWN
            ctypes.windll.user32.mouse_event(0x0010, 0, 0, 0, 0)  # RIGHTUP
        except Exception as e:
            logging.exception(f"Error with right click: {e}")

    def set_position(self, x: int, y: int):
        """Set mouse position."""
        if not self.enabled:
            return
        try:
            import ctypes
            ctypes.windll.user32.SetCursorPos(x, y)
        except Exception as e:
            logging.exception(f"Error setting mouse position: {e}")

    def move_relative(self, dx: int, dy: int):
        """Move mouse relative to current position."""
        if not self.enabled:
            return
        try:
            import ctypes
            ctypes.windll.user32.mouse_event(0x0001, dx, dy, 0, 0)  # MOVE
        except Exception as e:
            logging.exception(f"Error moving mouse: {e}")

    def scroll(self, amount: int):
        """Scroll mouse wheel."""
        if not self.enabled:
            return
        try:
            import ctypes
            wheel_delta = amount * 120
            ctypes.windll.user32.mouse_event(0x0800, 0, 0, wheel_delta, 0)  # WHEEL
        except Exception as e:
            logging.exception(f"Error scrolling: {e}")


class KeyboardEmulator:
    """
    Class for emulating keyboard events on Windows.
    """

    def __init__(self):
        self.enabled = False

    def set_enabled(self, enabled: bool):
        """Enable/disable keyboard emulation."""
        self.enabled = enabled

    def press_key(self, key_code: str):
        """
        Press a key on Windows.

        :param key_code: Key code in hexadecimal
        """
        if not self.enabled:
            return

        try:
            key_name = get_keyboard_module_name(key_code)
            if key_name:
                keyboard.press(key_name)
        except Exception as e:
            logging.exception(f"Error pressing key {key_code}: {e}")

    def release_key(self, key_code: str):
        """
        Release a key on Windows.

        :param key_code: Key code in hexadecimal
        """
        if not self.enabled:
            return

        try:
            key_name = get_keyboard_module_name(key_code)
            if key_name:
                keyboard.release(key_name)
        except Exception as e:
            logging.exception(f"Error releasing key {key_code}: {e}")


class ConfigManager:
    """
    Application configuration manager.
    """

    def __init__(self):
        self.config_file = Path("config.ini")
        self.config = configparser.ConfigParser()
        self.load_config()

    def load_config(self):
        """Load configurations from file."""
        if self.config_file.exists():
            try:
                self.config.read(self.config_file)
            except Exception as e:
                logging.exception(f"Error loading configuration: {e}")
        else:
            self._create_default_config()

    def _create_default_config(self):
        """Create default configuration."""
        self.config["HOTKEYS"] = {"start": "F9", "stop": "F10"}
        self.config["SERIAL"] = {
            "last_port": "",
            "baud_rate": "9600",
            "auto_detect_baud": "true",
            "detected_baud_rate": "9600",
        }
        self.config["UI"] = {
            "theme": "default",
            "log_font_family": "Consolas",
            "log_font_size": "9",
            "technical_color": "#888888",
        }
        self.save_config()

    def save_config(self):
        """Save configurations to file."""
        try:
            with open(self.config_file, "w") as f:
                self.config.write(f)
        except Exception as e:
            logging.exception(f"Error saving configuration: {e}")

    def get_hotkey(self, action: str) -> str:
        """Return hotkey for specified action."""
        return self.config.get("HOTKEYS", action, fallback="")

    def set_hotkey(self, action: str, key: str):
        """Set hotkey for action."""
        if "HOTKEYS" not in self.config:
            self.config.add_section("HOTKEYS")
        self.config.set("HOTKEYS", action, key)
        self.save_config()

    def get_theme(self) -> str:
        """Return current theme name."""
        return self.config.get("UI", "theme", fallback="default")

    def set_theme(self, theme: str):
        """Set interface theme."""
        if "UI" not in self.config:
            self.config.add_section("UI")
        self.config.set("UI", "theme", theme)
        self.save_config()

    def get_last_port(self) -> str:
        """Return last used port."""
        return self.config.get("SERIAL", "last_port", fallback="")

    def set_last_port(self, port: str):
        """Set last used port."""
        if "SERIAL" not in self.config:
            self.config.add_section("SERIAL")
        self.config.set("SERIAL", "last_port", port)
        self.save_config()

    def get_detected_baud_rate(self) -> int:
        """Return last detected baud rate."""
        return self.config.getint("SERIAL", "detected_baud_rate", fallback=9600)

    def set_detected_baud_rate(self, baud_rate: int):
        """Set detected baud rate."""
        if "SERIAL" not in self.config:
            self.config.add_section("SERIAL")
        self.config.set("SERIAL", "detected_baud_rate", str(baud_rate))
        self.save_config()

    def get_log_font_family(self) -> str:
        """Return log font family."""
        return self.config.get("UI", "log_font_family", fallback="Consolas")

    def get_log_font_size(self) -> int:
        """Return log font size."""
        return self.config.getint("UI", "log_font_size", fallback=9)

    def get_technical_color(self) -> str:
        """Return color for technical details in parentheses."""
        return self.config.get("UI", "technical_color", fallback="#888888")

    def get_auto_detect_baud(self) -> bool:
        """Return whether to auto-detect baud rate."""
        return self.config.getboolean("SERIAL", "auto_detect_baud", fallback=True)

    def set_auto_detect_baud(self, auto_detect: bool):
        """Set auto-detect baud rate option."""
        if "SERIAL" not in self.config:
            self.config.add_section("SERIAL")
        self.config.set("SERIAL", "auto_detect_baud", str(auto_detect).lower())
        self.save_config()

    def get_serial_timeout(self) -> float:
        """Return serial timeout value."""
        return self.config.getfloat("SERIAL", "timeout", fallback=1.0)

    def get_test_timeout(self) -> float:
        """Return port test timeout value."""
        return self.config.getfloat("SERIAL", "test_timeout", fallback=0.5)

    def get_max_log_lines(self) -> int:
        """Return maximum number of log lines."""
        return self.config.getint("UI", "max_log_lines", fallback=1000)

    def get_enable_debug(self) -> bool:
        """Return whether debug logging is enabled."""
        return self.config.getboolean("DEBUG", "enable_debug", fallback=False)

    def get_save_logs_to_file(self) -> bool:
        """Return whether to save logs to file."""
        return self.config.getboolean("DEBUG", "save_logs_to_file", fallback=True)

    def get_log_filename(self) -> str:
        """Return log filename."""
        return self.config.get("DEBUG", "log_filename", fallback="serial_control.log")


class MainWindow(QDialog):
    """Main application window for Serial Input Monitor."""

    error_signal = Signal(str)
    status_signal = Signal(str)
    update_ui_signal = Signal()
    log_signal = Signal(str)

    def __init__(self) -> None:
        """Initialize the main window."""
        super().__init__()
        self.config_manager = ConfigManager()
        self.keyboard_emulator = KeyboardEmulator()
        self.mouse_emulator = MouseEmulator()
        self.serial_worker = SerialWorker(self.keyboard_emulator, self.mouse_emulator, self.config_manager)
        self.port_is_open = False
        self.emulation_enabled = False
        self.port_checked = False
        self.log_lines_count = 0

        self.ui = Ui_main_ui()
        self.ui.setupUi(self)

        self.setup_ui_connections()
        self.setup_connections()
        self.setup_hotkeys()
        self.refresh_com_ports()
        self.apply_theme()

    def setup_ui_connections(self) -> None:
        """Map UI elements from the .ui file to instance variables."""
        self.combo_ports = self.ui.combo_ports
        self.btn_check = self.ui.button_check
        self.btn_open_port = self.ui.button_open
        self.btn_close_port = self.ui.button_close
        self.btn_start = self.ui.button_start
        self.btn_stop = self.ui.button_stop
        self.edit_hotkey_start = self.ui.input_hotkey_start
        self.edit_hotkey_stop = self.ui.input_hotkey_stop
        self.btn_save_hotkeys_start = self.ui.button_hotkey_start_ok
        self.btn_save_hotkeys_stop = self.ui.button_hotkey_stop_ok
        self.text_log = self.ui.textarea_status

        font_family = self.config_manager.get_log_font_family()
        font_size = self.config_manager.get_log_font_size()
        self.text_log.setFont(QFont(font_family, font_size))

        self.edit_hotkey_start.setReadOnly(True)
        self.edit_hotkey_stop.setReadOnly(True)
        self.edit_hotkey_start.setPlaceholderText(
            "Click here and press key combination"
        )
        self.edit_hotkey_stop.setPlaceholderText("Click here and press key combination")

        self.update_ui_state()

    def setup_connections(self):
        """Configure signal connections."""
        self.btn_check.clicked.connect(self.check_port)
        self.btn_open_port.clicked.connect(self.open_port)
        self.btn_close_port.clicked.connect(self.close_port)
        self.btn_start.clicked.connect(self.start_emulation)
        self.btn_stop.clicked.connect(self.stop_emulation)
        self.btn_save_hotkeys_start.clicked.connect(self.save_hotkeys)
        self.btn_save_hotkeys_stop.clicked.connect(self.save_hotkeys)

        self.combo_ports.currentTextChanged.connect(self.on_port_selection_changed)

        self.combo_ports.activated.connect(self.on_combo_activated)

        self.edit_hotkey_start.installEventFilter(self)
        self.edit_hotkey_stop.installEventFilter(self)

        self.serial_worker.data_received.connect(self.append_log)
        self.serial_worker.error_occurred.connect(self.show_error)
        self.serial_worker.port_opened.connect(self.on_port_opened)
        self.serial_worker.port_closed.connect(self.on_port_closed)
        self.serial_worker.baud_rate_detected.connect(self.on_baud_rate_detected)

        self.error_signal.connect(self.show_error_safe)
        self.status_signal.connect(self.show_status_safe)
        self.update_ui_signal.connect(self.update_ui_state)
        self.log_signal.connect(self.append_log)

    def setup_hotkeys(self):
        """Configure global hotkeys."""
        self.edit_hotkey_start.setText(self.config_manager.get_hotkey("start").upper())
        self.edit_hotkey_stop.setText(self.config_manager.get_hotkey("stop").upper())

        self.register_hotkeys()

    def start_emulation_hotkey(self):
        """Thread-safe version for hotkey activation."""
        if self.edit_hotkey_start.hasFocus() or self.edit_hotkey_stop.hasFocus():
            return
        if not self.port_is_open:
            self.error_signal.emit("Open a serial port first")
            return

        self.emulation_enabled = True
        self.keyboard_emulator.set_enabled(True)
        self.mouse_emulator.set_enabled(True)
        self.update_ui_signal.emit()
        self.log_signal.emit("Keyboard and mouse emulation STARTED")
        self.status_signal.emit("Emulation active")
        
        # Set focus to stop button to avoid hotkey field interference  
        self.btn_stop.setFocus()

    def stop_emulation_hotkey(self):
        """Thread-safe version for hotkey deactivation."""
        if self.edit_hotkey_start.hasFocus() or self.edit_hotkey_stop.hasFocus():
            return
        self.emulation_enabled = False
        self.keyboard_emulator.set_enabled(False)
        self.mouse_emulator.set_enabled(False)
        self.update_ui_signal.emit()
        self.log_signal.emit("Keyboard and mouse emulation STOPPED")
        self.status_signal.emit("Emulation inactive")

    def apply_theme(self):
        """Apply selected theme to interface."""
        try:
            theme_name = self.config_manager.get_theme()
            qss_file = Path(f"src/ui/themes/{theme_name}.qss")

            if not qss_file.exists():
                qss_file = Path("src/ui/themes/default.qss")

            if qss_file.exists():
                with open(qss_file, "r", encoding="utf-8") as f:
                    self.setStyleSheet(f.read())
                logging.debug(f"Applied theme: {theme_name}")
            else:
                logging.warning("No theme files found, using system default")
        except Exception as e:
            logging.exception(f"Error loading theme: {e}")

    def refresh_com_ports(self):
        """Update available COM ports list."""
        self.combo_ports.clear()
        ports = serial.tools.list_ports.comports()

        for port in ports:
            self.combo_ports.addItem(f"{port.device} - {port.description}")

        if not ports:
            self.combo_ports.addItem("No ports found")

        last_port = self.config_manager.get_last_port()
        if last_port:
            for i in range(self.combo_ports.count()):
                if last_port in self.combo_ports.itemText(i):
                    self.combo_ports.setCurrentIndex(i)
                    break

    def on_port_selection_changed(self):
        """Called when port selection changes."""
        self.port_checked = False
        self.update_ui_state()

    def on_combo_activated(self):
        self.port_checked = False
        self.refresh_com_ports()

    def check_port(self):
        """Check if selected port is available."""
        port_text = self.combo_ports.currentText()
        if not port_text or "No ports" in port_text:
            self.show_error("Select a valid port")
            return

        port_name = port_text.split(" - ")[0]

        try:
            timeout_val = 0.5
            if hasattr(self, 'config_manager') and self.config_manager:
                timeout_val = self.config_manager.get_test_timeout()
            test_serial = serial.Serial(port_name, 9600, timeout=timeout_val)
            test_serial.close()
            self.port_checked = True
            self.append_log(f"Port {port_name} is available")
            self.show_status(f"Port {port_name} checked - OK", 3000)
            self.update_ui_state()
        except Exception as e:
            self.port_checked = False
            self.show_error(f"Error checking port {port_name}: {str(e)}")
            self.update_ui_state()

    def open_port(self):
        """Open selected serial port with auto baud rate detection."""
        port_text = self.combo_ports.currentText()
        if not port_text or "No ports" in port_text:
            self.show_error("Select a valid port")
            return

        if not self.port_checked:
            self.show_error(
                "Port must be checked before opening. Click 'Check' button first."
            )
            return

        port_name = port_text.split(" - ")[0]

        fallback_baud = self.config_manager.get_detected_baud_rate()
        auto_detect = self.config_manager.get_auto_detect_baud()

        if auto_detect:
            self.append_log("Auto-detection enabled. Quick test in progress...")

            quick_test = self.quick_data_test(port_name, fallback_baud)
            if not quick_test:
                auto_detect = False
                self.append_log(
                    "No data detected during quick test. Skipping auto-detection."
                )
                self.append_log(f"Using last known baud rate: {fallback_baud}")
            else:
                self.append_log("Data detected. Proceeding with baud rate detection...")
        else:
            self.append_log(
                f"Auto-detection disabled. Using configured baud rate: {fallback_baud}"
            )

        self.serial_worker.set_port_config(
            port_name, fallback_baud, auto_detect=auto_detect
        )
        self.serial_worker.open_port()

        self.config_manager.set_last_port(port_name)

    def quick_data_test(self, port_name: str, baud_rate: int) -> bool:
        """
        Quick test to see if there's any data being transmitted.

        :param port_name: COM port name
        :param baud_rate: Baud rate to test
        :return: True if data detected, False otherwise
        """
        try:
            timeout_val = 0.5
            if hasattr(self, 'config_manager') and self.config_manager:
                timeout_val = self.config_manager.get_test_timeout()
            test_serial = serial.Serial(port_name, baud_rate, timeout=timeout_val)
            test_serial.reset_input_buffer()

            for _ in range(5):
                if test_serial.in_waiting > 0:
                    test_serial.close()
                    return True
                time.sleep(0.1)

            test_serial.close()
            return False
        except Exception:
            return False

    def close_port(self):
        """Close serial port."""
        self.serial_worker.close_port()

    def on_port_opened(self):
        """Called when port is opened successfully."""
        self.port_is_open = True
        self.update_ui_state()
        self.show_status("Port opened", 3000)

    def on_port_closed(self):
        """Called when port is closed."""
        self.port_is_open = False
        self.emulation_enabled = False
        self.keyboard_emulator.set_enabled(False)
        self.update_ui_state()
        self.show_status("Port closed", 3000)

    def on_baud_rate_detected(self, baud_rate: int):
        """Called when baud rate is auto-detected."""
        self.append_log(f"Baud rate automatically detected: {baud_rate}")
        self.config_manager.set_detected_baud_rate(baud_rate)

    def start_emulation(self):
        """Start keyboard and mouse emulation."""
        if not self.port_is_open:
            self.error_signal.emit("Open a serial port first")
            return

        self.emulation_enabled = True
        self.keyboard_emulator.set_enabled(True)
        self.mouse_emulator.set_enabled(True)
        self.update_ui_state()
        self.append_log("Keyboard and mouse emulation STARTED")
        self.status_signal.emit("Emulation active")
        
        # Set focus to stop button to avoid hotkey field interference
        self.btn_stop.setFocus()

    def stop_emulation(self):
        """Stop keyboard and mouse emulation."""
        self.emulation_enabled = False
        self.keyboard_emulator.set_enabled(False)
        self.mouse_emulator.set_enabled(False)
        self.update_ui_state()
        self.append_log("Keyboard and mouse emulation STOPPED")
        self.status_signal.emit("Emulation inactive")

    def save_hotkeys(self):
        """Save configured hotkeys and apply them immediately."""
        try:
            start_key = self.edit_hotkey_start.text().strip()
            stop_key = self.edit_hotkey_stop.text().strip()

            keyboard.unhook_all_hotkeys()

            if start_key:
                self.config_manager.set_hotkey("start", start_key)
            if stop_key:
                self.config_manager.set_hotkey("stop", stop_key)

            self.register_hotkeys()

            self.show_status("Hotkeys saved and applied", 3000)
            self.append_log(f"Hotkeys saved: Start={start_key}, Stop={stop_key}")
        except Exception as e:
            self.show_error(f"Error saving hotkeys: {str(e)}")

    def register_hotkeys(self):
        """Register global hotkeys."""
        try:
            start_key = self.config_manager.get_hotkey("start")
            stop_key = self.config_manager.get_hotkey("stop")

            if start_key:
                keyboard.add_hotkey(start_key, self.start_emulation_hotkey)
            if stop_key:
                keyboard.add_hotkey(stop_key, self.stop_emulation_hotkey)
        except Exception as e:
            logging.exception(f"Error registering hotkeys: {e}")

    def update_ui_state(self):
        """Update interface controls state."""
        has_port_selected = bool(
            self.combo_ports.currentText()
            and "No ports" not in self.combo_ports.currentText()
        )

        self.btn_check.setEnabled(has_port_selected and not self.port_is_open)
        self.btn_open_port.setEnabled(
            has_port_selected and not self.port_is_open and self.port_checked
        )
        self.btn_close_port.setEnabled(self.port_is_open)

        self.combo_ports.setEnabled(not self.port_is_open)

        self.btn_start.setEnabled(self.port_is_open and not self.emulation_enabled)
        self.btn_stop.setEnabled(self.port_is_open and self.emulation_enabled)

        self.refresh_button_styles()

    def refresh_button_styles(self):
        """Force refresh of button styles to apply disabled states properly."""
        buttons = [
            self.btn_check,
            self.btn_open_port,
            self.btn_close_port,
            self.btn_start,
            self.btn_stop,
        ]

        for button in buttons:
            button.style().unpolish(button)
            button.style().polish(button)
            button.update()

        self.repaint()

    def append_log(self, message: str):
        """Add message to log with HTML formatting for technical details."""
        from datetime import datetime
        from PySide6.QtGui import QTextCursor

        timestamp = datetime.now().strftime("%H:%M:%S")

        # Check max log lines and truncate if needed
        max_lines = self.config_manager.get_max_log_lines()
        if max_lines > 0:
            self.log_lines_count += 1
            if self.log_lines_count > max_lines:
                # Clear half of the log to avoid frequent clearing
                cursor = self.text_log.textCursor()
                cursor.movePosition(QTextCursor.MoveOperation.Start)
                cursor.movePosition(QTextCursor.MoveOperation.Down, QTextCursor.MoveMode.KeepAnchor, max_lines // 2)
                cursor.removeSelectedText()
                self.log_lines_count = max_lines // 2

        # Save to file if enabled
        if self.config_manager.get_save_logs_to_file():
            try:
                log_filename = self.config_manager.get_log_filename()
                with open(log_filename, 'a', encoding='utf-8') as log_file:
                    log_file.write(f"[{timestamp}] {message}\n")
            except Exception as e:
                # Avoid infinite recursion by not using append_log here
                print(f"Error writing to log file: {e}")

        technical_color = self.config_manager.get_technical_color()

        formatted_message = re.sub(
            r"\(([^)]+)\)",
            f'<span style="color: {technical_color}; font-style: italic;">(\\1)</span>',
            message,
        )

        full_message = f"[{timestamp}] {formatted_message}"
        cursor = self.text_log.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.text_log.setTextCursor(cursor)
        self.text_log.insertHtml(full_message + "<br>")

    def append_debug_log(self, message: str):
        """Add debug message to log only if debug is enabled."""
        if self.config_manager.get_enable_debug():
            self.append_log(f"DEBUG: {message}")

    def show_error(self, message: str):
        """Display error message."""
        self.append_log(f"ERROR: {message}")
        QMessageBox.warning(self, "Error", message)

    def show_error_safe(self, message: str):
        """Thread-safe version of show_error."""
        self.append_log(f"ERROR: {message}")
        QMessageBox.warning(self, "Error", message)

    def show_status_safe(self, message: str):
        """Thread-safe version of show_status."""
        self.append_log(f"STATUS: {message}")

    def show_status(self, message: str, timeout: int = 0):
        """Show status message - using log since QDialog doesn't have status bar."""
        self.append_log(f"STATUS: {message}")

    def eventFilter(self, arg__1, arg__2):
        """Handle key events for hotkey input fields."""
        from PySide6.QtWidgets import QLineEdit

        if isinstance(arg__1, QLineEdit) and arg__1 in [
            self.edit_hotkey_start,
            self.edit_hotkey_stop,
        ]:
            if arg__2.type() == QEvent.Type.KeyPress:
                key_sequence = self.get_key_sequence(arg__2)
                if key_sequence:
                    arg__1.setText(key_sequence.upper())
                    arg__1.clearFocus()
                return True
            elif arg__2.type() == QEvent.Type.MouseButtonPress:
                arg__1.setText("")
                arg__1.setPlaceholderText("Press key combination...")
                return False
        return super().eventFilter(arg__1, arg__2)

    def get_key_sequence(self, event):
        """Convert QKeyEvent to string representation."""
        modifiers = []

        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            modifiers.append("ctrl")
        if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
            modifiers.append("shift")
        if event.modifiers() & Qt.KeyboardModifier.AltModifier:
            modifiers.append("alt")
        if event.modifiers() & Qt.KeyboardModifier.MetaModifier:
            modifiers.append("win")

        key = event.key()
        key_name = None

        if Qt.Key.Key_F1 <= key <= Qt.Key.Key_F24:
            key_name = f"f{key - Qt.Key.Key_F1 + 1}"
        elif Qt.Key.Key_0 <= key <= Qt.Key.Key_9:
            key_name = chr(key)
        elif Qt.Key.Key_A <= key <= Qt.Key.Key_Z:
            key_name = chr(key).lower()
        elif key == Qt.Key.Key_Space:
            key_name = "space"
        elif key == Qt.Key.Key_Enter or key == Qt.Key.Key_Return:
            key_name = "enter"
        elif key == Qt.Key.Key_Tab:
            key_name = "tab"
        elif key == Qt.Key.Key_Escape:
            key_name = "esc"
        elif key == Qt.Key.Key_Backspace:
            key_name = "backspace"
        elif key == Qt.Key.Key_Delete:
            key_name = "delete"
        elif key == Qt.Key.Key_Insert:
            key_name = "insert"
        elif key == Qt.Key.Key_Home:
            key_name = "home"
        elif key == Qt.Key.Key_End:
            key_name = "end"
        elif key == Qt.Key.Key_PageUp:
            key_name = "page up"
        elif key == Qt.Key.Key_PageDown:
            key_name = "page down"
        elif key == Qt.Key.Key_Up:
            key_name = "up"
        elif key == Qt.Key.Key_Down:
            key_name = "down"
        elif key == Qt.Key.Key_Left:
            key_name = "left"
        elif key == Qt.Key.Key_Right:
            key_name = "right"
        elif key in [
            Qt.Key.Key_Control,
            Qt.Key.Key_Shift,
            Qt.Key.Key_Alt,
            Qt.Key.Key_Meta,
        ]:
            return None

        if key_name:
            if modifiers:
                return "+".join(modifiers + [key_name])
            else:
                return key_name
        return None

    def closeEvent(self, arg__1):
        """Called when closing application."""
        if self.port_is_open:
            self.serial_worker.close_port()

        keyboard.unhook_all_hotkeys()

        arg__1.accept()


def setup_logging():
    """Configure logging system."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler("serial_control.log"), logging.StreamHandler()],
    )


def main():
    """Main application function."""
    setup_logging()

    app = QApplication(sys.argv)
    app.setApplicationName("Serial Input Monitor")
    app.setApplicationVersion("1.0.0")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
