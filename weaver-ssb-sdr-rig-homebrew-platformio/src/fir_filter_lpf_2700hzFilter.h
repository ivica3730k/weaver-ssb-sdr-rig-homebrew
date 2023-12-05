#ifndef FIR_FILTER_LPF_2700HZFILTER_H_
#define FIR_FILTER_LPF_2700HZFILTER_H_

#include <Arduino.h>
/*

FIR filter designed with
 http://t-filter.appspot.com

sampling frequency: 44100 Hz

fixed point precision: 16 bits

* 0 Hz - 1350 Hz
  gain = 1
  desired ripple = 1 dB
  actual ripple = n/a

* 1550 Hz - 22050 Hz
  gain = 0
  desired attenuation = -40 dB
  actual attenuation = n/a

*/

#define FIR_FILTER_LPF_2700HZFILTER_TAP_NUM 512

typedef struct {
  int history[FIR_FILTER_LPF_2700HZFILTER_TAP_NUM];
  unsigned int last_index;
} fir_filter_lpf_2700hzFilter;

void fir_filter_lpf_2700hzFilter_init(fir_filter_lpf_2700hzFilter* f);
void fir_filter_lpf_2700hzFilter_put(fir_filter_lpf_2700hzFilter* f, uint16_t input);
uint16_t fir_filter_lpf_2700hzFilter_get(fir_filter_lpf_2700hzFilter* f);

#endif