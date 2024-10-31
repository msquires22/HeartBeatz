#region IMPORTS
import threading
import time
from audio_player import play_song, set_playback_speed
from songLists import country, electronicDance, pop, rap, rock
#endregion

#region INPUTS
# Input age and genre choice
age = int(input("Enter user's age: "))

# Map user choices to playlists
genres = {
    1: country,
    2: pop,
    3: rock,
    4: rap,
    5: electronicDance
}

# Get user input and assign the chosen playlist
choice = int(input("User's preferred genre: 1. Country, 2. Pop, 3. Rock, 4. Rap, 5. Electronic Dance: "))
playlist = genres.get(choice)
#endregion

#region CALCULATE RANGES
# Calculate Ranges for HR based on age
maxHR = int(191.5 - .007 * age**2)  # max heart rate
heart_rate_zones = {
    "warmup": (int(maxHR * 0.4), int(maxHR * 0.5)),
    "high": (int(maxHR * 0.75), int(maxHR * 0.9)),
    "low": (int(maxHR * 0.5), int(maxHR * 0.75))
}

# Define time intervals for each zone (in seconds)
time_intervals = [
    (180, "warmup"),  # 3 minutes in warmup
    (180, "high"),    # 3 minutes in high intensity
    (180, "low"),     # 3 minutes in low intensity
    (180, "high"),
    (180, "low"),
    (180, "high"),
    (180, "low"),
    (180, "high"),
    (180, "cooldown") # 3 minutes in cooldown
]
#endregion

# Global variable for current heart rate
current_heart_rate = 0

def get_current_heart_rate():
    """Continuously update the heart rate from user input."""
    global current_heart_rate
    while True:
        try:
            current_heart_rate = int(input("Enter current heart rate: "))
            adjust_speed_based_on_heart_rate(current_heart_rate)
        except ValueError:
            print("Please enter a valid heart rate as an integer.")

def adjust_speed_based_on_heart_rate(heart_rate):
    """Calculate and set playback speed based on heart rate and target zones."""
    for _, zone in time_intervals:
        zone_min, zone_max = heart_rate_zones[zone]
        if heart_rate < zone_min:
            set_playback_speed(1.2)  # Increase speed to motivate
        elif heart_rate > zone_max:
            set_playback_speed(0.8)  # Decrease speed to slow down
        else:
            set_playback_speed(1.0)  # Normal speed in target zone
        break  # Exit after setting speed for the current interval

# Start a separate thread for continuous heart rate input
threading.Thread(target=get_current_heart_rate, daemon=True).start()

# Play each song in the selected playlist
for song in playlist:
    song_path = song["file"]  # Extract the file path from the song dictionary
    print(f"Playing {song['name']}")
    play_song(song_path)
