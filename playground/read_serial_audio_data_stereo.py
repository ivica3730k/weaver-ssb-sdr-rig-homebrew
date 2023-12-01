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
data_list_i = []
data_list_q = []
while len(data_list_i) < SAMPLE_RATE:
    
    two_bytes = ser.read(2)
    byte_val_i = two_bytes[0]
    byte_val_q = two_bytes[1]
    # for some reasons they are already integers
    data_list_i.append(byte_val_i)
    data_list_q.append(byte_val_q)


# Close the serial port
ser.close()

# Normalize the values to the range [-1, 1]
normalized_data_i = [(value - 127.5) / 127.5 for value in data_list_i]
normalized_data_q = [(value - 127.5) / 127.5 for value in data_list_q]

# Convert to a numpy array
data_array_i = np.array(normalized_data_i)
data_array_q = np.array(normalized_data_q)

# FFT plot of both signals
plt.magnitude_spectrum(data_array_i, Fs=SAMPLE_RATE, scale="dB")
plt.magnitude_spectrum(data_array_q, Fs=SAMPLE_RATE, scale="dB")
plt.title("AF Signal Spectrum")
plt.show()


# plot the wave just like oscilloscope, label the axis
plt.plot(data_array_i, label="I")
plt.plot(data_array_q, label="Q")
plt.title("AF Signal Waveform")
plt.xlabel("Time (samples)")
plt.ylabel("Amplitude")
plt.legend()
plt.show()