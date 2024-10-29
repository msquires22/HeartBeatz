#imports
import pyaudio
import wave
import sys
import csv
import time

# Open the wave file
song = wave.open("music/closer.wav", "rb")
# Instantiate PyAudio
p = pyaudio.PyAudio()
# Define initial playback speed
speed = 1.0

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
minTHRZ_HI = int(maxHR * .75) # THRZ Min - HII

maxTHRZ_LI = int(maxHR * .75) # Target Heart Rate Zone Max (Low Intensity Interval)
minTHRZ_LI = int(maxHR * .5) # THRZ Min - LII

maxTHRZ_WC = int(maxHR * .5) # Target Heart Rate Zone Max (Warmup/Cooldown)
minTHRZ_WC = int(maxHR * .4) # THRZ Min - WC

#################

#Calls to next song, can do this in prototype #2

#################

print("Tell user to begin warming up")

#fetch heart rate data



song = wave.open("music/nomoney.wav", "rb")
    
 # Instantiate PyAudio
p = pyaudio.PyAudio()

# Define initial playback speed 
speed = 1.3



#let program run for 30 seconds to get HR, detemrine average HR over the last 5 seconds,
#determine the first song and then can get into program 



#some kind of large dyanmic loop which continously plays music, editing tempo based on HR, and
#outputs it to BT

# if heart rate is lower than minimum of warmup zone, increase tempo
def read_heart_rate_from_csv(file_path):
    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        heart_rates = [int(row[0]) for row in csv_reader]
    return heart_rates

def determine_heart_rate_zone(heart_rate, min_thr, max_thr):
    if heart_rate < min_thr:
        return 'below'
    elif heart_rate > max_thr:
        return 'above'
    else:
        return 'within'
 
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

# Example usage
csv_file_path = 'test_hr_data.csv'

# Open a stream and start playing the song
stream = p.open(format=p.get_format_from_width(song.getsampwidth()),
                channels=song.getnchannels(),
                rate=song.getframerate(),
                output=True,
                stream_callback=callback)

stream.start_stream()

while True:
    heart_rates = read_heart_rate_from_csv(csv_file_path)
    if heart_rates:
        current_hr = heart_rates[-1]  # Assuming the latest heart rate is the last entry
        zone = determine_heart_rate_zone(current_hr, minTHRZ_WC, maxTHRZ_WC)
        
        if zone == 'below':
            speed += 0.1  # Increase tempo
        elif zone == 'above':
            speed -= 0.1  # Decrease tempo
        elif zone == 'within':
            speed = 1.3
        print(f"Current heart rate: {current_hr}, Zone: {zone}, Playback speed: {speed}")
    
    time.sleep(5)  # Wait for 5 seconds before reading the heart rate again
