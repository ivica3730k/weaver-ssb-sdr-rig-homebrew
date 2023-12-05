import serial
import numpy as np
import pyaudio
import threading
import struct
from queue import Queue
from time import sleep

# Set the sample rate
SAMPLE_RATE = 44100
CHUNK_SIZE = 512
SERIAL_PORT = "/dev/ttyACM0"  # Update this with your specific port

ser = serial.Serial(SERIAL_PORT)
data_queue = Queue()

p = pyaudio.PyAudio()

def read_serial_data():
    global data_queue
    while True:
        # Read multiple chunks of data
        chunks = [ser.read(2) for _ in range(CHUNK_SIZE)]
        data = b''.join(chunks)
        data_queue.put(data)

def audio_callback(in_data, frame_count, time_info, status):
    global data_queue
    data = b''.join([data_queue.get() for _ in range(frame_count)])
    return (data, pyaudio.paContinue)

def audio_stream():
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=SAMPLE_RATE,
        output=True,
        stream_callback=audio_callback,
    )

    stream.start_stream()

    while stream.is_active():
        sleep(0.01)  # Adjust sleep time if needed

    stream.stop_stream()
    stream.close()
    p.terminate()

# Create threads
serial_thread = threading.Thread(target=read_serial_data)
audio_thread = threading.Thread(target=audio_stream)

# Start threads
audio_thread.start()
serial_thread.start()

# Wait for threads to finish (join)
audio_thread.join()
serial_thread.join()
