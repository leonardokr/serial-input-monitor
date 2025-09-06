/**
 * @file example_using_library.ino
 * @brief Example using SerialInputMonitor library for complex operations
 * @author Leonardo Klein
 * @date 2025-09-05
 * 
 * This shows when you NEED the library vs simple Serial.println().
 * Demonstrates complex command processing with parameters and validation.
 * 
 * Features:
 * - Library-based command parsing
 * - Complex protocol handling
 * - Parameter validation
 * - Error handling
 * 
 * Commands: LED_ON, LED_OFF, BLINK_5
 * SerialInputMonitor library REQUIRED for this example.
 */

#include "SerialInputMonitor.h"

SerialInputMonitor monitor;

void setup() {
  Serial.begin(9600);
  
  monitor.begin();
  
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(2, OUTPUT);
  
  Serial.println("# SerialInputMonitor Library Example");
  Serial.println("# This Arduino can now RECEIVE commands from PC");
  Serial.println("# Try sending: LED_ON, LED_OFF, BLINK_5");
  Serial.println("# ");
}

void loop() {
  Serial.println("# Heartbeat from Arduino");
  Serial.println("500");
  
  monitor.processIncomingData();
  
  delay(1000);
}
