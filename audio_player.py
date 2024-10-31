# audio_player.py
import pyaudio
import wave
import numpy as np
import threading
import time

lock = threading.Lock()
speed = 1.0  # Initial playback speed

# Initialize PyAudio
p = pyaudio.PyAudio()
stream = None  # We'll open this in the function

def set_playback_speed(new_speed):
    """Set the playback speed."""
    global speed
    with lock:
        speed = new_speed
    print(f"Playback speed updated to: {speed}")

def play_song_with_heart_rate_control(song_path, get_current_heart_rate, heart_rate_zones, time_intervals):
    """
    Play a song with real-time tempo adjustment based on heart rate zones.
    
    Args:
        song_path (str): Path to the audio file.
        get_current_heart_rate (function): Function to get current heart rate from main.
        heart_rate_zones (dict): Dictionary with min and max HR for warmup, high, and low intensity.
        time_intervals (list): List of tuples defining the time and corresponding heart rate zones.
    """
    global stream

    # Open the audio file
    song = wave.open(song_path, 'rb')
    sr = song.getframerate()
    channels = song.getnchannels()
    sampwidth = song.getsampwidth()

    # Initialize audio stream if not already open
    stream = p.open(format=p.get_format_from_width(sampwidth),
                    channels=channels,
                    rate=sr,
                    output=True)

    # Get the start time to track time intervals
    start_time = time.time()

    for duration, zone in time_intervals:
        print(f"Targeting zone: {zone} for the next {duration} seconds.")

        end_time = start_time + duration
        while time.time() < end_time:
            current_hr = get_current_heart_rate()
            zone_min, zone_max = heart_rate_zones[zone]

            # Adjust speed based on heart rate and target zone
            if current_hr < zone_min:
                set_playback_speed(1.2)  # Increase speed to motivate
            elif current_hr > zone_max:
                set_playback_speed(0.8)  # Decrease speed to slow down
            else:
                set_playback_speed(1.0)  # Normal speed in target zone

            # Play audio with dynamic resampling
            chunk_size = 1024
            data = song.readframes(chunk_size)
            while data and time.time() < end_time:
                with lock:
                    audio_data = np.frombuffer(data, dtype=np.int16)
                    num_samples = int(len(audio_data) / speed)
                    resampled_data = np.interp(np.linspace(0, len(audio_data), num_samples), np.arange(len(audio_data)), audio_data)
                    stream.write(resampled_data.astype(np.int16).tobytes())
                data = song.readframes(chunk_size)

            time.sleep(1)  # Poll heart rate every second

    # Close the song and stream after playback
    song.close()
    stream.stop_stream()
    stream.close()
    p.terminate()
