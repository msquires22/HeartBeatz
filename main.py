#region IMPORTS
import threading
import time
import math
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
    (15, "warmup"),  # 3 minutes in warmup
    (15, "high"),    # 3 minutes in high intensity
    (180, "low"),     # 3 minutes in low intensity
    (180, "high"),
    (180, "low"),
    (180, "high"),
    (180, "low"),
    (180, "high"),
    (180, "cooldown") # 3 minutes in cooldown
]
#endregion

# Global variables
current_heart_rate = 0
current_zone = time_intervals[0][1]  # Start in the first zone
zone_index = 0
zone_end_time = time.time() + time_intervals[0][0]  # Set the end time for the first interval

def get_current_heart_rate():
    """Continuously update the heart rate from user input."""
    global current_heart_rate
    while True:
        try:
            # Continuously prompt for heart rate input
            current_heart_rate = int(input("Enter current heart rate: "))
            adjust_speed_based_on_heart_rate(current_heart_rate)
        except ValueError:
            print("Please enter a valid heart rate as an integer.")

def calculate_tempo_adjustment(heart_rate, zone_min, zone_max):
    """
    Calculate playback speed adjustment based on heart rate.
    Returns a tempo between 0.85 and 1.15 based on proximity to the target zone.
    """
    max_speed = 1.15
    min_speed = 0.85

    if heart_rate < zone_min:
        # Heart rate is below target zone - scale up tempo
        difference = zone_min - heart_rate
        max_difference = zone_min * 0.25
        tempo_increase = max_speed - (max_speed - 1.0) * math.exp(-difference / max_difference)
        return min(max(1.0, tempo_increase), max_speed)
    
    elif heart_rate > zone_max:
        # Heart rate is above target zone - scale down tempo
        difference = heart_rate - zone_max
        max_difference = zone_max * 0.25
        tempo_decrease = min_speed + (1.0 - min_speed) * math.exp(-difference / max_difference)
        return max(min(1.0, tempo_decrease), min_speed)
    
    else:
        # Heart rate is within target zone
        return 1.0

def adjust_speed_based_on_heart_rate(heart_rate):
    """Calculate and set playback speed based on heart rate and current zone."""
    global current_zone, zone_index, zone_end_time

    # Update the zone if time has elapsed
    if time.time() >= zone_end_time:
        # Move to the next interval
        zone_index += 1
        if zone_index < len(time_intervals):
            # Update the current zone and end time
            duration, current_zone = time_intervals[zone_index]
            zone_end_time = time.time() + duration
            print(f"Switched to zone: {current_zone} for the next {duration} seconds.")
        else:
            # End in cooldown if no more intervals
            current_zone = "cooldown"

    # Set speed based on the heart rate and current zone
    zone_min, zone_max = heart_rate_zones[current_zone]
    print(f"Current zone: {current_zone}, HR target range: {zone_min}-{zone_max}")  # Print current THRZ range
    new_speed = calculate_tempo_adjustment(heart_rate, zone_min, zone_max)
    set_playback_speed(new_speed)

# Start a separate thread for continuous heart rate input
threading.Thread(target=get_current_heart_rate, daemon=True).start()

# Play each song in the selected playlist with heart rate-based tempo control
for song in playlist:
    song_path = song["file"]  # Extract the file path from the song dictionary
    print(f"Playing {song['name']}")
    play_song(song_path)