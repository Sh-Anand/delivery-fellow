#include <Servo.h>
#include <FastLED.h>
#include <arduino-timer.h>
#include <Ultrasonic.h>

#define LED_PIN  9
#define LED_PIN_REAR 8
#define NUM_LEDS  86
#define NUM_BLINK_LEDS  11
#define BRIGHTNESS  20
#define initPin 22
#define STOP_TIMEOUT 4000


CRGB ledsF[NUM_LEDS/2];
CRGB ledsR[NUM_LEDS/2];

void timeout();
void unclampAndBrake();
void blinkWhite1();
void blinkWhite2();
void blinkRed1();
void blinkRed2();
void evaluateUS();

int t_blink = 500;
int f_orange = 50;
int f_white = 30;

byte ESC1pin = 3, ESC2pin = 2, Clamp1pin = 4, Clamp2pin = 5, Brake1pin = 6, Brake2pin = 7;
int Buttonpin = A0;
Servo ESC1, ESC2, Clamp1, Clamp2, Brake1, Brake2;
int timeoutInterval = 200;

//Ticker timeoutTicker(timeou t, timeoutInterval, MILLIS);
Timer<16, micros> timer;
auto stationary_timer = timer_create_default();
int blinkI = NUM_BLINK_LEDS - 1;
int rightBlink2 = 1;
int leftBlink1 = 1;
int leftBlink2 = 1;
bool blinking = false, stationary_started = false, clampedBraked = false;

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

  //init clamps
  Clamp1.attach(Clamp1pin);
  Clamp2.attach(Clamp2pin);

  //init brakes
  Brake1.attach(Brake1pin);
  Brake2.attach(Brake2pin);

  //unclamp and brake the servos
  unclampAndBrake();

  FastLED.addLeds<WS2812, LED_PIN, GRB>(ledsF, NUM_LEDS/2);
  FastLED.addLeds<WS2812, LED_PIN_REAR, GRB>(ledsR, NUM_LEDS/2);
  FastLED.setBrightness(BRIGHTNESS);
  RedWhite();
  //initialize timer to stop the motors on input timeout
  //timeoutTicker.start();
}

void loop() {
  if(!(analogRead(Buttonpin) > 1000 && digitalRead(initPin) == HIGH)) {
    ESC1.writeMicroseconds(1000);
    ESC2.writeMicroseconds(1000);
  }
  timer.tick();
  stationary_timer.tick();
  //timeoutTicker.update();
}

void serialEvent() {
//   if(analogRead(Buttonpin) <= 1000) {
//    ESC1.writeMicroseconds(1000);
//    ESC2.writeMicroseconds(1000);
//  }

  // see if there's incoming serial data:
  if (Serial.available() > 0) {
    //timeoutTicker.stop();
    // read the oldest byte in the serial buffer:
    if(Serial.read() == '#') {
      int ESC1Speed = Serial.parseInt();
      Serial.read();
      int ESC2Speed = Serial.parseInt();

      if(analogRead(Buttonpin) < 1000) {
        ESC1Speed = 1000;
        ESC2Speed = 1000;
        ESC1.writeMicroseconds(1000);
        ESC2.writeMicroseconds(1000);
      }
      else {
        ESC1.writeMicroseconds(ESC1Speed);
        ESC2.writeMicroseconds(ESC2Speed);
      }
      //Check clamping
      if(ESC1Speed == ESC2Speed && ESC1Speed == 1000) {
          if(!stationary_started) {
          stationary_timer.in(STOP_TIMEOUT, unclampAndBrake);
          stationary_started = true;
          }
      }
      else if(!clampedBraked) {
        stationary_timer.cancel();
        stationary_started = false;
        Clamp1.write(150);
        Clamp2.write(30);
        Brake1.write(180);
        Brake2.write(0);
        clampedBraked = true;
      }

      //Blink indicator lights
      if(ESC1Speed == ESC2Speed) {
        blinking = false;
        RedWhite();
      }
      else if(abs(ESC1Speed - 1000) < abs(ESC2Speed - 1000)) {
        if(!blinking) {
          blinking = true;
          blinkRight1();
        }
      }
      else {
        if(!blinking) {
          blinking = true;
          blinkLeft1();
        }
      }
    }
    //timeoutTicker.interval(timeoutInterval);
    //timeoutTicker.start();
  }
}

