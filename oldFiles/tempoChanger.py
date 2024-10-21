import sounddevice as sd
import librosa
import numpy as np
import time

# Load audio file using librosa
y, sr = librosa.load("/Users/mikeysquires/Documents/FALL 2025/COS 436/HeartBeatz/BabyElephantWalk60.wav", sr=None)

# Initial tempo change factor (1.0 means normal speed)
tempo_change = 1.0

# This will store the position in the audio array
current_idx = 0
chunk_size = 512  # Number of frames to process at a time


def adjust_tempo(new_tempo):
    """
    This function adjusts the tempo dynamically.
    new_tempo: The new tempo factor (e.g., 1.2 for 20% faster, 0.8 for 20% slower)
    """
    global tempo_change
    tempo_change = new_tempo
    print(f"Tempo adjusted to: {tempo_change}")


# Define callback function to process audio in real-time
def audio_callback(outdata, frames, time, status):
    global current_idx, tempo_change, y
    
    # Get a chunk of the audio data
    chunk = y[current_idx:current_idx + chunk_size]
    
    # Apply time-stretching to adjust tempo without changing pitch
    stretched_chunk = librosa.effects.time_stretch(chunk, tempo_change)
    
    # If the processed chunk is smaller than the buffer, pad it with zeros
    if len(stretched_chunk) < frames:
        outdata[:len(stretched_chunk)] = stretched_chunk.reshape(-1, 1)
        outdata[len(stretched_chunk):] = 0  # Fill the remaining buffer with silence
    else:
        outdata[:] = stretched_chunk[:frames].reshape(-1, 1)

    # Update the current index to move to the next chunk of audio
    current_idx += chunk_size
    if current_idx >= len(y):  # Loop the audio if we reach the end
        current_idx = 0


# Function to handle playback with dynamic tempo adjustments
def play_audio():
    with sd.OutputStream(samplerate=sr, channels=1, callback=audio_callback):
        print("Playing... Use adjust_tempo(new_tempo) to change the speed dynamically.")
        sd.sleep(len(y) // sr * 1000)  # Keep the stream open for the duration of the audio


# Start the audio playback
play_audio()

# Wait 5 seconds and then change the tempo
time.sleep(5)
adjust_tempo(1.5)  # Speed up by 50%

# Wait another 5 seconds and slow it down
time.sleep(5)
adjust_tempo(0.75)  # Slow down by 25%

# Example of dynamically adjusting the tempo while playing:
# adjust_tempo(1.5)  # Speeds up the playback by 50%
# adjust_tempo(0.75)  # Slows down the playback by 25%
