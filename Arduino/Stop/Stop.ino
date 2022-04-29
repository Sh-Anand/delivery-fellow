#include <Servo.h>
#include <Ultrasonic.h>

#define US_N_PIN_1    46
#define US_N_PIN_2    47
#define US_TIMEOUT    20000UL

Ultrasonic us_N   (US_N_PIN_1,    US_N_PIN_2);//,   US_TIMEOUT);

byte ESC1pin = 3, ESC2pin = 5;
Servo ESC1, ESC2;
int speed = 1000;
void setup() {
  Serial.begin(9600);
  //pinMode(LED_BUILTIN, OUTPUT);
  ESC1.attach(ESC1pin);
  ESC1.writeMicroseconds(1000);
  ESC2.attach(ESC2pin);
   ESC2.writeMicroseconds(1000);
}

void loop() {
  Serial.println("Test");
  delay(1);
   //analogWrite(3, 250);
   //analogWrite(5, 250);
}
