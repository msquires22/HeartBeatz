import pyaudio
import wave
import numpy as np
import threading

# Initial playback speed
speed = 1.0
lock = threading.Lock()

# Open the audio file
song_path = "music/rock/YoureGonnaGoFarKid.wav"
song = wave.open(song_path, 'rb')
sr = song.getframerate()
channels = song.getnchannels()
sampwidth = song.getsampwidth()

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open audio stream
stream = p.open(format=p.get_format_from_width(sampwidth),
                channels=channels,
                rate=sr,
                output=True)

# Function to update playback speed in real-time
def update_speed():
    global speed
    while True:
        try:
            new_speed = float(input("Enter new playback speed (e.g., 1.0 for normal speed): "))
            if new_speed > 0:
                with lock:
                    speed = new_speed
                print(f"Playback speed updated to: {speed}")
        except ValueError:
            print("Invalid input. Please enter a number greater than 0.")

# Start a separate thread to listen for speed updates
threading.Thread(target=update_speed, daemon=True).start()

# Play audio with dynamic resampling
chunk_size = 1024
data = song.readframes(chunk_size)
while data:
    with lock:
        # Convert data to numpy array and adjust playback speed
        audio_data = np.frombuffer(data, dtype=np.int16)
        num_samples = int(len(audio_data) / speed)
        
        # Use resampling to adjust speed without restarting stream
        resampled_data = np.interp(np.linspace(0, len(audio_data), num_samples), np.arange(len(audio_data)), audio_data)
        
        # Write to stream
        stream.write(resampled_data.astype(np.int16).tobytes())
    
    # Read next chunk of data
    data = song.readframes(chunk_size)

# Close the stream after playback
stream.stop_stream()
stream.close()
p.terminate()
