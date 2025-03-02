#include <FastLED.h>

#define LED_DataPin 3
#define Num_LED 50
#define flash_Input 9

CRGB leds[Num_LED];

bool last_flash_status = false;
uint8_t flash_duration = 65;

void setup() {
  pinMode(flash_Input, INPUT_PULLUP);
  FastLED.addLeds<WS2812, LED_DataPin, RGB>(leds, Num_LED);
  FastLED.setBrightness(95);
  FastLED.clear();
  FastLED.show();

  for (uint8_t a = 0; a < 5; a++) {
    flash_Turn_On();
    delay(50);
    flash_Turn_Off();
    delay(50);
  }
  last_flash_status = false;
}

void loop() {
  if (digitalRead(flash_Input) && last_flash_status != digitalRead(flash_Input)) {
    perform_flash(flash_duration);
    last_flash_status = digitalRead(flash_Input);
  } else {
    flash_Turn_Off();
  }
}

void perform_flash(uint8_t flash_duration) {
  for (uint8_t a = 0; a < 10; a++) {
    flash_Turn_Off();
    delay(50);
    flash_Turn_On();
    delay(50);
  }
  delay(flash_duration * 1000);
}


void flash_Turn_On() {
  FastLED.clear();
  for (int i = 0; i < 46; i++) {
    leds[i] = CRGB(0xF3E7D3);
  }

  FastLED.show();
}

void flash_Turn_Off() {

  FastLED.clear();
  for (int i = 0; i < 46; i++) {
    leds[i] = CRGB(0x000000);
  }
  FastLED.show();
}
