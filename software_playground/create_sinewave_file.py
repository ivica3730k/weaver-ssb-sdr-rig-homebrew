import numpy as np

SAMPLE_RATE = 11025

# Create a sine wave of 1khz with integer values between 0 and 255
# The sine wave will have SAMPLE_RATE samples
sine_wave = np.array([int(255 * np.sin(2 * np.pi * 1000 * x / SAMPLE_RATE)) for x in range(SAMPLE_RATE)])

# Save the sine wave to a cpp file that can be included in the Arduino sketch
with open("sine_wave.h", "w") as f:
    f.write(f"const int sine_wave[] = {{{', '.join([str(x) for x in sine_wave])}}};")

    