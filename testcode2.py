import pyaudio
import wave
import sys
import librosa
import numpy as np

# Open the wave file using librosa to load it as a numpy array
filename = "closer.wav"
y, sr = librosa.load(filename, sr=None)

# Instantiate PyAudio
p = pyaudio.PyAudio()

# Define initial playback speed
speed = 1.0
current_idx = 0
chunk_size = 1024  # How much audio we read per cycle


# Define callback function to stream the song
def callback(in_data, frame_count, time_info, status):
    global speed, current_idx

    # Extract the audio chunk
    chunk = y[current_idx:current_idx + chunk_size]

    # If the chunk is too short (end of file), pad with zeros
    if len(chunk) < chunk_size:
        chunk = np.pad(chunk, (0, chunk_size - len(chunk)), mode='constant')

    # Time-stretch the chunk using librosa without changing the pitch
    stretched_chunk = librosa.effects.time_stretch(chunk, speed)

    # Convert to raw data to play
    data = np.float32(stretched_chunk).tobytes()

    # Update current index
    current_idx += chunk_size

    # If we've reached the end of the song, stop playback
    if current_idx >= len(y):
        return data, pyaudio.paComplete

    return data, pyaudio.paContinue


# Open a stream and start playing the song
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=sr,
                output=True,
                stream_callback=callback)

stream.start_stream()

# Allow user to input speed changes during playback
try:
    while stream.is_active():
        speed_input = input("Enter speed (1.0 = normal speed): ")
        speed = float(speed_input)
except KeyboardInterrupt:
    stream.stop_stream()
    stream.close()
    p.terminate()
    sys.exit()

# Stop and close the stream and PyAudio
stream.stop_stream()
stream.close()
p.terminate()
