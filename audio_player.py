# audio_player.py
import pyaudio
import wave
import numpy as np
import threading

# Playback speed that main.py will modify
speed = 1.0
lock = threading.Lock()

def set_playback_speed(new_speed):
    """Update playback speed."""
    global speed
    with lock:
        speed = new_speed# audio_player.py
import pyaudio
import wave
import numpy as np
import threading

# Playback speed that main.py will modify
speed = 1.0
lock = threading.Lock()

def set_playback_speed(new_speed):
    """Update playback speed."""
    global speed
    with lock:
        speed = new_speed

# Function to play the song with real-time tempo adjustment
def play_song(song_path):
    # Open the audio file
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
    song.close()
    stream.stop_stream()
    stream.close()
    p.terminate()

# Function to play the song with real-time tempo adjustment
def play_song(song_path):
    # Open the audio file
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
    song.close()
    stream.stop_stream()
    stream.close()
    p.terminate()
