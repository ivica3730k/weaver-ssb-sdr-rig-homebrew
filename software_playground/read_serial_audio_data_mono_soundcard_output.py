import serial
import numpy as np
import pyaudio
import threading

# Set the sample rate
SAMPLE_RATE = 44100
SERIAL_PORT = "/dev/ttyACM0"  # Update this with your specific port

ser = serial.Serial(SERIAL_PORT)
data_queue = []
data_queue_lock = threading.Lock()

p = pyaudio.PyAudio()

def read_serial_data():
    global data_queue
    while True:
        data = ser.read(2)  # Read the correct number of bytes (2 bytes per sample)
        data_np = np.frombuffer(data, dtype=np.int16)
        data_bytes = data_np.tobytes()
        with data_queue_lock:
            data_queue.extend(data_bytes)

def audio_callback(in_data, frame_count, time_info, status):
    global data_queue
    with data_queue_lock:
        data = data_queue[:frame_count*2]  # Adjust frame_count to bytes
        data_queue = data_queue[frame_count*2:]
    return (bytes(data), pyaudio.paContinue)

def audio_stream():
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=SAMPLE_RATE,
                    output=True,
                    stream_callback=audio_callback)

    stream.start_stream()

    while stream.is_active():
        pass

    stream.stop_stream()
    stream.close()
    p.terminate()

# Create threads
serial_thread = threading.Thread(target=read_serial_data)
audio_thread = threading.Thread(target=audio_stream)

# Start threads
serial_thread.start()
audio_thread.start()

# Wait for threads to finish (join)
serial_thread.join()
audio_thread.join()
