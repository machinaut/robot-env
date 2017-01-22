// widowxctl - simple robot arm control for WidowX arm from trossen robotics

#include <ax12.h>
#include <BioloidController.h>
#include "poses.h"

BioloidController bioloid = BioloidController(1000000);

const int SERVOCOUNT = 6;  //number of servos in this robot
int id;
int pos;
//float voltage;
boolean RunCheck;          //


Servo baseSrv;  // Base Servo - Digital I/O 3
Servo shoulderSrv;  // Shoulder Servo - Digital I/O 5
Servo elbowSrv;  // Elbow Servo - Digital I/O 6
Servo wristSrv;  // Wrist Servo - Digital I/O 9
Servo gripSrv;  // Grip Servo - Digital I/O 10

int basePot = 0;  // Base Joystick (potentiometer) - Analog I/O 0
int shoulderPot = 1;  // Shoulder Joystick (potentiometer) - Analog I/O 1
int elbowPot = 2;  // Elbow Joystick (potentiometer) - Analog I/O 2
int wristPot = 3;  // Wrist Joystick (potentiometer) - Analog I/O 3
int gripPot = 4;  // Grip Dial (potentiometer) - Analog I/O 4

int captPin = 2;  // capture button - Digital I/O 2
int playPin = 4;  // playback button - Digital I/O 4

void printPositions(void);
void centerServos(void);
void writeServos(void);

void setup() {
  ///////////////////
  Serial.begin(9600);  // TODO: try 115200
  Serial.setTimeout(10);  // Timeout waiting for input after 10 milliseconds
  delay(500);  // TODO: REMOVEME
  dxlVoltageReport(SERVOCOUNT);
  dxlServoReport(SERVOCOUNT);  // scan servos, return position and error

  centerServos();

  while (!Serial);  // Wait for serial port to connect
}

void loop() {
  printPositions();
  if (Serial.available() > 0) {
    writeServos();
  }
}

void printPositions(void) {
  int basePos = analogRead(basePot);  // Base Joystick Position
  int shoulderPos = analogRead(shoulderPot);  // Shoulder Joystick Position
  int elbowPos = analogRead(elbowPot);  // Elbow Joystick Position
  int wristPos = analogRead(wristPot);  // Wrist Joystick Position
  int gripPos = analogRead(gripPot);  // Grip Joystick Position
  int captVal = digitalRead(captPin);  // Capture Button Value (HIGH / LOW)
  int playVal = digitalRead(playPin);  // Playback Button Value (HIGH / LOW)

  Serial.print('R');
  Serial.print(basePos); Serial.print(',');
  Serial.print(shoulderPos); Serial.print(',');
  Serial.print(elbowPos); Serial.print(',');
  Serial.print(wristPos); Serial.print(',');
  Serial.print(gripPos); Serial.print(',');
  Serial.print(captVal); Serial.print(',');
  Serial.print(playVal); Serial.print('\n');
  Serial.flush();
}

void writeServos(void) {
  Serial.readStringUntil('W');
  int baseCmd = Serial.parseInt();  Serial.read();  // Skip comma
  int shoulderCmd = Serial.parseInt();  Serial.read();  // Skip comma
  int elbowCmd = Serial.parseInt();  Serial.read();  // Skip comma
  int wristCmd = Serial.parseInt();  Serial.read();  // Skip comma
  int gripCmd = Serial.parseInt();  Serial.read();  // Skip newline

  // baseCmd = constrain(baseCmd, 0, 180);
  // shoulderCmd = constrain(shoulderCmd, 0, 180);
  // elbowCmd = constrain(elbowCmd, 0, 180);
  // wristCmd = constrain(wristCmd, 0, 180);
  // gripCmd = constrain(gripCmd, 0, 180);

  // baseSrv.write(baseCmd);
  // shoulderSrv.write(shoulderCmd);
  // elbowSrv.write(elbowCmd);
  // wristSrv.write(wristCmd);
  // gripSrv.write(gripCmd);
  dxlSetGoalPosition(1, baseCmd);

  Serial.print('E');
  Serial.print(baseCmd); Serial.print(',');
  Serial.print(shoulderCmd); Serial.print(',');
  Serial.print(elbowCmd); Serial.print(',');
  Serial.print(wristCmd); Serial.print(',');
  Serial.print(gripCmd); Serial.print('\n');
  Serial.flush();
}

void centerServos(void) {
  // TODO: remove this?
  // Move to centered position
  bioloid.loadPose(Center);      // load the pose from FLASH, into the nextPose buffer
  bioloid.readPose();            // read in current servo positions to the curPose buffer
  // Travel
  bioloid.interpolateSetup(1000); // setup for interpolation from current->next over 1/2 a second
  while(bioloid.interpolating > 0){  // do this while we have not reached our new pose
      bioloid.interpolateStep();     // move servos, if necessary.
      delay(3);
  }
}
