import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig

# Radio Frequency (RF) parameters
RF_SAMPLE_RATE = 1e6
RF_CARRIER = 1e5
MODE = "USB"
CHECK_SIDEBAND_REJECTION = False

# Generate 1 second of noise on RF_SAMPLE_RATE with amplitude 0.1
noise = np.random.normal(0, 0.25, int(RF_SAMPLE_RATE))
rf_signal = noise

# Modulate noise with sinusoidal components based on the selected mode (USB or LSB)
for i in range(0, 3000, 10):
    if MODE.upper() == "USB":
        if CHECK_SIDEBAND_REJECTION:
            rf_signal = rf_signal + np.sin(
                2 * np.pi * (RF_CARRIER - i) * np.arange(0, 1, 1 / RF_SAMPLE_RATE)
            )
        else:
            rf_signal = rf_signal + np.sin(
                2 * np.pi * (RF_CARRIER + i) * np.arange(0, 1, 1 / RF_SAMPLE_RATE)
            )
    elif MODE.upper() == "LSB":
        if CHECK_SIDEBAND_REJECTION:
            rf_signal = rf_signal + np.sin(
                2 * np.pi * (RF_CARRIER + i) * np.arange(0, 1, 1 / RF_SAMPLE_RATE)
            )
        else:
            rf_signal = rf_signal - np.sin(
                2 * np.pi * (RF_CARRIER + i) * np.arange(0, 1, 1 / RF_SAMPLE_RATE)
            )
    else:
        assert False, "MODE must be USB or LSB"

# Resample the RF signal to RF_SAMPLE_RATE
rf_signal = sig.resample(rf_signal, int(RF_SAMPLE_RATE))

# Plot the magnitude spectrum of the RF signal
plt.magnitude_spectrum(rf_signal, Fs=RF_SAMPLE_RATE, scale="dB")
plt.title("RF Signal Spectrum")
plt.show()

# Import filter parameters from an external module
from weaver_filter_bpf_1100hz_1800hz import filter

# Filter parameters
FILTER = filter
AF_SAMPLE_RATE = FILTER.SAMPLE_RATE
AF_LPF_LOW_CUTOFF = FILTER.LPF_LOW_CUTOFF
AF_LPF_HIGH_CUTOFF = FILTER.LPF_HIGH_CUTOFF

print(f"AF Sample Rate is {AF_SAMPLE_RATE} Hz")
print(f"AF Low Pass Filter Low Cutoff is {AF_LPF_LOW_CUTOFF} Hz")
print(f"AF Low Pass Filter High Cutoff is {AF_LPF_HIGH_CUTOFF} Hz")

# Calculate LO frequency for Weaver SSB demodulation
if MODE.upper() == "USB":
    rf_lo = RF_CARRIER + 0.5 * (AF_LPF_LOW_CUTOFF + AF_LPF_HIGH_CUTOFF)
elif MODE.upper() == "LSB":
    rf_lo = RF_CARRIER - 0.5 * (AF_LPF_LOW_CUTOFF + AF_LPF_HIGH_CUTOFF)
else:
    assert False, "MODE must be USB or LSB"

print(f"RF LO frequency for Weaver SSB demodulation is {rf_lo} Hz")

# Generate 1 second of RF LO signal for in-phase (I) and quadrature (Q)
i_rf_lo = np.cos(2 * np.pi * rf_lo * np.arange(0, 1, 1 / RF_SAMPLE_RATE))
q_rf_lo = np.sin(2 * np.pi * rf_lo * np.arange(0, 1, 1 / RF_SAMPLE_RATE))

# Multiply RF signal with LO signal
i_rf_signal_at_rf_sample_rate = rf_signal * i_rf_lo
q_rf_signal_at_rf_sample_rate = rf_signal * q_rf_lo

### - END OF EMULATED HARDWARE PART - ###
### - START OF THE SOFTWARE PART - ###

# Resample I and Q signals to AF_SAMPLE_RATE (emulating ADC read)
i_af_signal = sig.resample(i_rf_signal_at_rf_sample_rate, int(AF_SAMPLE_RATE))
q_af_signal = sig.resample(q_rf_signal_at_rf_sample_rate, int(AF_SAMPLE_RATE))

# Filter I and Q signals with Weaver filter
i_af_signal_filtered = sig.lfilter(FILTER.FILTER_TAPS, 1.0, i_af_signal)
q_af_signal_filtered = sig.lfilter(FILTER.FILTER_TAPS, 1.0, q_af_signal)

af_lo = 0.5 * (AF_LPF_LOW_CUTOFF + AF_LPF_HIGH_CUTOFF)
print(f"AF LO frequency for Weaver SSB demodulation is {af_lo} Hz")

# Generate 1 second of AF LO signal for in-phase (I) and quadrature (Q)
i_af_lo = np.cos(2 * np.pi * af_lo * np.arange(0, 1, 1 / AF_SAMPLE_RATE))
q_af_lo = np.sin(2 * np.pi * af_lo * np.arange(0, 1, 1 / AF_SAMPLE_RATE))

# Multiply I and Q AF signals with AF LO signal
i_af_signal_filtered_at_af_sample_rate = i_af_signal_filtered * i_af_lo
q_af_signal_filtered_at_af_sample_rate = q_af_signal_filtered * q_af_lo

# Add I and Q AF signals
if MODE.upper() == "USB":
    af_signal = (
        i_af_signal_filtered_at_af_sample_rate + q_af_signal_filtered_at_af_sample_rate
    )
elif MODE.upper() == "LSB":
    af_signal = (
        i_af_signal_filtered_at_af_sample_rate - q_af_signal_filtered_at_af_sample_rate
    )
else:
    assert False, "MODE must be USB or LSB"

# Plot the magnitude spectrum of AF signal and filtered AF signal on the same plot
plt.magnitude_spectrum(af_signal, Fs=AF_SAMPLE_RATE, scale="dB", color="blue")
plt.title("AF Signal Spectrum")
plt.show()

### - END OF THE SOFTWARE PART - ###
