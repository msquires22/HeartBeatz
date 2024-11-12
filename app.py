import tkinter as tk
from tkinter import ttk
import threading
import time
import main2
import json
import os

# Initialize main Tkinter window
root = tk.Tk()
root.title("Heart Rate Controlled Music Player")

# Center the root window's columns
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Global Variables for Heart Rate and Display Updates
current_hr_text = tk.StringVar()  # To display the current heart rate
display_text = tk.StringVar()      # For the current song name
thrz_text = tk.StringVar()         # For the THRZ information
elapsed_time_text = tk.StringVar()  # To show elapsed time since start
remaining_time_text = tk.StringVar()  # Time left in the current THRZ

# Callback function to update the UI display for the current song
def display_callback(message):
    display_text.set(message)

# Function to start playback with user inputs
def start_playback():
    age = age_entry.get()
    genre = genre_combobox.get()
    main2.initialize(age, genre)

    # Initialize THRZ and timer displays
    thrz_text.set(main2.get_thrz_info())
    start_time = time.time()

    def continuous_update():
        def read_variable():
            with open("shared_data.json", "r") as f:
                data = json.load(f)
            return data["hr"]

        last_modified = None
        hr = 0.0
        while True:
            try:
                modified_time = os.path.getmtime("shared_data.json")
                if modified_time != last_modified:
                    last_modified = modified_time
                    value = read_variable()
                    hr = float(value)  # Get the current heart rate from the input
                main2.adjust_speed_based_on_heart_rate(hr, thrz_text.set)
                current_hr_text.set(f"Current HR: {hr}")

                # Calculate elapsed time and remaining time in THRZ
                elapsed = int(time.time() - start_time)
                elapsed_time_text.set(f"Elapsed Time: {elapsed // 60}:{elapsed % 60:02d}")

                remaining = main2.get_time_remaining_in_zone()
                remaining_time_text.set(f"Time Left in THRZ: {remaining // 60}:{remaining % 60:02d}")

            except ValueError:
                pass
            time.sleep(1)

    threading.Thread(target=continuous_update, daemon=True).start()
    threading.Thread(target=main2.play_songs_with_ui_update, args=(display_callback,), daemon=True).start()

# UI Elements
tk.Label(root, height=5, width=30, font=("Arial", 25), text="Enter Age:").grid(row=0, column=0, sticky="e")
age_entry = tk.Entry(root)
age_entry.grid(row=0, column=1, pady=5, padx=5, sticky="w")

tk.Label(root, height=5, width=30, font=("Arial", 25), text="Select Genre:").grid(row=1, column=0, sticky="e")
genre_combobox = ttk.Combobox(root, values=["Country", "Pop", "Rock", "Rap", "Electronic Dance"])
genre_combobox.grid(row=1, column=1, pady=5, padx=5, sticky="w")

start_button = tk.Button(root, font=("Arial", 25), text="Start Playback", command=start_playback)
start_button.grid(row=2, column=0, columnspan=2, pady=10)

# Display Fields
tk.Label(root, height=4, width=30, font=("Arial", 30), textvariable=current_hr_text).grid(row=3, column=0, columnspan=2, sticky="nsew")

tk.Label(root, height=4, width=30, font=("Arial", 25), text="Target Heart Rate Zone (THRZ):").grid(row=4, column=0, sticky="e")
tk.Label(root, height=4, width=30, font=("Arial", 25), textvariable=thrz_text).grid(row=4, column=1, sticky="w")

tk.Label(root, height=4, width=30, font=("Arial", 25), text="Time Left in THRZ:").grid(row=5, column=0, sticky="e")
tk.Label(root, height=4, width=30, font=("Arial", 25), textvariable=remaining_time_text).grid(row=5, column=1, sticky="w")

tk.Label(root, height=4, width=30, font=("Arial", 25), text="Elapsed Workout Time:").grid(row=6, column=0, sticky="e")
tk.Label(root, height=4, width=30, font=("Arial", 25), textvariable=elapsed_time_text).grid(row=6, column=1, sticky="w")

tk.Label(root, height=4, width=30, font=("Arial", 25), text="Current Song:").grid(row=7, column=0, sticky="e")
tk.Label(root, height=4, width=30, font=("Arial", 25), textvariable=display_text).grid(row=7, column=1, sticky="w")

root.mainloop()
