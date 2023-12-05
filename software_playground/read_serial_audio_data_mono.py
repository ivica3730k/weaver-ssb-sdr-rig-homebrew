import serial
import numpy as np
import matplotlib.pyplot as plt

# Set the sample rate
SAMPLE_RATE = 22050
# Set the serial port and baud rate
SERIAL_PORT = "/dev/ttyACM0"  # Update this with your specific port
BAUD_RATE = 250000

# Open the serial port
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)

# Read data from the serial port until SAMPLE_RATE samples are collected
data_list = []
while len(data_list) < SAMPLE_RATE:
    byte_val = ser.read(1)
    int_val = int.from_bytes(byte_val, byteorder='big')
    data_list.append(int_val)

# Close the serial port
ser.close()

# Normalize the values to the range [-1, 1]
normalized_data = [(value - 127.5) / 127.5 for value in data_list]

# Convert to a numpy array
data_array = np.array(normalized_data)

# FFT plot of the signal
plt.magnitude_spectrum(data_array, Fs=SAMPLE_RATE, scale="dB")
plt.title("AF Signal Spectrum")
plt.show()

# plot the wave just like oscilloscope
plt.plot(data_array)
plt.title("AF Signal Waveform")
plt.show()