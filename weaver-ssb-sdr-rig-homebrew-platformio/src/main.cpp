#include <Arduino.h>
#define LED PC13
#include "stm32_def.h"
#include "stm32f1xx_hal_msp.h"
#include <fir_filter_lpf_2700hzFilter.h>
#include <fir_filter_lpf_2700hzFilter.c>
fir_filter_lpf_2700hzFilter i_fir_filter_lpf_2700hzFilter;
#define SAMPLE_RATE 11025
void setup()
{
  pinMode(LED, OUTPUT);
  fir_filter_lpf_2700hzFilter_init(&i_fir_filter_lpf_2700hzFilter);
  Serial1.begin(115200);
}
void loop()
{

  for (int i = 0; i < SAMPLE_RATE; i++)
  {
    float sin_wave = sin(2 * PI * 1400 * i / SAMPLE_RATE);
    float sin_wave2 = sin(2 * PI * 2100 * i / SAMPLE_RATE);
    // int16_t signal = static_cast<int16_t>(sin_wave * 2048);
    int16_t signal1 = static_cast<int16_t>((sin_wave) * 2048);
    int16_t signal2 = static_cast<int16_t>((sin_wave2) * 2048);
    int16_t signal = signal1 + signal2;
    fir_filter_lpf_2700hzFilter_put(&i_fir_filter_lpf_2700hzFilter, signal);
    signal = fir_filter_lpf_2700hzFilter_get(&i_fir_filter_lpf_2700hzFilter);
    Serial.write(reinterpret_cast<uint8_t *>(&signal), sizeof(signal));
  }
}