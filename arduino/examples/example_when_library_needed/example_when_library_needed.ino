/**
 * @file example_when_library_needed.ino
 * @brief Example showing WHEN you need SerialInputMonitor library
 * @author Leonardo Klein
 * @date 2025-09-05
 * 
 * WITHOUT SerialInputMonitor:
 * - You manually parse Serial.readString()
 * - Limited command processing
 * - Basic string matching only
 * 
 * WITH SerialInputMonitor:
 * - Structured protocol handling
 * - Mouse/keyboard event simulation
 * - Complex parameter parsing
 * - Error handling and validation
 * 
 * This example only SENDS data (library not needed).
 * No SerialInputMonitor library required.
 */

void setup() {
  Serial.begin(9600);
  
  Serial.println("# ===========================================");
  Serial.println("# SerialInputMonitor Library Usage Example");
  Serial.println("# ===========================================");
  Serial.println("# ");
  Serial.println("# Current: Basic Arduino example (no library needed)");
  Serial.println("# Use library when you need:");
  Serial.println("# - Receive complex commands from PC");
  Serial.println("# - Control servos, motors, LEDs via PC commands");
  Serial.println("# - Implement structured communication protocol");
  Serial.println("# ");
  Serial.println("# This example only SENDS data (library not needed)");
  Serial.println("# ");
}

void loop() {
  static int counter = 0;
  
  Serial.println("# ---- Simulation cycle starting ----");
  
  Serial.print("0 1 ");
  Serial.print(random(-10, 11));
  Serial.print(" ");
  Serial.println(random(-10, 11));
  Serial.println("# Mouse movement sent to PC");
  
  delay(500);
  
  Serial.print("1 1 0x");
  Serial.println(random(65, 91), HEX);
  Serial.println("# Keyboard key press sent to PC");
  
  delay(500);
  
  Serial.println(random(100, 1000));
  Serial.println("# Sensor value (standalone numeric)");
  
  delay(1000);
  
  counter++;
  Serial.print("# Cycle ");
  Serial.print(counter);
  Serial.println(" completed");
  Serial.println("# ");
  
  delay(2000);
}
