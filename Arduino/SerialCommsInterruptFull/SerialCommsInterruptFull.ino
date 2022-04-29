#include <Servo.h>
#include <Ticker.h>

void timeout();

int initPin = 22;
byte ESC1pin = 3, ESC2pin = 2;
int buttonPin = A0;
Servo ESC1, ESC2;
int timeoutInterval = 200;
bool disabled = false;
//Ticker timeoutTicker(timeout, timeoutInterval, MILLIS);

const int ledPin = 13; // the pin that the LED is attached to
int incomingByte = 1100;      // a variable to read incoming serial data into

void setup() {
  // initialize serial communication:
  Serial.begin(9600);

  //initialize
  pinMode(initPin, OUTPUT);
  digitalWrite(initPin, HIGH);
  
  //initialize ESC pins and stop the motors
  ESC1.attach(ESC1pin);
  ESC1.writeMicroseconds(1000);
  ESC2.attach(ESC2pin);
  ESC2.writeMicroseconds(1000);

  //init emergency button pin
  pinMode(buttonPin, INPUT);
  attachInterrupt(digitalPinToInterrupt(buttonPin), toggleDisable, CHANGE);

  if(digitalRead(buttonPin) == HIGH)
    disabled = true;

  //initialize timer to stop the motors on input timeout
  //timeoutTicker.start();
}

void loop() {
  if(disabled) {
    ESC1.writeMicroseconds(1000);
    ESC2.writeMicroseconds(1000);
  }

  //timeoutTicker.update();
}

void serialEvent() {
  // see if there's incoming serial data:
  if (!disabled && Serial.available() > 0) {
    //timeoutTicker.stop();
    // read the oldest byte in the serial buffer:
    if(Serial.read() == '#') {
      ESC1.writeMicroseconds(Serial.parseInt());
      Serial.read();
      ESC2.writeMicroseconds(Serial.parseInt());
    }
    //timeoutTicker.interval(timeoutInterval);
    //timeoutTicker.start();
  }
}

void toggleDisable() {
  disabled != disabled;
}

//void timeout() {
  //ESC1.writeMicroseconds(1000);
  //ESC2.writeMicroseconds(1000);
//a}
