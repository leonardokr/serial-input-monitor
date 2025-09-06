/**
 * @file example_basic_usage.ino
 * @brief Basic usage example for SerialInputMonitor library
 * @author Leonardo Klein
 * @date 2025-09-05
 *
 * This example demonstrates basic usage of the library for controlling
 * mouse and keyboard via serial communication.
 *
 * Arduino Uno connections:
 * - Pin 2: Button for mouse click test
 * - Pin 3: Button for typing test
 * - Pin 13: Indicator LED (built-in)
 * - GND: Button ground
 * 
 * SerialInputMonitor library REQUIRED for this example.
 */

#include "SerialInputMonitor.h"

// Pin configuration
const int BUTTON_MOUSE_PIN    = 2;
const int BUTTON_KEYBOARD_PIN = 3;
const int LED_PIN             = 13;

const unsigned long DEBOUNCE_DELAY = 50;

bool lastButtonMouseState            = HIGH;
bool lastButtonKeyboardState         = HIGH;
unsigned long lastButtonMouseTime    = 0;
unsigned long lastButtonKeyboardTime = 0;

SerialInputMonitor controller;

// ==================== SETUP ====================

void setup() {
    Serial.begin(9600);

    pinMode(BUTTON_MOUSE_PIN, INPUT_PULLUP);
    pinMode(BUTTON_KEYBOARD_PIN, INPUT_PULLUP);
    pinMode(LED_PIN, OUTPUT);

    for(int i = 0; i < 3; i++) {
        digitalWrite(LED_PIN, HIGH);
        delay(200);
        digitalWrite(LED_PIN, LOW);
        delay(200);
    }

    Serial.println("Arduino Serial Input Monitor v2.0");
    Serial.println("System initialized and ready");
    Serial.println("Protocol: DEVICE EVENT [PARAMS]");
    Serial.println("Device: 0=Mouse, 1=Keyboard");
    Serial.println("==========================================");
}

// ==================== MAIN LOOP ====================

void loop() {
    handleButtonPress();
    delay(10);
}

// ==================== CONTROL FUNCTIONS ====================

/**
 * @brief Handles button press with debounce
 */
void handleButtonPress() {
    unsigned long currentTime = millis();

    bool currentMouseState = digitalRead(BUTTON_MOUSE_PIN);
    if(currentMouseState != lastButtonMouseState && (currentTime - lastButtonMouseTime) > DEBOUNCE_DELAY) {

        if(currentMouseState == LOW) {
            demonstrateMouseControls();
            digitalWrite(LED_PIN, HIGH);
        } else {
            digitalWrite(LED_PIN, LOW);
        }

        lastButtonMouseState = currentMouseState;
        lastButtonMouseTime  = currentTime;
    }

    bool currentKeyboardState = digitalRead(BUTTON_KEYBOARD_PIN);
    if(currentKeyboardState != lastButtonKeyboardState && (currentTime - lastButtonKeyboardTime) > DEBOUNCE_DELAY) {

        if(currentKeyboardState == LOW) {
            demonstrateKeyboardControls();
            digitalWrite(LED_PIN, HIGH);
        } else {
            digitalWrite(LED_PIN, LOW);
        }

        lastButtonKeyboardState = currentKeyboardState;
        lastButtonKeyboardTime  = currentTime;
    }
}

/**
 * @brief Demonstrates mouse controls
 */
void demonstrateMouseControls() {
    Serial.println("Demo: Mouse Controls");

    controller.setMousePosition(500, 300);
    delay(500);

    controller.clickLeft();
    delay(500);

    controller.moveMouseRelative(100, 50);
    delay(500);

    controller.doubleClickLeft();
    delay(500);

    controller.clickRight();
    delay(500);

    controller.scrollMouse(3);
    delay(300);

    controller.scrollMouse(-3);

    Serial.println("Mouse demo completed");
}

/**
 * @brief Demonstrates keyboard controls
 */
void demonstrateKeyboardControls() {
    Serial.println("Demo: Keyboard Controls");

    controller.typeText("Hello from Arduino! ");
    delay(1000);

    controller.typeText("12345 ");
    delay(1000);

    controller.tapKey(VirtualKey::ENTER);
    delay(500);

    controller.typeText("UPPERCASE TEXT");
    delay(1000);

    controller.selectAll();
    delay(500);

    controller.copy();
    delay(500);

    controller.tapKey(VirtualKey::END);
    delay(500);

    controller.paste();

    Serial.println("Keyboard demo completed");
}

// ==================== UTILITY FUNCTIONS ====================

/**
 * @brief Blinks indicator LED
 * @param times Number of blinks
 * @param delayMs Delay between blinks
 */
void blinkLED(int times, int delayMs) {
    for(int i = 0; i < times; i++) {
        digitalWrite(LED_PIN, HIGH);
        delay(delayMs);
        digitalWrite(LED_PIN, LOW);
        delay(delayMs);
    }
}

/**
 * @brief Sends status message via serial
 * @param message Message to send
 */
void sendStatus(const char *message) {
    Serial.print("STATUS: ");
    Serial.println(message);
}
