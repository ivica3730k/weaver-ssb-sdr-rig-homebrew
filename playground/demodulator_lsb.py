import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig

RF_SAMPLE_RATE = 1e6
RF_CARRIER = 100000
from weaver_filter_lpf_4800hz import filter_taps as weaver_filter_lpf_4800hz_taps

# make 1 second of noise on RF_SAMPLE_RATE with amplitude 0.1
noise = np.random.normal(0, 0.25, int(RF_SAMPLE_RATE))

# make a signal 1khz above carrier
signal_wanted_1 = np.sin(2 * np.pi * (RF_CARRIER - 1000) * np.arange(0, 1, 1 / RF_SAMPLE_RATE))
signal_wanted_2 = np.sin(2 * np.pi * (RF_CARRIER - 1250) * np.arange(0, 1, 1 / RF_SAMPLE_RATE))
signal_wanted_3 = np.sin(2 * np.pi * (RF_CARRIER - 3200) * np.arange(0, 1, 1 / RF_SAMPLE_RATE))
signal_unwanted_1 = np.sin(2 * np.pi * (RF_CARRIER + 500) * np.arange(0, 1, 1 / RF_SAMPLE_RATE))

rf_signal = sig.resample(signal_wanted_1, int(RF_SAMPLE_RATE)) \
            + sig.resample(signal_wanted_2, int(RF_SAMPLE_RATE)) \
            + sig.resample(signal_unwanted_1, int(RF_SAMPLE_RATE)) \
            + sig.resample(noise, int(RF_SAMPLE_RATE)) \
            + sig.resample(signal_wanted_3, int(RF_SAMPLE_RATE))

# fft plot of rf_signal
plt.magnitude_spectrum(rf_signal, Fs=RF_SAMPLE_RATE, scale='dB')
plt.title('RF Signal Spectrum')
plt.show()

AF_SAMPLE_RATE = 22050
AF_LPF_LOW_CUTOFF = 0
AF_LPF_HIGH_CUTOFF = 4800
### - START OF THE EMULATED HARDWARE PART - ###
# lo frequency for weaver ssb demodulation is lo=carrier + 0.5*AF_LPF_CUTOFF
rf_lo = RF_CARRIER - 0.5 * (AF_LPF_LOW_CUTOFF + AF_LPF_HIGH_CUTOFF)
print(f"RF LO frequency for weaver ssb demodulation is {rf_lo} Hz")

# make 1 second of rf_lo signal for i and q
i_rf_lo = np.cos(2 * np.pi * rf_lo * np.arange(0, 1, 1 / RF_SAMPLE_RATE))
q_rf_lo = np.sin(2 * np.pi * rf_lo * np.arange(0, 1, 1 / RF_SAMPLE_RATE))

# multiply rf_signal with lo signal
i_rf_signal_at_rf_sample_rate = rf_signal * i_rf_lo
q_rf_signal_at_rf_sample_rate = rf_signal * q_rf_lo

# fft plot of i_rf_signal 
# plt.magnitude_spectrum(i_rf_signal_at_rf_sample_rate, Fs=RF_SAMPLE_RATE, scale='dB')
# plt.title('I RF Signal Spectrum')
# plt.show()
### - END OF EMULATED HARDWARE PART - ###
### - START OF THE SOFTWARE PART - ###
# resample i and q signals to AF_SAMPLE_RATE, in real implementation this would be adc read
i_af_signal = sig.resample(i_rf_signal_at_rf_sample_rate, int(AF_SAMPLE_RATE))
q_af_signal = sig.resample(q_rf_signal_at_rf_sample_rate, int(AF_SAMPLE_RATE))

# plt.plot(np.arange(0,1,1/AF_SAMPLE_RATE), i_af_signal, label='I')
# plt.plot(np.arange(0,1,1/AF_SAMPLE_RATE), q_af_signal, label='Q')
# plt.legend()
# plt.title('I and Q AF Signals before filtering - after first mixer')
# plt.show()


# fft plot of i_rf_signal
# plt.magnitude_spectrum(i_af_signal, Fs=AF_SAMPLE_RATE, scale='dB')
# plt.title('I AF Signal Spectrum')
# plt.show()

# filter i and q signals with weaver_filter_lpf_4800hz_taps
i_af_signal_filtered = sig.lfilter(weaver_filter_lpf_4800hz_taps, 1.0, i_af_signal)
q_af_signal_filtered = sig.lfilter(weaver_filter_lpf_4800hz_taps, 1.0, q_af_signal)

# fft plot of i_af_signal_filtered
# plt.magnitude_spectrum(i_af_signal_filtered, Fs=AF_SAMPLE_RATE, scale='dB')
# plt.title('I AF Signal Filtered Spectrum')
# plt.show()

af_lo = 0.5 * (AF_LPF_LOW_CUTOFF + AF_LPF_HIGH_CUTOFF)
print(f"AF LO frequency for weaver ssb demodulation is {af_lo} Hz")

# make 1 second of af_lo signal for i and q
i_af_lo = np.cos(2 * np.pi * af_lo * np.arange(0, 1, 1 / AF_SAMPLE_RATE))
q_af_lo = np.sin(2 * np.pi * af_lo * np.arange(0, 1, 1 / AF_SAMPLE_RATE))

# multiply i and q af signals with af_lo signal
i_af_signal_filtered_at_af_sample_rate = i_af_signal_filtered * i_af_lo
q_af_signal_filtered_at_af_sample_rate = q_af_signal_filtered * q_af_lo

# plot i and q af signals
# plt.plot(np.arange(0,1,1/AF_SAMPLE_RATE), i_af_signal_filtered_at_af_sample_rate, label='I')
# plt.plot(np.arange(0,1,1/AF_SAMPLE_RATE), q_af_signal_filtered_at_af_sample_rate, label='Q')
# plt.legend()
# plt.title('I and Q AF Signals after filtering - after second mixer')
# plt.show()

# add i_af_signal_filtered_at_af_sample_rate and q_af_signal_filtered_at_af_sample_rate
af_signal = i_af_signal_filtered_at_af_sample_rate - q_af_signal_filtered_at_af_sample_rate

# fft plot of af_signal
plt.magnitude_spectrum(af_signal, Fs=AF_SAMPLE_RATE, scale='dB')
plt.title('AF Signal Spectrum')
plt.show()

### - END OF THE SOFTWARE PART - ###
