#include <Arduino.h>
#define LED_BUILTIN PC13
#if !(defined(STM32F0) || defined(STM32F1) || defined(STM32F2) || defined(STM32F3) || defined(STM32F4) || defined(STM32F7) || \
      defined(STM32L0) || defined(STM32L1) || defined(STM32L4) || defined(STM32H7) || defined(STM32G0) || defined(STM32G4) || \
      defined(STM32WB) || defined(STM32MP1) || defined(STM32L5))
#error This code is designed to run on STM32F/L/H/G/WB/MP1 platform! Please check your Tools->Board setting.
#endif

#include "STM32TimerInterrupt.h"

#include "stm32f1xx_hal.h"
#define ADCCONVERTEDVALUES_BUFFER_SIZE ((uint32_t)2) /* Size of array containing ADC converted values */

ADC_HandleTypeDef AdcHandle;
__IO uint16_t aADCxConvertedValues[ADCCONVERTEDVALUES_BUFFER_SIZE];
bool adc_conversion_complete = false;

/**
    @brief  This function handles ADC interrupt request.
    @param  None
    @retval None
*/
extern "C" void ADC1_2_IRQHandler(void)
{
  HAL_ADC_IRQHandler(&AdcHandle);
}

/**
  @brief  This function handles DMA interrupt request.
  @param  None
  @retval None
*/
extern "C" void DMA1_Channel1_IRQHandler(void)
{
  HAL_DMA_IRQHandler(AdcHandle.DMA_Handle);
}

/**
    @brief ADC MSP initialization
           This function configures the hardware resources used in this example:
             - Enable clock of ADC peripheral
             - Configure the GPIO associated to the peripheral channels
             - Configure the DMA associated to the peripheral
             - Configure the NVIC associated to the peripheral interruptions
    @param hadc: ADC handle pointer
    @retval None
*/
extern "C" void HAL_ADC_MspInit(ADC_HandleTypeDef *hadc)
{
  GPIO_InitTypeDef GPIO_InitStruct;
  static DMA_HandleTypeDef DmaHandle;
  RCC_PeriphCLKInitTypeDef PeriphClkInit;

  /*##-1- Enable peripherals and GPIO Clocks #################################*/
  /* Enable clock of GPIO associated to the peripheral channels */
  //  __HAL_RCC_GPIOA_CLK_ENABLE();

  /* Enable clock of ADCx peripheral */
  __HAL_RCC_ADC1_CLK_ENABLE();

  /* Configure ADCx clock prescaler */
  /* Caution: On STM32F1, ADC clock frequency max is 14MHz (refer to device   */
  /*          datasheet).                                                     */
  /*          Therefore, ADC clock prescaler must be configured in function   */
  /*          of ADC clock source frequency to remain below this maximum      */
  /*          frequency.                                                      */
  PeriphClkInit.PeriphClockSelection = RCC_PERIPHCLK_ADC;
  PeriphClkInit.AdcClockSelection = RCC_ADCPCLK2_DIV6;
  HAL_RCCEx_PeriphCLKConfig(&PeriphClkInit);

  /* Enable clock of DMA associated to the peripheral */
  __HAL_RCC_DMA1_CLK_ENABLE();

  /*##-2- Configure peripheral GPIO ##########################################*/
  /* Configure GPIO pin of the selected ADC channel */
  GPIO_InitStruct.Pin = ADC_CHANNEL_3 | ADC_CHANNEL_4;
  GPIO_InitStruct.Mode = GPIO_MODE_ANALOG;
  GPIO_InitStruct.Pull = GPIO_PIN_3 | GPIO_PIN_4;
  HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

  /*##-3- Configure the DMA ##################################################*/
  /* Configure DMA parameters */
  DmaHandle.Instance = DMA1_Channel1;

  DmaHandle.Init.Direction = DMA_PERIPH_TO_MEMORY;
  DmaHandle.Init.PeriphInc = DMA_PINC_DISABLE;
  DmaHandle.Init.MemInc = DMA_MINC_ENABLE;
  DmaHandle.Init.PeriphDataAlignment = DMA_PDATAALIGN_HALFWORD; /* Transfer from ADC by half-word to match with ADC configuration: ADC resolution 10 or 12 bits */
  DmaHandle.Init.MemDataAlignment = DMA_MDATAALIGN_HALFWORD;    /* Transfer to memory by half-word to match with buffer variable type: half-word */
  DmaHandle.Init.Mode = DMA_CIRCULAR;                           /* DMA in circular mode to match with ADC configuration: DMA continuous requests */
  DmaHandle.Init.Priority = DMA_PRIORITY_HIGH;

  /* Deinitialize  & Initialize the DMA for new transfer */
  HAL_DMA_DeInit(&DmaHandle);
  HAL_DMA_Init(&DmaHandle);

  /* Associate the initialized DMA handle to the ADC handle */
  __HAL_LINKDMA(hadc, DMA_Handle, DmaHandle);

  /*##-4- Configure the NVIC #################################################*/

  /* NVIC configuration for DMA interrupt (transfer completion or error) */
  /* Priority: high-priority */
  HAL_NVIC_SetPriority(DMA1_Channel1_IRQn, 1, 0);
  HAL_NVIC_EnableIRQ(DMA1_Channel1_IRQn);

  /* NVIC configuration for ADC interrupt */
  /* Priority: high-priority */
  HAL_NVIC_SetPriority(ADC1_2_IRQn, 0, 0);
  HAL_NVIC_EnableIRQ(ADC1_2_IRQn);
}

