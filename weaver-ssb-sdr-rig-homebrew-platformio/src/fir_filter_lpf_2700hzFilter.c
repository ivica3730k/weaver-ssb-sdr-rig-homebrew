#include <fir_filter_lpf_2700hzFilter.h>


static int filter_taps[FIR_FILTER_LPF_2700HZFILTER_TAP_NUM] = {
  -308,
  386,
  359,
  304,
  157,
  -45,
  -200,
  -215,
  -71,
  147,
  296,
  261,
  41,
  -240,
  -396,
  -300,
  19,
  374,
  526,
  336,
  -122,
  -576,
  -709,
  -366,
  310,
  917,
  1010,
  389,
  -711,
  -1661,
  -1713,
  -404,
  2143,
  5189,
  7655,
  8601,
  7655,
  5189,
  2143,
  -404,
  -1713,
  -1661,
  -711,
  389,
  1010,
  917,
  310,
  -366,
  -709,
  -576,
  -122,
  336,
  526,
  374,
  19,
  -300,
  -396,
  -240,
  41,
  261,
  296,
  147,
  -71,
  -215,
  -200,
  -45,
  157,
  304,
  359,
  386,
  -308
};

void fir_filter_lpf_2700hzFilter_init(fir_filter_lpf_2700hzFilter* f) {
  int i;
  for(i = 0; i < FIR_FILTER_LPF_2700HZFILTER_TAP_NUM; ++i)
    f->history[i] = 0;
  f->last_index = 0;
}

void fir_filter_lpf_2700hzFilter_put(fir_filter_lpf_2700hzFilter* f, int input) {
  f->history[f->last_index++] = input;
  if(f->last_index == FIR_FILTER_LPF_2700HZFILTER_TAP_NUM)
    f->last_index = 0;
}

int fir_filter_lpf_2700hzFilter_get(fir_filter_lpf_2700hzFilter* f) {
  long long acc = 0;
  int index = f->last_index, i;
  for(i = 0; i < FIR_FILTER_LPF_2700HZFILTER_TAP_NUM; ++i) {
    index = index != 0 ? index-1 : FIR_FILTER_LPF_2700HZFILTER_TAP_NUM-1;
    acc += (long long)f->history[index] * filter_taps[i];
  };
  return acc >> 16;
}