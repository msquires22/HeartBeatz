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

# Global Variables for Heart Rate and Display Updates
#heart_rate = tk.StringVar()
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
                    print("getting new hr value...")
                    value = read_variable()
                    print(value)
                    hr = float(value) # Get the current heart rate from the input
                    print("new heartrate: ", str(hr))
                main2.adjust_speed_based_on_heart_rate(hr, thrz_text.set)
                current_hr_text.set(f"Current HR: {hr}")
                print("Updated value:", str(hr))

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

# Function to handle heart rate input when Enter is pressed
#def on_heart_rate_enter(event):
#    try:
#        hr = int(heart_rate_entry.get())
#        heart_rate.set(hr)
#        main2.adjust_speed_based_on_heart_rate(hr, thrz_text.set)
#        current_hr_text.set(f"Current HR: {hr}")
#        heart_rate_entry.delete(0, tk.END)  # Clear the input field after entry
#    except ValueError:
#        pass

# UI Elements

tk.Label(root, text="Enter Age:").grid(row=0, column=0, sticky="w")
age_entry = tk.Entry(root)
age_entry.grid(row=0, column=1, pady=5, padx=5)

tk.Label(root, text="Select Genre:").grid(row=1, column=0, sticky="w")
genre_combobox = ttk.Combobox(root, values=["Country", "Pop", "Rock", "Rap", "Electronic Dance"])
genre_combobox.grid(row=1, column=1, pady=5, padx=5)

start_button = tk.Button(root, text="Start Playback", command=start_playback)
start_button.grid(row=2, column=0, columnspan=2, pady=10)

# Display Fields

tk.Label(root, height=3, width=30, text="Current Song:").grid(row=3, column=0, sticky="w")
tk.Label(root, height=3, width=30, textvariable=display_text).grid(row=3, column=1, sticky="w")

tk.Label(root, height=3, width=30, text="Target Heart Rate Zone (THRZ):").grid(row=4, column=0, sticky="w")
tk.Label(root, height=3, width=30, textvariable=thrz_text).grid(row=4, column=1, sticky="w")

tk.Label(root, height=3, width=30, text="Elapsed Workout Time:").grid(row=5, column=0, sticky="w")
tk.Label(root, height=3, width=30, textvariable=elapsed_time_text).grid(row=5, column=1, sticky="w")

tk.Label(root,height=3, width=30, text="Time Left in THRZ:").grid(row=6, column=0, sticky="w")
tk.Label(root, height=3, width=30, textvariable=remaining_time_text).grid(row=6, column=1, sticky="w")

#tk.Label(root, text="Enter Heart Rate:").grid(row=7, column=0, sticky="w")
#heart_rate_entry = tk.Entry(root, textvariable=heart_rate)
#heart_rate_entry.grid(row=7, column=1, pady=5, padx=5)
#heart_rate_entry.bind("<Return>", on_heart_rate_enter)  # Bind Enter key to update heart rate

tk.Label(root, height=3, width=30, textvariable=current_hr_text).grid(row=8, column=0, columnspan=2)

root.mainloop()
