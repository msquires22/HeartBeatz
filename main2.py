#region IMPORTS
import time
import math
from audio_player import play_song, set_playback_speed
from songLists import country, electronicDance, pop, rap, rock
#endregion

# Global variables to be set from the front end
age = None
current_genre = None
current_heart_rate = 0
current_zone = "warmup"  # Start in the warmup zone
playlist = None
zone_index = 0
zone_end_time = time.time() + 10  # Starting with 10 seconds for warmup

# Map user choices to playlists
genres = {
    "Country": country,
    "Pop": pop,
    "Rock": rock,
    "Rap": rap,
    "Electronic Dance": electronicDance
}

# Function to initialize age, genre, and playlist from the UI
def initialize(age_input, genre_input):
    global age, current_genre, playlist
    age = int(age_input)
    current_genre = genre_input
    playlist = genres.get(current_genre)
    calculate_zones()  # Initialize the heart rate zones

def calculate_zones():
    """Calculate heart rate zones based on age."""
    global maxHR, heart_rate_zones, time_intervals, zone_index, zone_end_time, current_zone
    maxHR = int(191.5 - .007 * age**2)  # max heart rate
    heart_rate_zones = {
        "warmup": (int(maxHR * 0.4), int(maxHR * 0.5)),
        "high": (int(maxHR * 0.75), int(maxHR * 0.9)),
        "low": (int(maxHR * 0.5), int(maxHR * 0.75))
    }
    time_intervals = [
        (180, "warmup"),
        (180, "high"),
        (180, "low"),
        (180, "high"),
        (180, "low"),
        (180, "high"),
        (180, "low"),
        (180, "high"),
        (180, "cooldown")
    ]
    zone_index = 0
    current_zone = time_intervals[zone_index][1]
    zone_end_time = time.time() + time_intervals[zone_index][0]

def calculate_tempo_adjustment(heart_rate, zone_min, zone_max):
    """Adjust playback speed based on heart rate."""
    max_speed = 1.15
    min_speed = 0.85

    if heart_rate < zone_min:
        difference = zone_min - heart_rate
        max_difference = zone_min * 0.25
        tempo_increase = max_speed - (max_speed - 1.0) * math.exp(-difference / max_difference)
        return min(max(1.0, tempo_increase), max_speed)
    elif heart_rate > zone_max:
        difference = heart_rate - zone_max
        max_difference = zone_max * 0.25
        tempo_decrease = min_speed + (1.0 - min_speed) * math.exp(-difference / max_difference)
        return max(min(1.0, tempo_decrease), min_speed)
    else:
        return 1.0

def adjust_speed_based_on_heart_rate(heart_rate, display_callback):
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
            display_callback(f"{get_thrz_info()}")
        else:
            current_zone = "cooldown"

    zone_min, zone_max = heart_rate_zones[current_zone]
    new_speed = calculate_tempo_adjustment(heart_rate, zone_min, zone_max)
    set_playback_speed(new_speed)

def get_thrz_info():
    """Retrieve current Target Heart Rate Zone (THRZ) details."""
    zone_min, zone_max = heart_rate_zones[current_zone]
    return f"{current_zone.capitalize()} Zone - Target HR: {zone_min} to {zone_max}"

def play_songs_with_ui_update(display_callback):
    """Play each song and update the UI with the current song and THRZ info."""
    for song in playlist:
        song_name = song["name"]
        song_path = song["file"]
        
        # Update the UI with the current song and THRZ info
        display_callback(f"Playing {song_name}")
        
        # Play the song
        play_song(song_path)

#made with assistance of ChatGPT: https://chatgpt.com/share/6722839a-fad4-800f-933a-1552d8787364