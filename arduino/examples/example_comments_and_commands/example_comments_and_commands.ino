/**
 * @file example_comments_and_commands.ino
 * @brief Example with comments and two-way communication
 * @author Leonardo Klein
 * @date 2025-09-05
 * 
 * Demonstrates when SerialInputMonitor library would be needed.
 * Shows the difference between sending data (no library) and receiving commands (library helpful).
 * 
 * Features:
 * - Comment system demonstration
 * - Basic command reception
 * - LED control via serial commands
 * 
 * Commands: LED_ON, LED_OFF, STATUS
 * No SerialInputMonitor library required for this basic example.
 */

void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  
  Serial.println("# Arduino started - LED control example");
  Serial.println("# Send commands: LED_ON, LED_OFF, STATUS");
  Serial.println("# This example shows when you need SerialInputMonitor library");
}

void loop() {
  Serial.println("# Sensor reading every 2 seconds");
  Serial.println("1000");
  
  if (Serial.available()) {
    String command = Serial.readString();
    command.trim();
    
    Serial.print("# Received command: ");
    Serial.println(command);
    
    if (command == "LED_ON") {
      digitalWrite(LED_BUILTIN, HIGH);
      Serial.println("# LED turned ON");
    }
    else if (command == "LED_OFF") {
      digitalWrite(LED_BUILTIN, LOW);
      Serial.println("# LED turned OFF");
    }
    else if (command == "STATUS") {
      Serial.println("# LED status check");
      if (digitalRead(LED_BUILTIN)) {
        Serial.println("# LED is currently ON");
      } else {
        Serial.println("# LED is currently OFF");
      }
    }
    else {
      Serial.print("# Unknown command: ");
      Serial.println(command);
    }
  }
  
  delay(2000);
}
