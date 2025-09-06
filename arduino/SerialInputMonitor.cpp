/**
 * @file SerialInputMonitor.cpp
 * @brief Implementation of input monitoring and control library via serial
 * @version 1.0.0
 * @date 2025-09-05
 * 
 * @author Leonardo Klein
 */

#include "SerialInputMonitor.h"

SerialInputMonitor::SerialInputMonitor() 
    : m_leftButtonPressed(false)
    , m_rightButtonPressed(false)
    , m_middleButtonPressed(false) {
}

void SerialInputMonitor::sendCommand(Device device, uint8_t event, int param1, int param2) {
    Serial.print(static_cast<uint8_t>(device));
    Serial.print(" ");
    Serial.print(event);
    
    if (param1 != 0 || param2 != 0) {
        Serial.print(" ");
        Serial.print(param1);
        
        if (param2 != 0) {
            Serial.print(" ");
            Serial.print(param2);
        }
    }
    
    Serial.println();
}

void SerialInputMonitor::sendKeySequence(bool newLine, const char* text) {
    if (!text) return;
    
    size_t length = strlen(text);
    
    for (size_t i = 0; i < length; i++) {
        typeCharacter(text[i]);
        delay(10);
    }
    
    if (newLine) {
        tapKey(VirtualKey::ENTER);
    }
}

void SerialInputMonitor::setMousePosition(int x, int y) {
    sendCommand(Device::MOUSE, static_cast<uint8_t>(MouseEvent::POSITION), x, y);
}

void SerialInputMonitor::moveMouseRelative(int deltaX, int deltaY) {
    sendCommand(Device::MOUSE, static_cast<uint8_t>(MouseEvent::MOVE), deltaX, deltaY);
}

void SerialInputMonitor::pressRightButton() {
    if (!m_rightButtonPressed) {
        sendCommand(Device::MOUSE, static_cast<uint8_t>(MouseEvent::RIGHT_PRESS));
        m_rightButtonPressed = true;
    }
}

void SerialInputMonitor::releaseRightButton() {
    if (m_rightButtonPressed) {
        sendCommand(Device::MOUSE, static_cast<uint8_t>(MouseEvent::RIGHT_RELEASE));
        m_rightButtonPressed = false;
    }
}

void SerialInputMonitor::pressLeftButton() {
    if (!m_leftButtonPressed) {
        sendCommand(Device::MOUSE, static_cast<uint8_t>(MouseEvent::LEFT_PRESS));
        m_leftButtonPressed = true;
    }
}

void SerialInputMonitor::releaseLeftButton() {
    if (m_leftButtonPressed) {
        sendCommand(Device::MOUSE, static_cast<uint8_t>(MouseEvent::LEFT_RELEASE));
        m_leftButtonPressed = false;
    }
}

void SerialInputMonitor::pressMiddleButton() {
    if (!m_middleButtonPressed) {
        sendCommand(Device::MOUSE, static_cast<uint8_t>(MouseEvent::MIDDLE_PRESS));
        m_middleButtonPressed = true;
    }
}

void SerialInputMonitor::releaseMiddleButton() {
    if (m_middleButtonPressed) {
        sendCommand(Device::MOUSE, static_cast<uint8_t>(MouseEvent::MIDDLE_RELEASE));
        m_middleButtonPressed = false;
    }
}

void SerialInputMonitor::clickLeft() {
    pressLeftButton();
    delay(50);
    releaseLeftButton();
}

void SerialInputMonitor::clickRight() {
    pressRightButton();
    delay(50);
    releaseRightButton();
}

void SerialInputMonitor::doubleClickLeft() {
    clickLeft();
    delay(100);
    clickLeft();
}

void SerialInputMonitor::scrollMouse(int scrollAmount) {
    sendCommand(Device::MOUSE, static_cast<uint8_t>(MouseEvent::SCROLL), scrollAmount);
}

void SerialInputMonitor::pressKey(VirtualKey key) {
    sendCommand(Device::KEYBOARD, static_cast<uint8_t>(KeyboardEvent::PRESS), 
                static_cast<uint16_t>(key));
}

void SerialInputMonitor::releaseKey(VirtualKey key) {
    sendCommand(Device::KEYBOARD, static_cast<uint8_t>(KeyboardEvent::RELEASE), 
                static_cast<uint16_t>(key));
}

void SerialInputMonitor::tapKey(VirtualKey key) {
    pressKey(key);
    delay(50);
    releaseKey(key);
}

void SerialInputMonitor::pressKey(char character) {
    VirtualKey key = charToVirtualKey(character);
    
    if (requiresShift(character)) {
        pressKey(VirtualKey::LEFT_SHIFT);
        delay(10);
        pressKey(key);
    } else {
        pressKey(key);
    }
}

void SerialInputMonitor::releaseKey(char character) {
    VirtualKey key = charToVirtualKey(character);
    
    if (requiresShift(character)) {
        releaseKey(key);
        delay(10);
        releaseKey(VirtualKey::LEFT_SHIFT);
    } else {
        releaseKey(key);
    }
}

void SerialInputMonitor::typeCharacter(char character) {
    pressKey(character);
    delay(50);
    releaseKey(character);
}

void SerialInputMonitor::typeTextLine(const char* text) {
    sendKeySequence(true, text);
}

