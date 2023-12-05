import serial
import time

# Set the sample rate
SAMPLE_RATE = 44100
# Set the serial port and baud rate
SERIAL_PORT = "/dev/ttyACM0"  # Update this with your specific port

# Open the serial port
ser = serial.Serial(SERIAL_PORT)

# Read data from the serial port until SAMPLE_RATE samples are collected
data_list = []

time_1 = time.time_ns()
while len(data_list) < SAMPLE_RATE:
    byte_val = ser.read(2)
    int_val = int.from_bytes(byte_val, byteorder='big')
    data_list.append(int_val)
time_2 = time.time_ns()

# Close the serial port

# Calculate the time taken in nanoseconds
time_taken_ns = time_2 - time_1

print(f"Time taken to read {SAMPLE_RATE} samples: {time_taken_ns} nanoseconds")
print(f"Time taken to read {SAMPLE_RATE} samples: {time_taken_ns / 1e9} seconds")

