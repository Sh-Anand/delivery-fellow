#include <Servo.h>

byte ESC1pin = 3, ESC2pin = 2;
int Buttonpin = A0;
Servo ESC1, ESC2;

const int ledPin = 13; // the pin that the LED is attached to
int incomingByte = 1100;      // a variable to read incoming serial data into

void setup() {
  // initialize serial communication:
  Serial.begin(9600);
  // initialize the LED pin as an output:
  pinMode(ledPin, OUTPUT);

  //initialize ESC pins and stop the motors
  ESC1.attach(ESC1pin);
  ESC1.writeMicroseconds(1000);
  ESC2.attach(ESC2pin);
  ESC2.writeMicroseconds(1000);
}

void loop() {
  if(analogRead(Buttonpin) < 1000) {
    ESC1.writeMicroseconds(1000);
    ESC2.writeMicroseconds(1000);
  }

  // see if there's incoming serial data:
  else if (Serial.available() > 0) {
    // read the oldest byte in the serial buffer:
    if(Serial.read() == '#') {
      ESC1.writeMicroseconds(Serial.parseInt());
      Serial.read();
      ESC2.writeMicroseconds(Serial.parseInt());
    }
  }
}
