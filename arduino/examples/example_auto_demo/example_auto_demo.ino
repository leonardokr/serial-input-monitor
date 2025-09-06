/**
 * @file example_auto_demo.ino
 * @brief Auto demo with mouse square movement and keyboard presses
 * @author Leonardo Klein
 * @date 2025-09-05
 * 
 * This example moves the mouse in a square in the center of the screen
 * and presses the up arrow key at each movement, with 500ms delay.
 * 
 * Features:
 * - Automated square mouse movement
 * - Arrow key press/release sequences
 * - Timing control with millis()
 * 
 * Serial output format:
 * - Mouse: "0 7 X Y" (cursor position)
 * - Keyboard: "1 1 26" (key pressed - up arrow)
 * - Keyboard: "1 0 26" (key released - up arrow)
 * 
 * No SerialInputMonitor library required.
 */

const int SCREEN_CENTER_X = 960;
const int SCREEN_CENTER_Y = 540;
const int SQUARE_SIZE = 200;

const int SQUARE_POSITIONS[][2] = {
  {SCREEN_CENTER_X - SQUARE_SIZE/2, SCREEN_CENTER_Y - SQUARE_SIZE/2},
  {SCREEN_CENTER_X + SQUARE_SIZE/2, SCREEN_CENTER_Y - SQUARE_SIZE/2},
  {SCREEN_CENTER_X + SQUARE_SIZE/2, SCREEN_CENTER_Y + SQUARE_SIZE/2},
  {SCREEN_CENTER_X - SQUARE_SIZE/2, SCREEN_CENTER_Y + SQUARE_SIZE/2}
};

const String KEY_UP_ARROW = "26";

int currentPosition = 0;
unsigned long lastActionTime = 0;
const unsigned long ACTION_DELAY = 2000;
bool keyPressed = false;

void setup() {
  Serial.begin(9600);
  
  delay(2000);
  
  Serial.println("# Auto Demo Starting - Mouse Square + Arrow Key");
  Serial.println("# Moving mouse in square pattern with arrow key presses");
}

void loop() {
  unsigned long currentTime = millis();
  
  if (currentTime - lastActionTime >= ACTION_DELAY) {
    
    if (!keyPressed) {
      moveMouseToPosition(currentPosition);
      keyPressed = true;
      
    } else {
      pressArrowKey();
      
      currentPosition = (currentPosition + 1) % 4;
      keyPressed = false;
    }
    
    lastActionTime = currentTime;
  }
}

void moveMouseToPosition(int position) {
  int x = SQUARE_POSITIONS[position][0];
  int y = SQUARE_POSITIONS[position][1];
  
  Serial.print("0 7 ");
  Serial.print(x);
  Serial.print(" ");
  Serial.println(y);
}

void pressArrowKey() {
  Serial.print("1 1 ");
  Serial.println(KEY_UP_ARROW);
  
  delay(50);
  
  Serial.print("1 0 ");
  Serial.println(KEY_UP_ARROW);
}
