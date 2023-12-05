import numpy as np
import matplotlib.pyplot as plt
import time
import scipy.signal as sig
from fir_filter_lpf_2400hz import filter_taps as fir_filter_lpf_2400hz_taps

# Parameters
sample_rate = 22050  # Hz
duration = 1  # seconds

# Generate time values
t = np.arange(0, duration, 1/sample_rate)

# Generate sine waves
sinewave = np.sin(2 * np.pi * 1000 * t)  \
    + np.sin(2 * np.pi * 1700 * t) \
    + np.sin(2 * np.pi * 3300 * t)

# create the fir low pass filter with a cutoff frequency of 2.4 kHz
#fir_filter = sig.firwin(563, 2400, fs=sample_rate)

filtered_sinewave = sig.lfilter(fir_filter_lpf_2400hz_taps, 1.0, sinewave)

# Create subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))

# Plot the sine waves
ax1.plot(t, sinewave, label='Combined')
ax1.plot(t, filtered_sinewave, label='Filtered')
# ax1.set_xlim(0, 4/1000)
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Amplitude')
ax1.legend()

# Plot the FFT of the filtered signal
ax2.magnitude_spectrum(filtered_sinewave, Fs=sample_rate, scale='dB')
ax2.set_xlim(0, 5000)
ax2.set_ylim(-100, 0)
ax2.set_xlabel('Frequency (Hz)')
ax2.set_ylabel('Magnitude (dB)')

# Adjust layout for better spacing
plt.tight_layout()

# Show the combined plot
plt.show()
