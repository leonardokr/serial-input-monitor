/**
 * @file SerialInputMonitor.h
 * @brief Library for input monitoring and control via serial communication
 * @version 1.0.0
 * @date 2025-09-05
 *
 * This library enables remote monitoring and control of computer input devices
 * through commands sent via serial port. Compatible with Arduino Uno
 * and similar microcontrollers.
 *
 * Communication protocol:
 * DEVICE EVENT [PARAMS]
 *
 * Where:
 * - DEVICE: 0=Mouse, 1=Keyboard
 * - EVENT: Specific event code
 * - PARAMS: Optional parameters (coordinates, key codes, etc.)
 *
 * @author Leonardo Klein
 */

#ifndef SERIAL_INPUT_MONITOR_H
#define SERIAL_INPUT_MONITOR_H

#include <Arduino.h>

/**
 * @brief Supported device types
 */
enum class Device : uint8_t {
    MOUSE    = 0, ///< Mouse device
    KEYBOARD = 1  ///< Keyboard device
};

/**
 * @brief Mouse events
 */
enum class MouseEvent : uint8_t {
    RIGHT_PRESS    = 0, ///< Press right button
    RIGHT_RELEASE  = 1, ///< Release right button
    LEFT_PRESS     = 2, ///< Press left button
    LEFT_RELEASE   = 3, ///< Release left button
    MIDDLE_PRESS   = 4, ///< Press middle button
    MIDDLE_RELEASE = 5, ///< Release middle button
    SCROLL         = 6, ///< Scroll wheel
    POSITION       = 7, ///< Set absolute position
    MOVE           = 8  ///< Move relatively
};

/**
 * @brief Keyboard events
 */
enum class KeyboardEvent : uint8_t {
    PRESS   = 1, ///< Press key
    RELEASE = 0  ///< Release key
};

/**
 * @brief Key codes based on Windows Virtual Key Codes standard
 *
 * This enumeration contains standardized hexadecimal codes for keys,
 * compatible with Windows system and widely used in embedded systems.
 */
enum class VirtualKey : uint16_t {
    // Basic control keys
    BACKSPACE = 0x08, ///< BACKSPACE key
    TAB       = 0x09, ///< TAB key
    CLEAR     = 0x0C, ///< CLEAR key
    ENTER     = 0x0D, ///< ENTER key

    // Modifier keys
    SHIFT     = 0x10, ///< SHIFT key (generic)
    CONTROL   = 0x11, ///< CTRL key (generic)
    ALT       = 0x12, ///< ALT key (generic)
    PAUSE     = 0x13, ///< PAUSE key
    CAPS_LOCK = 0x14, ///< CAPS LOCK key

    // IME keys
    KANA    = 0x15, ///< Kana IME mode
    HANGEUL = 0x15, ///< Hangeul IME mode (alias)
    HANGUL  = 0x15, ///< Hangul IME mode (alias)
    IME_ON  = 0x16, ///< IME enabled
    JUNJA   = 0x17, ///< Junja IME mode
    FINAL   = 0x18, ///< Final IME mode
    HANJA   = 0x19, ///< Hanja IME mode
    KANJI   = 0x19, ///< Kanji IME mode (alias)
    IME_OFF = 0x1A, ///< IME disabled

    // Navigation keys
    ESCAPE     = 0x1B, ///< ESC key
    CONVERT    = 0x1C, ///< IME conversion
    NONCONVERT = 0x1D, ///< IME non-conversion
    ACCEPT     = 0x1E, ///< IME accept
    MODECHANGE = 0x1F, ///< IME mode change

    // Special keys
    SPACE     = 0x20, ///< Space bar
    PAGE_UP   = 0x21, ///< PAGE UP key
    PAGE_DOWN = 0x22, ///< PAGE DOWN key
    END       = 0x23, ///< END key
    HOME      = 0x24, ///< HOME key

    // Arrow keys
    ARROW_LEFT  = 0x25, ///< Left arrow
    ARROW_UP    = 0x26, ///< Up arrow
    ARROW_RIGHT = 0x27, ///< Right arrow
    ARROW_DOWN  = 0x28, ///< Down arrow