void SerialInputMonitor::typeText(const char* text) {
    sendKeySequence(false, text);
}

void SerialInputMonitor::copy() {
    pressKey(VirtualKey::LEFT_CONTROL);
    delay(10);
    tapKey(VirtualKey::C);
    delay(10);
    releaseKey(VirtualKey::LEFT_CONTROL);
}

void SerialInputMonitor::paste() {
    pressKey(VirtualKey::LEFT_CONTROL);
    delay(10);
    tapKey(VirtualKey::V);
    delay(10);
    releaseKey(VirtualKey::LEFT_CONTROL);
}

void SerialInputMonitor::cut() {
    pressKey(VirtualKey::LEFT_CONTROL);
    delay(10);
    tapKey(VirtualKey::X);
    delay(10);
    releaseKey(VirtualKey::LEFT_CONTROL);
}

void SerialInputMonitor::undo() {
    pressKey(VirtualKey::LEFT_CONTROL);
    delay(10);
    tapKey(VirtualKey::Z);
    delay(10);
    releaseKey(VirtualKey::LEFT_CONTROL);
}

void SerialInputMonitor::redo() {
    pressKey(VirtualKey::LEFT_CONTROL);
    delay(10);
    tapKey(VirtualKey::Y);
    delay(10);
    releaseKey(VirtualKey::LEFT_CONTROL);
}

void SerialInputMonitor::selectAll() {
    pressKey(VirtualKey::LEFT_CONTROL);
    delay(10);
    tapKey(VirtualKey::A);
    delay(10);
    releaseKey(VirtualKey::LEFT_CONTROL);
}

void SerialInputMonitor::altTab() {
    pressKey(VirtualKey::LEFT_ALT);
    delay(10);
    tapKey(VirtualKey::TAB);
    delay(10);
    releaseKey(VirtualKey::LEFT_ALT);
}

void SerialInputMonitor::altF4() {
    pressKey(VirtualKey::LEFT_ALT);
    delay(10);
    tapKey(VirtualKey::F4);
    delay(10);
    releaseKey(VirtualKey::LEFT_ALT);
}

VirtualKey SerialInputMonitor::charToVirtualKey(char character) {
    // Numbers 0-9
    if (character >= '0' && character <= '9') {
        return static_cast<VirtualKey>(VirtualKey::NUM_0 + (character - '0'));
    }
    
    // Lowercase letters a-z
    if (character >= 'a' && character <= 'z') {
        return static_cast<VirtualKey>(VirtualKey::A + (character - 'a'));
    }
    
    // Uppercase letters A-Z
    if (character >= 'A' && character <= 'Z') {
        return static_cast<VirtualKey>(VirtualKey::A + (character - 'A'));
    }
    
    // Common special characters
    switch (character) {
        case ' ': return VirtualKey::SPACE;
        case '\t': return VirtualKey::TAB;
        case '\r':
        case '\n': return VirtualKey::ENTER;
        case '\b': return VirtualKey::BACKSPACE;
        
        // Punctuation that doesn't require Shift
        case ',': return VirtualKey::OEM_COMMA;
        case '.': return VirtualKey::OEM_PERIOD;
        case '/': return VirtualKey::OEM_2;
        case ';': return VirtualKey::OEM_1;
        case '\'': return VirtualKey::OEM_7;
        case '[': return VirtualKey::OEM_4;
        case ']': return VirtualKey::OEM_6;
        case '\\': return VirtualKey::OEM_5;
        case '`': return VirtualKey::OEM_3;
        case '-': return VirtualKey::OEM_MINUS;
        case '=': return VirtualKey::OEM_PLUS;
        
        case '!': return VirtualKey::NUM_1;
        case '@': return VirtualKey::NUM_2;
        case '#': return VirtualKey::NUM_3;
        case '$': return VirtualKey::NUM_4;
        case '%': return VirtualKey::NUM_5;
        case '^': return VirtualKey::NUM_6;
        case '&': return VirtualKey::NUM_7;
        case '*': return VirtualKey::NUM_8;
        case '(': return VirtualKey::NUM_9;
        case ')': return VirtualKey::NUM_0;
        case '_': return VirtualKey::OEM_MINUS;
        case '+': return VirtualKey::OEM_PLUS;
        case '{': return VirtualKey::OEM_4;
        case '}': return VirtualKey::OEM_6;
        case '|': return VirtualKey::OEM_5;
        case ':': return VirtualKey::OEM_1;
        case '"': return VirtualKey::OEM_7;
        case '<': return VirtualKey::OEM_COMMA;
        case '>': return VirtualKey::OEM_PERIOD;
        case '?': return VirtualKey::OEM_2;
        case '~': return VirtualKey::OEM_3;
        
        default:
            return VirtualKey::SPACE;
    }
}

bool SerialInputMonitor::requiresShift(char character) {
    if (character >= 'A' && character <= 'Z') {
        return true;
    }
    
    switch (character) {
        case '!': case '@': case '#': case '$': case '%':
        case '^': case '&': case '*': case '(': case ')':
        case '_': case '+': case '{': case '}': case '|':
        case ':': case '"': case '<': case '>': case '?':
        case '~':
            return true;
        default:
            return false;
    }
}

void SerialInputMonitor::delay(unsigned long milliseconds) {
    ::delay(milliseconds);
}
