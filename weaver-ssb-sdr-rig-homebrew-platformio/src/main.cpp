#include <Arduino.h>
#define LED PC13
#include "stm32_def.h"
#include "adc_dma.h"
#if !(defined(STM32F0) || defined(STM32F1) || defined(STM32F2) || defined(STM32F3) || defined(STM32F4) || defined(STM32F7) || \
      defined(STM32L0) || defined(STM32L1) || defined(STM32L4) || defined(STM32H7) || defined(STM32G0) || defined(STM32G4) || \
      defined(STM32WB) || defined(STM32MP1) || defined(STM32L5))
#error This code is designed to run on STM32F/L/H/G/WB/MP1 platform! Please check your Tools->Board setting.
#endif
#include <STM32TimerInterrupt.h>
#include "fir_filter_lpf_2700hzFilter.h"
#include "fir_filter_lpf_2700hzFilter.c"
fir_filter_lpf_2700hzFilter i_fir_filter_lpf_2700hzFilter;
fir_filter_lpf_2700hzFilter q_fir_filter_lpf_2700hzFilter;

#define SAMPLE_RATE 44100
STM32Timer ITimer(TIM1);

long current_sample_rx = 0;
void sampling_loop_rx()
{
  digitalWrite(PC14, !digitalRead(PC14));
  uint16_t i_value = 0;
  uint16_t q_value = 0;
  sample_iq_adc(i_value, q_value);
  fir_filter_lpf_2700hzFilter_put(&i_fir_filter_lpf_2700hzFilter, i_value);
  fir_filter_lpf_2700hzFilter_put(&q_fir_filter_lpf_2700hzFilter, q_value);
  i_value = fir_filter_lpf_2700hzFilter_get(&i_fir_filter_lpf_2700hzFilter);
  q_value = fir_filter_lpf_2700hzFilter_get(&q_fir_filter_lpf_2700hzFilter);
  Serial.write(reinterpret_cast<uint8_t *>(&i_value), sizeof(i_value));
  Serial.write(reinterpret_cast<uint8_t *>(&q_value), sizeof(q_value));

  if (current_sample_rx >= SAMPLE_RATE)
  {
    digitalWrite(LED, !digitalRead(LED));
    current_sample_rx = 0;
  }
  else if (current_sample_rx == 0)
  {
    current_sample_rx++;
  }
  else
  {
    current_sample_rx++;
  }
}

void setup()
{
  pinMode(LED, OUTPUT);
  pinMode(PC14, OUTPUT);
  pinMode(PA3, INPUT_ANALOG);
  pinMode(PA4, INPUT_ANALOG);
  fir_filter_lpf_2700hzFilter_init(&i_fir_filter_lpf_2700hzFilter);
  fir_filter_lpf_2700hzFilter_init(&q_fir_filter_lpf_2700hzFilter);
  Serial.begin();
  Serial1.begin(9600);

  // set the timmerinterrupt to run sample_loop_rx on SAMPLE_RATE hz

  if (ITimer.setFrequency(SAMPLE_RATE, sampling_loop_rx))
  {
    Serial.print(F("Starting  ITimer OK, millis() = "));
    Serial1.println(millis());
  }
  else
  {
    Serial.println(F("Can't set ITimer correctly. Select another freq. or timer"));
    while (1)
    {
      /* code */
    }
  }

  /* Configure the ADC peripheral */
  ADC_Config();

  /* Run the ADC calibration */
  if (HAL_ADCEx_Calibration_Start(&AdcHandle) != HAL_OK)
  {
    /* Calibration Error */
    Error_Handler();
  }
  /* Start ADC conversion on regular group with transfer by DMA */
  if (HAL_ADC_Start_DMA(&AdcHandle,
                        (uint32_t *)aADCxConvertedValues,
                        ADCCONVERTEDVALUES_BUFFER_SIZE) != HAL_OK)
  {
    /* Start Error */
    Error_Handler();
  }
}

void loop()
{
}