"""
Key mappings for Serial Input Monitor.
Contains all keyboard key code mappings for both technical and friendly names.

Author: Leonardo Klein
"""

# Technical key names mapping (hexadecimal code to technical name)
TECHNICAL_KEY_MAP = {
    "08": "BACKSPACE",
    "09": "TAB",
    "0D": "ENTER",
    "10": "SHIFT",
    "11": "CTRL",
    "12": "ALT",
    "13": "PAUSE",
    "14": "CAPS_LOCK",
    "1B": "ESC",
    "20": "SPACE",
    "21": "PAGE_UP",
    "22": "PAGE_DOWN",
    "23": "END",
    "24": "HOME",
    "25": "LEFT_ARROW",
    "26": "UP_ARROW",
    "27": "RIGHT_ARROW",
    "28": "DOWN_ARROW",
    "2C": "PRINT_SCREEN",
    "2D": "INSERT",
    "2E": "DELETE",
    "70": "F1",
    "71": "F2",
    "72": "F3",
    "73": "F4",
    "74": "F5",
    "75": "F6",
    "76": "F7",
    "77": "F8",
    "78": "F9",
    "79": "F10",
    "7A": "F11",
    "7B": "F12",
}

# User-friendly key names mapping (hexadecimal code to friendly name)
FRIENDLY_KEY_MAP = {
    "0D": "ENTER",
    "08": "BACKSPACE",
    "09": "TAB",
    "10": "SHIFT",
    "11": "CTRL",
    "12": "ALT",
    "1B": "ESCAPE",
    "20": "SPACE",
    "25": "LEFT ARROW",
    "26": "UP ARROW",
    "27": "RIGHT ARROW",
    "28": "DOWN ARROW",
    "2E": "DELETE",
    "21": "PAGE UP",
    "22": "PAGE DOWN",
    "23": "END",
    "24": "HOME",
    "2D": "INSERT",
    "90": "NUM LOCK",
    "91": "SCROLL LOCK",
    "14": "CAPS LOCK",
    "13": "PAUSE",
    "2C": "PRINT SCREEN",
    "A0": "LEFT SHIFT",
    "A1": "RIGHT SHIFT",
    "A2": "LEFT CTRL",
    "A3": "RIGHT CTRL",
    "A4": "LEFT ALT",
    "A5": "RIGHT ALT",
    "5B": "LEFT WINDOWS",
    "5C": "RIGHT WINDOWS",
    "5D": "MENU",
    "BA": "SEMICOLON",
    "BB": "EQUALS",
    "BC": "COMMA",
    "BD": "MINUS",
    "BE": "PERIOD",
    "BF": "SLASH",
    "C0": "BACKTICK",
    "DB": "LEFT BRACKET",
    "DC": "BACKSLASH",
    "DD": "RIGHT BRACKET",
    "DE": "QUOTE",
    "6A": "NUMPAD MULTIPLY",
    "6B": "NUMPAD PLUS",
    "6D": "NUMPAD MINUS",
    "6E": "NUMPAD PERIOD",
    "6F": "NUMPAD DIVIDE",
    "70": "F1",
    "71": "F2",
    "72": "F3",
    "73": "F4",
    "74": "F5",
    "75": "F6",
    "76": "F7",
    "77": "F8",
    "78": "F9",
    "79": "F10",
    "7A": "F11",
    "7B": "F12",
    # Special control characters
    "0": "NULL",
    "1": "SOH",
    "2": "STX",
    "3": "ETX",
    "4": "EOT",
    "5": "ENQ",
    "6": "ACK",
    "7": "BELL",
    "A": "LINE FEED",
    "B": "VERTICAL TAB",
    "C": "FORM FEED",
    "E": "SHIFT OUT",
    "F": "SHIFT IN",
    "15": "NAK",
    "16": "SYN",
    "17": "ETB",
    "18": "CANCEL",
    "19": "EM",
    "1A": "SUB",
    "1C": "FILE SEPARATOR",
    "1D": "GROUP SEPARATOR",
    "1E": "RECORD SEPARATOR",
    "1F": "UNIT SEPARATOR",
    # OEM and system keys
    "92": "OEM_102",
    "93": "ICO_HELP",
    "94": "ICO_00",
    "96": "ICO_CLEAR",
    "E1": "OEM_SPECIFIC",
    "E3": "ICO_HELP",
    "E4": "ICO_00",
    "E6": "ICO_CLEAR",
    "E9": "OEM_RESET",
    "EA": "OEM_JUMP",
    "EB": "OEM_PA1",
    "EC": "OEM_PA2",
    "ED": "OEM_PA3",
    "EE": "OEM_WSCTRL",
    "EF": "OEM_CUSEL",
    "F0": "OEM_ATTN",
    "F1": "OEM_FINISH",
    "F2": "OEM_COPY",
    "F3": "OEM_AUTO",
    "F4": "OEM_ENLW",
    "F5": "OEM_BACKTAB",
    "F6": "ATTN",
    "F7": "CRSEL",
    "F8": "EXSEL",
    "F9": "EREOF",
    "FA": "PLAY",
    "FB": "ZOOM",
    "FC": "NONAME",
    "FD": "PA1",
    "FE": "OEM_CLEAR",
    "FF": "NONE",
    "07": "BEEP",
    "0A": "LINEFEED",
    "0B": "CLEAR",
    "0C": "CLEAR",
    "0E": "SHIFT_OUT",
    "0F": "SHIFT_IN",
    # Extended keys
    "160": "ENTER",
    "161": "SHIFT",
    "162": "CTRL",
    "163": "ALT",
    "164": "ALT GR",
}

