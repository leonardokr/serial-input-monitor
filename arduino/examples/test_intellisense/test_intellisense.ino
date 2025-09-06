/**
 * @file test_intellisense.ino
 * @brief Test file to verify Arduino.h and SerialInputMonitor.h includes are working
 * @author Leonardo Klein
 * @date 2025-09-05
 * 
 * This file tests if IntelliSense is properly configured for Arduino development.
 * If no errors appear, the include paths are correctly set up.
 * 
 * Features:
 * - Arduino.h function testing
 * - SerialInputMonitor.h include verification
 * - Basic LED control
 * 
 * Used for VS Code IntelliSense validation.
 */

#include <Arduino.h>
#include "SerialInputMonitor.h"

void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  
  digitalWrite(LED_BUILTIN, HIGH);
  delay(1000);
  digitalWrite(LED_BUILTIN, LOW);
}

void loop() {
  Serial.println("# IntelliSense test - if no errors, includes are working!");
  delay(2000);
}