    // Special function keys
    SELECT       = 0x29, ///< SELECT key
    PRINT        = 0x2A, ///< PRINT key
    EXECUTE      = 0x2B, ///< EXECUTE key
    PRINT_SCREEN = 0x2C, ///< PRINT SCREEN key
    INSERT       = 0x2D, ///< INSERT key
    DELETE       = 0x2E, ///< DELETE key
    HELP         = 0x2F, ///< HELP key

    // Numbers (0-9)
    NUM_0 = 0x30, NUM_1 = 0x31, NUM_2 = 0x32, NUM_3 = 0x33, NUM_4 = 0x34,
    NUM_5 = 0x35, NUM_6 = 0x36, NUM_7 = 0x37, NUM_8 = 0x38, NUM_9 = 0x39,

    // Letters (A-Z)
    A = 0x41, B = 0x42, C = 0x43, D = 0x44, E = 0x45, F = 0x46,
    G = 0x47, H = 0x48, I = 0x49, J = 0x4A, K = 0x4B, L = 0x4C,
    M = 0x4D, N = 0x4E, O = 0x4F, P = 0x50, Q = 0x51, R = 0x52,
    S = 0x53, T = 0x54, U = 0x55, V = 0x56, W = 0x57, X = 0x58,
    Y = 0x59, Z = 0x5A,

    // Windows keys
    LEFT_WIN  = 0x5B, ///< Left Windows key
    RIGHT_WIN = 0x5C, ///< Right Windows key
    APPS      = 0x5D, ///< Applications key

    // Special key
    SLEEP = 0x5F, ///< Computer sleep key

    // Numeric keypad
    NUMPAD_0 = 0x60, NUMPAD_1 = 0x61, NUMPAD_2 = 0x62, NUMPAD_3 = 0x63, NUMPAD_4 = 0x64,
    NUMPAD_5 = 0x65, NUMPAD_6 = 0x66, NUMPAD_7 = 0x67, NUMPAD_8 = 0x68, NUMPAD_9 = 0x69,

    MULTIPLY  = 0x6A, ///< * (multiply)
    ADD       = 0x6B, ///< + (add)
    SEPARATOR = 0x6C, ///< Separator
    SUBTRACT  = 0x6D, ///< - (subtract)
    DECIMAL   = 0x6E, ///< . (decimal)
    DIVIDE    = 0x6F, ///< / (divide)

    // Function keys (F1-F24)
    F1 = 0x70, F2 = 0x71, F3 = 0x72, F4 = 0x73, F5 = 0x74, F6 = 0x75,
    F7 = 0x76, F8 = 0x77, F9 = 0x78, F10 = 0x79, F11 = 0x7A, F12 = 0x7B,
    F13 = 0x7C, F14 = 0x7D, F15 = 0x7E, F16 = 0x7F, F17 = 0x80, F18 = 0x81,
    F19 = 0x82, F20 = 0x83, F21 = 0x84, F22 = 0x85, F23 = 0x86, F24 = 0x87,

    // Lock keys
    NUM_LOCK    = 0x90, ///< NUM LOCK
    SCROLL_LOCK = 0x91, ///< SCROLL LOCK

    // Specific modifiers
    LEFT_SHIFT    = 0xA0, ///< Left SHIFT
    RIGHT_SHIFT   = 0xA1, ///< Right SHIFT
    LEFT_CONTROL  = 0xA2, ///< Left CTRL
    RIGHT_CONTROL = 0xA3, ///< Right CTRL
    LEFT_ALT      = 0xA4, ///< Left ALT
    RIGHT_ALT     = 0xA5, ///< Right ALT

    // Browser keys
    BROWSER_BACK      = 0xA6, ///< Browser back
    BROWSER_FORWARD   = 0xA7, ///< Browser forward
    BROWSER_REFRESH   = 0xA8, ///< Browser refresh
    BROWSER_STOP      = 0xA9, ///< Browser stop
    BROWSER_SEARCH    = 0xAA, ///< Browser search
    BROWSER_FAVORITES = 0xAB, ///< Browser favorites
    BROWSER_HOME      = 0xAC, ///< Browser home