/**
    @brief ADC MSP de-initialization
           This function frees the hardware resources used in this example:
             - Disable clock of ADC peripheral
             - Revert GPIO associated to the peripheral channels to their default state
             - Revert DMA associated to the peripheral to its default state
             - Revert NVIC associated to the peripheral interruptions to its default state
    @param hadc: ADC handle pointer
    @retval None
*/
extern "C" void HAL_ADC_MspDeInit(ADC_HandleTypeDef *hadc)
{
  /*##-1- Reset peripherals ##################################################*/
  __HAL_RCC_ADC1_FORCE_RESET();
  __HAL_RCC_ADC1_RELEASE_RESET();

  /*##-2- Disable peripherals and GPIO Clocks ################################*/
  /* De-initialize GPIO pin of the selected ADC channel */
  HAL_GPIO_DeInit(GPIOA, GPIO_PIN_3 | GPIO_PIN_4);

  /*##-3- Disable the DMA ####################################################*/
  /* De-Initialize the DMA associated to the peripheral */
  if (hadc->DMA_Handle != NULL)
  {
    HAL_DMA_DeInit(hadc->DMA_Handle);
  }

  /*##-4- Disable the NVIC ###################################################*/
  /* Disable the NVIC configuration for DMA interrupt */
  HAL_NVIC_DisableIRQ(DMA1_Channel1_IRQn);

  /* Disable the NVIC configuration for ADC interrupt */
  HAL_NVIC_DisableIRQ(ADC1_2_IRQn);
}

