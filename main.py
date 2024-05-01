import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from functions import record_video, play_video_slow
import threading

# Set the filename and duration
filename = "webcam_recording.avi"
duration = 1  # record for 2 seconds

def start_recording():
    def update_progress(elapsed_time):
        progress['value'] = elapsed_time
        root.update_idletasks()

    def recording_complete():
        play_button.pack(pady=20)  # Show play button after recording

    threading.Thread(target=record_video_and_handle_completion, args=(filename, duration, update_progress, recording_complete)).start()
    play_button.pack_forget()  # Hide play button during recording

def record_video_and_handle_completion(filename, duration, update_progress, completion_callback):
    record_video(filename, duration, update_progress)
    root.after(0, completion_callback)  # Schedule the play button to show up after recording

def start_playback():
    play_video_slow(filename)

def set_background_image():
    image = Image.open("waves_background.jpg")  # Replace with your actual image path
    resized_image = image.resize((root.winfo_width(), root.winfo_height()), Image.Resampling.LANCZOS)
    bg_image = ImageTk.PhotoImage(resized_image)
    bg_label.config(image=bg_image)
    bg_label.image = bg_image  # Keep a reference!

# Create the main window
root = tk.Tk()
root.title("Video Recorder")
root.attributes('-fullscreen', True)

bg_label = tk.Label(root)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

root.bind('<Configure>', lambda event: set_background_image())  # Update background on resize



def toggle_fullscreen():
    root.attributes('-fullscreen', not root.attributes('-fullscreen'))

# Styling
style = ttk.Style(root)
style.theme_use('clam')

# Progress bar style
style.configure('Horizontal.TProgressbar', background='#6E6449', troughcolor='#DDD5C7', thickness=20)

# Button style
style.configure('TButton', font=('Helvetica', 14, 'bold'), foreground='#FFFFFF', background='#8B8378')
style.map('TButton',
          foreground=[('pressed', '#FFFFFF'), ('active', '#FFFFFF')],
          background=[('pressed', '!disabled', '#5C5346'), ('active', '#6E6449')])

# Add a toggle button
toggle_button = ttk.Button(root, text="Toggle Fullscreen", style='TButton', command=toggle_fullscreen)
toggle_button.pack(pady=10, padx=10, fill=tk.X)

# Create a progress bar
progress = ttk.Progressbar(root, style='Horizontal.TProgressbar', orient="horizontal", length=400, mode="determinate", maximum=duration)
progress.pack(pady=20, padx=10, fill=tk.X)

# Create a button that will start the video recording
record_button = ttk.Button(root, text="Start Recording", style='TButton', command=start_recording)
record_button.pack(pady=20, padx=10, fill=tk.X)

# Create a button to play the video, initially not visible
play_button = ttk.Button(root, text="Play", style='TButton', command=start_playback)

# Start the GUI event loop
root.mainloop()
