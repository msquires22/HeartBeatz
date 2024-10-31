import pyaudio
import wave
import numpy as np
import threading

# Initial playback speed
speed = 1.0
lock = threading.Lock()  # Lock to manage safe access to stream

# Open the audio file
song_path = "music/pop/Closer.wav"  # Replace with your actual file path
song = wave.open(song_path, 'rb')
sr = song.getframerate()
channels = song.getnchannels()
sampwidth = song.getsampwidth()

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open the audio stream with initial playback speed
stream = p.open(format=p.get_format_from_width(sampwidth),
                channels=channels,
                rate=int(sr * speed),
                output=True)

# Function to update playback speed in real-time
def update_speed():
    global speed, stream
    while True:
        try:
            new_speed = float(input("Enter new playback speed (e.g., 1.0 for normal speed): "))
            if new_speed > 0:
                with lock:
                    speed = new_speed
                    # Close and reopen the stream safely
                    stream.close()
                    stream = p.open(format=p.get_format_from_width(sampwidth),
                                    channels=channels,
                                    rate=int(sr * speed),
                                    output=True)
                print(f"Playback speed updated to: {speed}")
        except ValueError:
            print("Invalid input. Please enter a number greater than 0.")

# Start a separate thread for updating speed
threading.Thread(target=update_speed, daemon=True).start()

# Play the audio
chunk_size = 1024
data = song.readframes(chunk_size)
while data:
    with lock:
        # Convert data to numpy array and adjust playback speed
        audio_data = np.frombuffer(data, dtype=np.int16)
        num_samples = int(len(audio_data) / speed)
        resampled_data = np.interp(np.linspace(0, len(audio_data), num_samples), np.arange(len(audio_data)), audio_data)
        
        # Write to stream
        stream.write(resampled_data.astype(np.int16).tobytes())
    
    # Read next chunk of data
    data = song.readframes(chunk_size)

# Close stream and PyAudio
stream.stop_stream()
stream.close()
p.terminate()