//when not going left or right
void RedWhite(){
  for(int i = 0; i < NUM_LEDS/2; i++){
    ledsF[i] = CRGB::White;
    ledsR[i] = CRGB::Red;
  }
  FastLED.show();
}

void blinkRight1(){
   if (blinkI < NUM_LEDS/2){
     ledsF[blinkI] = CRGB::Orange; 
   }else{
     ledsR[blinkI-NUM_LEDS/2] = CRGB::Orange;
   }
   if(NUM_LEDS-blinkI-1 < NUM_LEDS/2){
     ledsF[NUM_LEDS-blinkI-1] = CRGB::Orange;
   }else{
    ledsR[NUM_LEDS-blinkI-1-NUM_LEDS/2] = CRGB::Orange;
   }
   FastLED.show();
   if(blinkI == 0) {
    blinkI = NUM_BLINK_LEDS - 1;
    timer.cancel();
    timer.in(t_blink, blinkRight2);
    return;
   }
   blinkI--;
   timer.in(f_orange, blinkRight1);
}

void blinkRight2() {
   
   if (blinkI < NUM_LEDS/2){
     ledsF[blinkI] = CRGB::White; 
   }else{
     ledsR[blinkI-NUM_LEDS/2] = CRGB::White;
   }
   if(NUM_LEDS-blinkI-1 < NUM_LEDS/2){
     ledsF[NUM_LEDS-blinkI-1] = CRGB::Red;
   }else{
    ledsR[NUM_LEDS-blinkI-1-NUM_LEDS/2] = CRGB::Red;
   }
//   leds[blinkI] = CRGB::White;
//   leds[NUM_LEDS-blinkI-1] = CRGB::Red;
   FastLED.show();
   if(blinkI == 0) {
    blinkI = NUM_BLINK_LEDS - 1;
    timer.cancel();
    blinking = false;
    return;
   }
   blinkI--;
   timer.in(f_white, blinkRight2);
}

//delay(t_blink);

//when going left
void blinkLeft1() {
  if(NUM_LEDS/2-blinkI-1 < NUM_LEDS/2){
    ledsF[NUM_LEDS/2-blinkI-1] = CRGB::Orange;
  }else{
    ledsR[NUM_LEDS/2-blinkI-1-NUM_LEDS/2] = CRGB::Orange;
  }
  if(NUM_LEDS/2+blinkI < NUM_LEDS/2){
    ledsF[NUM_LEDS/2+blinkI] = CRGB::Orange;
  }else{
    ledsR[NUM_LEDS/2+blinkI-NUM_LEDS/2] = CRGB::Orange;
  }
  FastLED.show();
  if(blinkI == 0) {
    blinkI = NUM_BLINK_LEDS - 1;
    timer.cancel();
    timer.in(t_blink, blinkLeft2);
    return;
   }
  blinkI--;
  timer.in(f_orange, blinkLeft1);
}

void blinkLeft2() {
  if(NUM_LEDS/2-blinkI-1 < NUM_LEDS/2){
    ledsF[NUM_LEDS/2-blinkI-1] = CRGB::White;
  }else{
    ledsR[NUM_LEDS/2-blinkI-1-NUM_LEDS/2] = CRGB::White;
  }
  if(NUM_LEDS/2+blinkI < NUM_LEDS/2){
    ledsF[NUM_LEDS/2+blinkI] = CRGB::Red;
  }else{
    ledsR[NUM_LEDS/2+blinkI-NUM_LEDS/2] = CRGB::Red;
  }
  FastLED.show();
  if(blinkI == 0) {
    blinkI = NUM_BLINK_LEDS - 1;
    timer.cancel();
    blinking = false;
    return;
   }
  blinkI--;
  timer.in(f_white, blinkLeft2);
}

//unclamp and brake when it stops
void unclampAndBrake() {
   Clamp1.write(180);
   Clamp2.write(0);
   Brake1.write(140);
   Brake2.write(40);
   stationary_started = false;
   clampedBraked = false;
}

//void timeout() {
  //ESC1.writeMicroseconds(1000);
  //ESC2.writeMicroseconds(1000);
//a}