/**
    @brief  ADC configuration
    @param  None
    @retval None
*/
static void ADC_Config(void)
{
  ADC_ChannelConfTypeDef sConfig;
  ADC_AnalogWDGConfTypeDef AnalogWDGConfig;

  /* Configuration of ADCx init structure: ADC parameters and regular group */
  AdcHandle.Instance = ADC1;

  AdcHandle.Init.DataAlign = ADC_DATAALIGN_RIGHT;
  AdcHandle.Init.ScanConvMode = ADC_SCAN_ENABLE;        /* Sequencer disabled (ADC conversion on only 1 channel: channel set on rank 1) */
  AdcHandle.Init.ContinuousConvMode = ENABLE;           /* Continuous mode to have maximum conversion speed (no delay between conversions) */
  AdcHandle.Init.NbrOfConversion = 2;                   /* Parameter discarded because sequencer is disabled */
  AdcHandle.Init.DiscontinuousConvMode = DISABLE;       /* Parameter discarded because sequencer is disabled */
  AdcHandle.Init.NbrOfDiscConversion = 2;               /* Parameter discarded because sequencer is disabled */
  AdcHandle.Init.ExternalTrigConv = ADC_SOFTWARE_START; /* Software start to trig the 1st conversion manually, without external event */

  if (HAL_ADC_Init(&AdcHandle) != HAL_OK)
  {
    /* ADC initialization error */
    Error_Handler();
  }

  /* Configuration of channel on ADCx regular group on sequencer rank 1 */
  /* Note: Considering IT occurring after each ADC conversion if ADC          */
  /*       conversion is out of the analog watchdog window selected (ADC IT   */
  /*       enabled), select sampling time and ADC clock with sufficient       */
  /*       duration to not create an overhead situation in IRQHandler.        */
  sConfig.Channel = ADC_CHANNEL_3;
  sConfig.Rank = ADC_REGULAR_RANK_1;
  sConfig.SamplingTime = ADC_SAMPLETIME_41CYCLES_5;

  if (HAL_ADC_ConfigChannel(&AdcHandle, &sConfig) != HAL_OK)
  {
    /* Channel Configuration Error */
    Error_Handler();
  }

  sConfig.Channel = ADC_CHANNEL_4;
  sConfig.Rank = ADC_REGULAR_RANK_2;

  if (HAL_ADC_ConfigChannel(&AdcHandle, &sConfig) != HAL_OK)
  {
    /* Channel Configuration Error */
    Error_Handler();
  }
}
/**
    @brief  Conversion complete callback in non blocking mode
    @param  AdcHandle : AdcHandle handle
    @note   This example shows a simple way to report end of conversion
            and get conversion result. You can add your own implementation.
    @retval None
*/
extern "C" void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef *)
{
  adc_conversion_complete = true;
}

/**
    @brief  Conversion DMA half-transfer callback in non blocking mode
    @param  hadc: ADC handle
    @retval None
*/
extern "C" void HAL_ADC_ConvHalfCpltCallback(ADC_HandleTypeDef *)
{
}

/**
    @brief  ADC error callback in non blocking mode
           (ADC conversion with interruption or transfer by DMA)
    @param  hadc: ADC handle
    @retval None
*/
extern "C" void HAL_ADC_ErrorCallback(ADC_HandleTypeDef *)
{
  /* In case of ADC error, call main error handler */
  Error_Handler();
}
// the setup routine runs once when you press reset:

#define SAMPLE_RATE 44100
STM32Timer ITimer(TIM1);

long current_sample_rx = 0;
void sampling_loop_rx()
{
  digitalWrite(PC14, !digitalRead(PC14));
  while (!adc_conversion_complete)
  {
    /* code */
  }
  adc_conversion_complete = false;
  uint16_t adc1 = aADCxConvertedValues[0];
  uint16_t adc2 = aADCxConvertedValues[1];

  // convert two readings to two set of 8 bit values in their own separate buffers
  // send the two buffers over serial
  byte adc1_bytes[2] = {adc1 >> 8, adc1 & 0xFF};
  byte adc2_bytes[2] = {adc2 >> 8, adc2 & 0xFF};

  Serial.write(adc1_bytes, 2);

  if (current_sample_rx >= SAMPLE_RATE)
  {
    digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
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
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(PC14, OUTPUT);
  pinMode(PA3, INPUT_ANALOG);
  pinMode(PA4, INPUT_ANALOG);
  Serial.begin();
  Serial1.begin(9600);
  delay(5000);

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

// the loop routine runs over and over again forever:
void loop()
{
  //   /* Turn-on/off LED_BUILTIN in function of ADC conversion result */
  //   /*  - Turn-off if voltage is into AWD window */
  //   /*  - Turn-on if voltage is out of AWD window */

  //   /* Variable of analog watchdog status is set into analog watchdog         */
  //   /* interrupt callback                                                     */
  //   long micros_a = 0;
  //   long micros_b = 0;
  //   micros_a = micros();
  //   if (adc_conversion_complete == true)
  //   {
  //     micros_b = micros();
  //     adc_conversion_complete = false;
  //     Serial.print("ADC1: ");
  //     Serial.println(aADCxConvertedValues[0]);
  //     Serial.print("ADC2: ");
  //     Serial.println(aADCxConvertedValues[1]);
  //   }
  //   Serial.print("Time between adc samples in us: ");
  //   Serial.println(micros_b - micros_a);
  // Serial1.println(millis());
  // delay(1000);
}