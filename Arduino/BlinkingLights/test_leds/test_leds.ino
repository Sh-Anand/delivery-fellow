#include <FastLED.h>
#define LED_PIN  5
#define NUM_LEDS  30
#define NUM_BLINK_LEDS  7
#define BRIGHTNESS  20
CRGB leds[NUM_LEDS];

int t_blink = 500;
int f_orange = 50;
int f_white = 30;

void setup(){
  FastLED.addLeds<WS2812, LED_PIN, GRB>(leds, NUM_LEDS);
  FastLED.setBrightness(BRIGHTNESS);
  RedWhite();
}

void loop(){
  delay(3000);
  for(int k = 0; k <= 3; k++){
    blinkRight();
  }
  for(int k = 0; k<= 3; k++){
    blinkLeft();
  }
}

void allWhite(){
  for(int i = 0; i <= 9; i++){
    leds[i] = CRGB::White;
    FastLED.show();
  }
}

void RedWhite(){
  for(int i = 0; i < NUM_LEDS/2; i++){
    leds[i] = CRGB::White;
  }
  for(int i = NUM_LEDS/2; i < NUM_LEDS; i++){
    leds[i] = CRGB::Red;
  }
  FastLED.show();
}

void blinkRight(){
  for(int i = NUM_BLINK_LEDS-1; i >= 0; i--){
    leds[i] = CRGB::Orange;
    leds[NUM_LEDS-i-1] = CRGB::Orange;
    FastLED.show();
    delay(f_orange);
  }
  delay(t_blink);
  for(int i = NUM_BLINK_LEDS-1; i >= 0; i--){
    leds[i] = CRGB::White;
    leds[NUM_LEDS-i-1] = CRGB::Red;
    FastLED.show();
    delay(f_white);
  }
  delay(t_blink);
}

void blinkLeft(){
  for(int i = NUM_BLINK_LEDS-1; i >= 0; i--){
    leds[NUM_LEDS/2-i-1] = CRGB::Orange;
    leds[NUM_LEDS/2+i] = CRGB::Orange;
    FastLED.show();
    delay(f_orange);
  }
  delay(t_blink);
  for(int i = NUM_BLINK_LEDS-1; i >= 0; i--){
    leds[NUM_LEDS/2-i-1] = CRGB::White;
    leds[NUM_LEDS/2+i] = CRGB::Red;
    FastLED.show();
    delay(f_white);
  }
  delay(t_blink);
}
