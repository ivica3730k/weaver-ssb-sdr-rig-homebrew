import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig

# Importing filter parameters from an external module
# from weaver_filter_bpf_1100hz_1800hz import filter
from weaver_filter_lpf_1100hz import filter

# Audio Frequency (AF) sample rate based on imported filter
AF_SAMPLE_RATE = filter.SAMPLE_RATE

# Generate AF noise and create an AF signal with sinusoidal components
af_noise = np.random.normal(0, 0.10, int(AF_SAMPLE_RATE))
af_signal = af_noise

# add a sigle tone at 550 Hz
af_signal = af_signal + np.sin(2 * np.pi * 550 * np.arange(0, 1, 1 / AF_SAMPLE_RATE))

# # Add sinusoidal components to simulate AF signal
# for i in range(0, 3000, 10):
#     af_signal = af_signal + np.sin(2 * np.pi * i * np.arange(0, 1, 1 / AF_SAMPLE_RATE))

# Resample the AF signal to the specified AF sample rate
af_signal = sig.resample(af_signal, int(AF_SAMPLE_RATE))

# Plot the magnitude spectrum of the AF signal
plt.magnitude_spectrum(af_signal, Fs=AF_SAMPLE_RATE, scale="dB")
plt.title("AF Signal Spectrum")
plt.show()

# Low Pass Filter (LPF) parameters
AF_LPF_LOW_CUTOFF = filter.LPF_LOW_CUTOFF
AF_LPF_HIGH_CUTOFF = filter.LPF_HIGH_CUTOFF

# Calculate the center frequency of AF LPF
af_lo = 0.5 * (AF_LPF_LOW_CUTOFF + AF_LPF_HIGH_CUTOFF)

# Generate in-phase (I) and quadrature (Q) components of AF LO
i_af_lo = sig.resample(
    np.cos(2 * np.pi * af_lo * np.arange(0, 1, 1 / AF_SAMPLE_RATE)), int(AF_SAMPLE_RATE)
)
q_af_lo = sig.resample(
    np.sin(2 * np.pi * af_lo * np.arange(0, 1, 1 / AF_SAMPLE_RATE)), int(AF_SAMPLE_RATE)
)

# # Plot I and Q components of AF LO
# plt.title("I and Q AF LO")
# plt.plot(i_af_lo, label="I AF LO")
# plt.plot(q_af_lo, label="Q AF LO")
# plt.legend()
# plt.show()

# Modulate AF signal with AF LO
i_af_signal_at_af_sample_rate = af_signal * i_af_lo
q_af_signal_at_af_sample_rate = af_signal * q_af_lo

# Filter modulated signals with the Weaver filter
i_af_signal_at_af_sample_rate_filtered = sig.lfilter(
    filter.FILTER_TAPS, 1.0, i_af_signal_at_af_sample_rate
)
q_af_signal_at_af_sample_rate_filtered = sig.lfilter(
    filter.FILTER_TAPS, 1.0, q_af_signal_at_af_sample_rate
)


# # Plot filtered I and Q components of AF signal
# plt.title("I and Q AF Signal Filtered")
# plt.plot(i_af_signal_at_af_sample_rate, label="I AF Signal")
# plt.plot(q_af_signal_at_af_sample_rate, label="Q AF Signal")
# plt.plot(i_af_signal_at_af_sample_rate_filtered, label="I AF Signal Filtered")
# plt.plot(q_af_signal_at_af_sample_rate_filtered, label="Q AF Signal Filtered")
# plt.legend()
# plt.show()

# Radio Frequency (RF) parameters
RF_SAMPLE_RATE = 1e6
RF_CARRIER = 1e5
MODE = "LSB"

### END OF THE SOFTWARE PART ###
### START OF THE EMULATED HARDWARE PART ###

# Resample filtered signals to RF sample rate (emulating DAC write)
i_af_signal_at_rf_sample_rate = sig.resample(
    i_af_signal_at_af_sample_rate_filtered, int(RF_SAMPLE_RATE)
)
q_af_signal_at_rf_sample_rate = sig.resample(
    q_af_signal_at_af_sample_rate_filtered, int(RF_SAMPLE_RATE)
)

# Determine the frequency of RF LO based on the selected mode
if MODE.upper() == "USB":
    rf_lo = RF_CARRIER + af_lo
elif MODE.upper() == "LSB":
    rf_lo = RF_CARRIER - af_lo
else:
    assert False, "MODE must be USB or LSB"

# Generate I and Q components of RF LO
i_rf_lo = np.cos(2 * np.pi * rf_lo * np.arange(0, 1, 1 / RF_SAMPLE_RATE))
q_rf_lo = np.sin(2 * np.pi * rf_lo * np.arange(0, 1, 1 / RF_SAMPLE_RATE))

# Modulate signals to RF
i_rf_signal_at_rf_sample_rate = i_af_signal_at_rf_sample_rate * i_rf_lo
q_rf_signal_at_rf_sample_rate = q_af_signal_at_rf_sample_rate * q_rf_lo

# Combine I and Q signals based on the selected mode
if MODE.upper() == "USB":
    rf_signal = i_rf_signal_at_rf_sample_rate + q_rf_signal_at_rf_sample_rate
elif MODE.upper() == "LSB":
    rf_signal = i_rf_signal_at_rf_sample_rate - q_rf_signal_at_rf_sample_rate

# Plot the magnitude spectrum of the RF signal
plt.magnitude_spectrum(rf_signal, Fs=RF_SAMPLE_RATE, scale="dB")
plt.title("RF Signal Spectrum")
plt.show()