# Keyboard module mapping for emulation (hexadecimal code to keyboard module name)
KEYBOARD_MODULE_MAP = {
    "08": "backspace",
    "09": "tab",
    "0D": "enter",
    "10": "shift",
    "11": "ctrl",
    "12": "alt",
    "1B": "esc",
    "20": "space",
    "25": "left",
    "26": "up",
    "27": "right",
    "28": "down",
    "2E": "delete",
    "70": "f1",
    "71": "f2",
    "72": "f3",
    "73": "f4",
}


def get_technical_key_name(key_code: str) -> str:
    """
    Get technical key name from hexadecimal code.

    :param key_code: Hexadecimal key code
    :return: Technical key name
    """
    key_map = TECHNICAL_KEY_MAP.copy()

    # Add numeric keys 0-9
    for i in range(10):
        key_map[f"{48 + i:02X}"] = str(i)

    # Add letters A-Z
    for i in range(26):
        key_map[f"{65 + i:02X}"] = chr(65 + i)

    return key_map.get(key_code.upper(), f"KEY_{key_code}")


def get_friendly_key_name(key_code: str) -> str:
    """
    Get user-friendly key name from hexadecimal code.

    :param key_code: Hexadecimal key code
    :return: Friendly key name
    """
    friendly_map = FRIENDLY_KEY_MAP.copy()

    # Add numeric keys 0-9
    for i in range(10):
        friendly_map[f"{48 + i:02X}"] = f"NUMBER {i}"
        friendly_map[f"{96 + i:02X}"] = f"NUMPAD {i}"

    # Add letters A-Z
    for i in range(26):
        friendly_map[f"{65 + i:02X}"] = f"LETTER {chr(65 + i)}"

    # Special handling for 3-digit codes
    code_upper = key_code.upper()
    if code_upper == "160":
        return "ENTER"
    elif code_upper.startswith("16") and len(code_upper) == 3:
        return f"EXTENDED KEY ({code_upper})"

    return friendly_map.get(code_upper, f"UNKNOWN KEY (0x{code_upper})")


def get_keyboard_module_name(key_code: str) -> str:
    """
    Get keyboard module key name for emulation.

    :param key_code: Hexadecimal key code
    :return: Keyboard module key name or empty string if not found
    """
    code_map = KEYBOARD_MODULE_MAP.copy()

    # Add numbers 0-9
    for i in range(10):
        code_map[f"{48 + i:02X}"] = str(i)

    # Add letters A-Z (lowercase for keyboard module)
    for i in range(26):
        code_map[f"{65 + i:02X}"] = chr(97 + i)

    return code_map.get(key_code.upper(), "")
