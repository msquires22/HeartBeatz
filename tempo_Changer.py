import pyaudio
import wave
import sys

# Open the wave file
song = wave.open("music/closer.wav", "rb")

# Instantiate PyAudio
p = pyaudio.PyAudio()

# Define initial playback speed
speed = 1.0


# Define callback function to stream the song
def callback(in_data, frame_count, time_info, status):
    global speed

    # Read in more or fewer frames based on speed
    frames_to_read = int(frame_count * speed)
    data = song.readframes(frames_to_read)

    # If end of song is reached, stop playback
    if data == b'':
        return None, pyaudio.paComplete

    # If speed is less than 1, add zeros to slow down playback
    if speed < 1.0:
        data += b'\x00' * (frame_count - frames_to_read) * song.getsampwidth() * song.getnchannels()

    return data, pyaudio.paContinue


# Open a stream and start playing the song
stream = p.open(format=p.get_format_from_width(song.getsampwidth()),
                channels=song.getnchannels(),
                rate=song.getframerate(),
                output=True,
                stream_callback=callback)

stream.start_stream()

# Allow user to input speed changes during playback
while stream.is_active():
    try:
        # Read user input
        speed_input = input("Enter speed (1.0 = normal speed): ")
        # Convert input to float
        speed = float(speed_input)
    except KeyboardInterrupt:
        # If user interrupts with Ctrl+C, stop playback
        stream.stop_stream()
        stream.close()
        song.close()
        p.terminate()
        sys.exit()

# Stop and close the stream and PyAudio
stream.stop_stream()
stream.close()
song.close()
p.terminate()


#from https://stackoverflow.com/questions/75504433/changing-speed-of-song-while-its-playing-and-have-the-changed-effects-in-the-son