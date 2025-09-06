/**
 * @file example_minimal.ino
 * @brief Minimal test for serial communication and baud rate detection
 * @author Leonardo Klein
 * @date 2025-09-05
 * 
 * This example sends only basic commands to test automatic baud rate detection.
 * Ideal for checking if serial connection is working without complex operations.
 * 
 * Commands sent:
 * - Mouse position setting
 * - Basic key press/release
 * 
 * No SerialInputMonitor library required.
 */

void setup() {
  Serial.begin(9600);
  
  delay(500);
  Serial.println("# Minimal Test Ready");
}

void loop() {
  Serial.println("0 7 640 360");
  delay(1000);
  
  Serial.println("1 1 26");
  delay(100);
  Serial.println("1 0 26");
  delay(1000);
  
  Serial.println("0 7 800 500");
  delay(1000);
  
  Serial.println("1 1 51");
  delay(100);
  Serial.println("1 0 51");
  delay(2000);
}