    // Volume controls
    VOLUME_MUTE = 0xAD, ///< Mute
    VOLUME_DOWN = 0xAE, ///< Volume down
    VOLUME_UP   = 0xAF, ///< Volume up

    // Media controls
    MEDIA_NEXT_TRACK = 0xB0, ///< Next track
    MEDIA_PREV_TRACK = 0xB1, ///< Previous track
    MEDIA_STOP       = 0xB2, ///< Stop media
    MEDIA_PLAY_PAUSE = 0xB3, ///< Play/Pause

    // Launch keys
    LAUNCH_MAIL         = 0xB4, ///< Launch mail
    LAUNCH_MEDIA_SELECT = 0xB5, ///< Media selector
    LAUNCH_APP1         = 0xB6, ///< Application 1
    LAUNCH_APP2         = 0xB7, ///< Application 2

    // OEM keys (keyboard specific)
    OEM_1      = 0xBA, ///< Misc characters (;: in US)
    OEM_PLUS   = 0xBB, ///< + key for any country
    OEM_COMMA  = 0xBC, ///< , key for any country
    OEM_MINUS  = 0xBD, ///< - key for any country
    OEM_PERIOD = 0xBE, ///< . key for any country
    OEM_2      = 0xBF, ///< Misc characters (/? in US)
    OEM_3      = 0xC0, ///< Misc characters (`~ in US)

    OEM_4 = 0xDB, ///< Misc characters ([{ in US)
    OEM_5 = 0xDC, ///< Misc characters (\\| in US)
    OEM_6 = 0xDD, ///< Misc characters (]} in US)
    OEM_7 = 0xDE, ///< Misc characters ('" in US)
    OEM_8 = 0xDF, ///< Misc characters

    // Advanced special keys
    OEM_102     = 0xE2, ///< <> or \\| key on RT 102
    PROCESS_KEY = 0xE5, ///< IME process key
    PACKET      = 0xE7, ///< Direct Unicode sending

    // Final control keys
    ATTN      = 0xF6, ///< ATTN key
    CRSEL     = 0xF7, ///< CrSel key
    EXSEL     = 0xF8, ///< ExSel key
    EREOF     = 0xF9, ///< EOF erase key
    PLAY      = 0xFA, ///< PLAY key
    ZOOM      = 0xFB, ///< ZOOM key
    PA1       = 0xFD, ///< PA1 key
    OEM_CLEAR = 0xFE  ///< CLEAR key
};

/**
 * @brief Main class for input monitoring and control via serial
 *
 * This class encapsulates all functionality needed to send
 * input commands through serial port, following a
 * structured and documented protocol.
 */
class SerialInputMonitor {
  private:
    // Mouse button states
    bool m_leftButtonPressed;   ///< Left mouse button state
    bool m_rightButtonPressed;  ///< Right mouse button state
    bool m_middleButtonPressed; ///< Middle mouse button state

    /**
     * @brief Send a character string as key sequence
     * @param newLine If true, adds ENTER at the end
     * @param text Text to be sent
     */
    void sendKeySequence(bool newLine, const char *text);

    /**
     * @brief Send formatted command via serial port
     * @param device Device type
     * @param event Event code
     * @param param1 First parameter (optional)
     * @param param2 Second parameter (optional)
     */
    void sendCommand(Device device, uint8_t event, int param1 = 0, int param2 = 0);

  public:
    /**
     * @brief Class constructor
     * Initialize mouse button states
     */
    SerialInputMonitor();

    // ==================== MOUSE CONTROLS ====================

    /**
     * @brief Set absolute mouse position
     * @param x X coordinate in pixels
     * @param y Y coordinate in pixels
     */
    void setMousePosition(int x, int y);

    /**
     * @brief Move mouse relative to current position
     * @param deltaX X displacement (can be negative)
     * @param deltaY Y displacement (can be negative)
     */
    void moveMouseRelative(int deltaX, int deltaY);

