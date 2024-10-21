import librosa
import sounddevice as sd
import numpy as np
import threading

# Load the audio file (make sure the correct path is used)
y, sr = librosa.load("closer.wav", sr=None)

# Set the initial tempo change (1.0 means no change)
tempo_change = 1.0
current_idx = 0
chunk_size = 1024  # Number of frames to process at a time

def adjust_tempo(new_tempo):
    """
    Adjusts the tempo dynamically.
    new_tempo: The new tempo factor (e.g., 1.2 for 20% faster, 0.8 for 20% slower)
    """
    global tempo_change
    tempo_change = new_tempo
    print(f"Tempo adjusted to: {tempo_change}")

def audio_callback(outdata, frames, time, status):
    global current_idx, tempo_change, y
    
    # Get the current chunk of audio
    chunk = y[current_idx:current_idx + frames]

    # If we're at the end of the file, pad with zeros
    if len(chunk) < frames:
        chunk = np.pad(chunk, (0, frames - len(chunk)))

    # Apply time-stretching to adjust tempo without changing pitch
    stretched_chunk = librosa.effects.time_stretch(chunk, rate=tempo_change)

    # If the stretched chunk is smaller than the frames, pad with zeros
    if len(stretched_chunk) < frames:
        stretched_chunk = np.pad(stretched_chunk, (0, frames - len(stretched_chunk)))

    # Ensure the buffer matches the frame size and send the data
    outdata[:frames] = stretched_chunk[:frames].reshape(-1, 1)

    # Update the current index to move to the next chunk of audioß
    current_idx += frames
    if current_idx >= len(y):  # Stop if we reach the end of the file
        print("Reached the end of the audio, stopping playback.")
        raise sd.CallbackStop()


# Function to play the audio with dynamic tempo adjustment
def play_audio():
    with sd.OutputStream(samplerate=sr, channels=1, callback=audio_callback):
        print("Playing... Use the terminal to change tempo dynamically.")
        sd.sleep(int(len(y) / sr * 1000))  # Wait for the duration of the audio

# Thread for handling audio playback
def audio_thread():
    play_audio()

# Function to handle user input for changing the tempo
def input_thread():
    while True:
        try:
            new_tempo = float(input("Enter new tempo (e.g., 1.0 for normal speed, 1.5 for 50% faster): "))
            adjust_tempo(new_tempo)
        except ValueError:
            print("Invalid input. Please enter a number.")

# Start audio in a separate thread
threading.Thread(target=audio_thread).start()

# Start input handling in the main thread
input_thread()
