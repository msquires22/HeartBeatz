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
        
# Custom resampling function
def custom_resample(audio_data, speed):
    # Generate new indices based on speed factor
    indices = np.arange(0, len(audio_data), speed)
    # Use linear interpolation to resample
    resampled_data = np.interp(indices, np.arange(len(audio_data)), audio_data)
    return resampled_data

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
    chunk_size = 2048  # Adjusted chunk size for smoother real-time playback
    data = song.readframes(chunk_size)
    while data:
        with lock:
            # Convert data to numpy array
            audio_data = np.frombuffer(data, dtype=np.int16)
            
            # Use custom resampling function
            resampled_data = custom_resample(audio_data, speed)
            
            # Write to stream
            stream.write(resampled_data.astype(np.int16).tobytes())
        
        # Read next chunk of data
        data = song.readframes(chunk_size)

    # Close the stream after playback
    song.close()
    stream.stop_stream()
    stream.close()
    p.terminate()
    
#made with assistance of ChatGPT: https://chatgpt.com/share/6722839a-fad4-800f-933a-1552d8787364
#https://chatgpt.com/share/6734d108-5bb4-800f-99f2-2f2616ff9e40