    /**
     * @brief Press right mouse button
     */
    void pressRightButton();

    /**
     * @brief Release right mouse button
     */
    void releaseRightButton();

    /**
     * @brief Press left mouse button
     */
    void pressLeftButton();

    /**
     * @brief Release left mouse button
     */
    void releaseLeftButton();

    /**
     * @brief Press middle mouse button
     */
    void pressMiddleButton();

    /**
     * @brief Release middle mouse button
     */
    void releaseMiddleButton();

    /**
     * @brief Perform single click with left button
     */
    void clickLeft();

    /**
     * @brief Perform single click with right button
     */
    void clickRight();

    /**
     * @brief Perform double click with left button
     */
    void doubleClickLeft();

    /**
     * @brief Scroll mouse wheel
     * @param scrollAmount Scroll amount (positive=up, negative=down)
     */
    void scrollMouse(int scrollAmount);

    // ==================== STATE QUERY ====================

    /**
     * @brief Check if left button is pressed
     * @return true if pressed, false otherwise
     */
    inline bool isLeftButtonPressed() const {
        return m_leftButtonPressed;
    }

    /**
     * @brief Check if right button is pressed
     * @return true if pressed, false otherwise
     */
    inline bool isRightButtonPressed() const {
        return m_rightButtonPressed;
    }

    /**
     * @brief Check if middle button is pressed
     * @return true if pressed, false otherwise
     */
    inline bool isMiddleButtonPressed() const {
        return m_middleButtonPressed;
    }

    // ==================== KEYBOARD CONTROLS ====================

    /**
     * @brief Press a key using virtual code
     * @param key Virtual key code
     */
    void pressKey(VirtualKey key);

    /**
     * @brief Release a key using virtual code
     * @param key Virtual key code
     */
    void releaseKey(VirtualKey key);

    /**
     * @brief Perform press and release of a key
     * @param key Virtual key code
     */
    void tapKey(VirtualKey key);

    /**
     * @brief Press a key using ASCII character
     * @param character Character to be pressed
     */
    void pressKey(char character);

    /**
     * @brief Release a key using ASCII character
     * @param character Character to be released
     */
    void releaseKey(char character);

    /**
     * @brief Perform press and release of a character
     * @param character Character to be typed
     */
    void typeCharacter(char character);

    // ==================== TEXT FUNCTIONS ====================

    /**
     * @brief Type a text string with line break
     * @param text Text to be typed
     */
    void typeTextLine(const char *text);

    /**
     * @brief Type a text string without line break
     * @param text Text to be typed
     */
    void typeText(const char *text);

    // ==================== KEY COMBINATIONS ====================

    /**
     * @brief Execute Ctrl+C combination (copy)
     */
    void copy();

    /**
     * @brief Execute Ctrl+V combination (paste)
     */
    void paste();

    /**
     * @brief Execute Ctrl+X combination (cut)
     */
    void cut();

    /**
     * @brief Execute Ctrl+Z combination (undo)
     */
    void undo();

    /**
     * @brief Execute Ctrl+Y combination (redo)
     */
    void redo();

    /**
     * @brief Execute Ctrl+A combination (select all)
     */
    void selectAll();

    /**
     * @brief Execute Alt+Tab combination (switch window)
     */
    void altTab();

    /**
     * @brief Execute Alt+F4 combination (close window)
     */
    void altF4();

    // ==================== UTILITY FUNCTIONS ====================

    /**
     * @brief Convert ASCII character to virtual key code
     * @param character ASCII character
     * @return Corresponding virtual key code
     */
    static VirtualKey charToVirtualKey(char character);

    /**
     * @brief Check if a character requires Shift to be typed
     * @param character Character to check
     * @return true if requires Shift, false otherwise
     */
    static bool requiresShift(char character);

    /**
     * @brief Add delay between commands (useful to avoid timing issues)
     * @param milliseconds Time in milliseconds
     */
    void delay(unsigned long milliseconds);
};

#endif // SERIAL_INPUT_MONITOR_H
