import serial
import numpy as np
import pyaudio
from time import sleep

# Set the sample rate
SAMPLE_RATE = 11025
# Set the serial port and baud rate
SERIAL_PORT = "/dev/ttyACM1"  # Update this with your specific port
BAUD_RATE = 250000
FRAMES_PER_BUFFER = 1000
# Set up PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,  # Change the format to int16
                channels=2,  # Use 2 channels for stereo
                rate=SAMPLE_RATE,
                output=True,
                frames_per_buffer=FRAMES_PER_BUFFER)

# Open the serial port
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
sleep(2)  # Wait for the serial port to be ready

while True:
    samples = ser.read(FRAMES_PER_BUFFER * 2)  # Read the correct number of bytes (2 bytes per sample)
    # Convert bytes to NumPy array of int16
    samples_np = np.frombuffer(samples, dtype=np.int16)
    # Split the samples into left and right channels
    left_channel = samples_np[::2]
    right_channel = samples_np[1::2]
    # Interleave the left and right channels
    interleaved_samples = np.column_stack((left_channel, right_channel)).flatten()
    # Write the interleaved samples to the sound card
    stream.write(interleaved_samples.tobytes())
