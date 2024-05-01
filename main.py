import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from functions import record_video, play_video_slow
import threading

# set the filename and duration
filename = "webcam_recording.avi"
duration = 1  # record for 2 seconds

def start_recording():
    def update_progress(elapsed_time):
        progress['value'] = elapsed_time
        root.update_idletasks()

    def recording_complete():
        play_button.pack(pady=20)  # play button

    threading.Thread(target=record_video_and_handle_completion, args=(filename, duration, update_progress, recording_complete)).start()
    play_button.pack_forget()  # dont show play button while recording

def record_video_and_handle_completion(filename, duration, update_progress, completion_callback):
    record_video(filename, duration, update_progress)
    root.after(0, completion_callback)  # show play button after recording

def start_playback():
    play_video_slow(filename)

def set_background_image():
    image = Image.open("waves_background.jpg") 
    resized_image = image.resize((root.winfo_width(), root.winfo_height()), Image.Resampling.LANCZOS)
    bg_image = ImageTk.PhotoImage(resized_image)
    bg_label.config(image=bg_image)
    bg_label.image = bg_image  

# main window
root = tk.Tk()
root.title("Video Recorder")
root.attributes('-fullscreen', True)

bg_label = tk.Label(root)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

root.bind('<Configure>', lambda event: set_background_image())  # fit background to size



def toggle_fullscreen():
    root.attributes('-fullscreen', not root.attributes('-fullscreen'))


style = ttk.Style(root)
style.theme_use('clam')


style.configure('Horizontal.TProgressbar', background='#6E6449', troughcolor='#DDD5C7', thickness=20)


style.configure('TButton', font=('Helvetica', 14, 'bold'), foreground='#FFFFFF', background='#8B8378')
style.map('TButton',
          foreground=[('pressed', '#FFFFFF'), ('active', '#FFFFFF')],
          background=[('pressed', '!disabled', '#5C5346'), ('active', '#6E6449')])

# toggle button
toggle_button = ttk.Button(root, text="Toggle Fullscreen", style='TButton', command=toggle_fullscreen)
toggle_button.pack(pady=10, padx=10, fill=tk.X)

# progress bar
progress = ttk.Progressbar(root, style='Horizontal.TProgressbar', orient="horizontal", length=400, mode="determinate", maximum=duration)
progress.pack(pady=20, padx=10, fill=tk.X)

# record button
record_button = ttk.Button(root, text="Start Recording", style='TButton', command=start_recording)
record_button.pack(pady=20, padx=10, fill=tk.X)

# play video button
play_button = ttk.Button(root, text="Play", style='TButton', command=start_playback)


root.mainloop()
