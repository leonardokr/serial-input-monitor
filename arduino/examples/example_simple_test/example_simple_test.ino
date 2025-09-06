/**
 * @file example_simple_test.ino
 * @brief Simple test with basic mouse and keyboard commands
 * @author Leonardo Klein
 * @date 2025-09-05
 * 
 * This example sends basic mouse and keyboard commands automatically to test the system.
 * Very useful to check if serial communication and baud rate detection are working.
 * 
 * Features:
 * - Mouse position cycling
 * - Arrow key testing
 * - Automatic timing control
 * 
 * No SerialInputMonitor library required.
 */

const unsigned long INTERVAL = 1000;
unsigned long lastActionTime = 0;
int actionCounter = 0;

const int TEST_POSITIONS[][2] = {
  {500, 300},
  {800, 300},
  {800, 600},
  {500, 600}
};

void setup() {
  Serial.begin(9600);
  
  delay(1000);
  
  Serial.println("# Simple Auto Test Starting");
  Serial.println("# Testing mouse movement and arrow key");
}

void loop() {
  unsigned long currentTime = millis();
  
  if (currentTime - lastActionTime >= INTERVAL) {
    
    switch (actionCounter % 8) {
      case 0:
      case 2:
      case 4:
      case 6:
        moveMouseToPosition((actionCounter / 2) % 4);
        break;
        
      case 1:
      case 3:
      case 5:
      case 7:
        pressUpArrow();
        break;
    }
    
    actionCounter++;
    lastActionTime = currentTime;
  }
}

void moveMouseToPosition(int index) {
  int x = TEST_POSITIONS[index][0];
  int y = TEST_POSITIONS[index][1];
  
  Serial.print("0 7 ");
  Serial.print(x);
  Serial.print(" ");
  Serial.println(y);
}

void pressUpArrow() {
  Serial.println("1 1 26");
  delay(50);
  Serial.println("1 0 26");
}
