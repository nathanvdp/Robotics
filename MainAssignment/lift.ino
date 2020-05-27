/*Example sketch to control a stepper motor with A4988/DRV8825 stepper motor
driver and Arduino without a library. More info: https://www.makerguides.com */

// Define stepper motor connections and steps per revolution:
#define dirPin 2
#define stepPin 5
#define stepsPerRevolution 400
int Mspeed = 500;
int totalSteps = 4600;

void spinDown(float revs){

  // Set the spinning direction counterclockwise:
  digitalWrite(dirPin, HIGH);
  delayMicroseconds(500);
  // Spin the stepper motor 5 revolutions fast:
  for (int i = 0; i < (revs) *  stepsPerRevolution; i++) {
    // These four lines result in 1 step:
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(Mspeed);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(Mspeed);
  }
}

void spinUp(float revs){

  // Set the spinning direction counterclockwise:

  digitalWrite(dirPin, LOW);
  delayMicroseconds(500);
  // Spin the stepper motor 5 revolutions fast:
  for (int i = 0; i < ( revs) * stepsPerRevolution; i++) {
    // These four lines result in 1 step:
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(Mspeed);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(Mspeed);
  }
}


void spinOffset(int steps){

  // Set the spinning direction counterclockwise:

  digitalWrite(dirPin, LOW);
  delayMicroseconds(500);
  // Spin the stepper motor 5 revolutions fast:
  for (int i = 0; i < steps ; i++) {
    // These four lines result in 1 step:
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(Mspeed);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(Mspeed);
  }

}


void setup() {
  // Declare pins as output:
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(4, OUTPUT);
  digitalWrite(4,HIGH);

}
unsigned long time_now = 0;
int period = 1000;

void loop() {
  spinUp(11.5);
  spinDown(11.5);
  time_now = millis();
}
