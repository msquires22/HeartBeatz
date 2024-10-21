import numpy as np
import sounddevice as sd

# Generate a 2-second sine wave at 440 Hz
duration = 2.0  # seconds
frequency = 440.0  # Hz (A4 note)
sample_rate = 44100  # Samples per second

t = np.linspace(0, duration, int(sample_rate * duration), False)
audio = np.sin(2 * np.pi * frequency * t)

# Play the sine wave
sd.play(audio, samplerate=sample_rate)
sd.wait()  # Wait until the sound is finished playing
