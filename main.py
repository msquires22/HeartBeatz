#imports
import pyaudio
import wave
import sys

# Input age and genre choice
age = int(input("Enter user's age: "))
print(f"User's age is: {age}")

genres = {1: 'Country', 2: 'Pop', 3: 'Rock', 4: 'Rap', 5: 'Electronic Dance'}
choice = int(input(f"User's preferred genre: {', '.join(f'{k}. {v}' for k, v in genres.items())}: "))
print(f"User's preferred genre is: {genres.get(choice, 'Invalid choice')}")

# Calculate Ranges for HR
maxHR = int(191.5 - .007 * age**2) # max heart rate
print(f"Users max heart rate is: {maxHR}")

maxTHRZ_HI = int(maxHR * .9) # Target Heart Rate Zone Max (High Intensity Interval)
minTHRZ_HI = int(maxHR * .85) # THRZ Min - HII

maxTHRZ_LI = int(maxHR * .75) # Target Heart Rate Zone Max (Low Intensity Interval)
minTHRZ_LI = int(maxHR * .65) # THRZ Min - LII

maxTHRZ_WC = int(maxHR * .7) # Target Heart Rate Zone Max (Warmup/Cooldown)
minTHRZ_WC = int(maxHR * .6) # THRZ Min - WC

#################

#Calls to next song, can do this in prototype #2

#################

print("Tell user to begin warming up")

#fetch heart rate data


songs = {"music/nomoney.wav", "music/titanium.wav", "music/closer.wav"}

for file in songs:
    song = wave.open(file, "rb")
    
    # Instantiate PyAudio
    p = pyaudio.PyAudio()

    # Define initial playback speed 
    speed = 1.0






#let program run for 30 seconds to get HR, detemrine average HR over the last 5 seconds,
#determine the first song and then can get into program 


#some kind of large dyanmic loop which continously plays music, editing tempo based on HR, and
#outputs it to BT