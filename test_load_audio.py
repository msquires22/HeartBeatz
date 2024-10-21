import librosa

# Test loading the audio file
y, sr = librosa.load("BabyElephantWalk60.wav", sr=None)
print(f"Loaded audio file with sample rate: {sr} and {len(y)} samples")
