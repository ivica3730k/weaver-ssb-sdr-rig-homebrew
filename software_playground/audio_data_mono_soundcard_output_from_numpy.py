import numpy as np
import pyaudio
import threading

# Set the sample rate
SAMPLE_RATE = 44100

sinewave = np.array([int(4096 * np.sin(2 * np.pi * 1000 * x / SAMPLE_RATE)) for x in range(SAMPLE_RATE)], dtype=np.int16)

# Convert to Python list
sinewave_bytes = sinewave.tobytes()

p = pyaudio.PyAudio()

def audio_callback(in_data, frame_count, time_info, status):
    global sinewave_bytes
    data = sinewave_bytes[:frame_count*2]  # Adjust frame_count to bytes
    sinewave_bytes = sinewave_bytes[frame_count*2:]
    return (data, pyaudio.paContinue)

def audio_stream():
    global sinewave_bytes
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=SAMPLE_RATE,
        output=True,
        stream_callback=audio_callback
    )

    stream.start_stream()

    while stream.is_active():
        pass

    stream.stop_stream()
    stream.close()
    p.terminate()

# Create threads
audio_thread = threading.Thread(target=audio_stream)

# Start threads
audio_thread.start()

# Wait for threads to finish (join)
audio_thread.join()
