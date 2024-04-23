import cv2
import datetime

def record_video(filename, duration):
    # Capture video from the webcam
    cap = cv2.VideoCapture(1)  
    if not cap.isOpened():
        print("Error: Cannot open webcam.")
        return

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))

    start_time = datetime.datetime.now()
    print("Recording started...")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Cannot capture frame.")
            break
        
        out.write(frame)  # Write the frame into the file

        # Show the frame on the screen (optional)
        cv2.imshow('Webcam', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Stop recording after 'duration' seconds
        if (datetime.datetime.now() - start_time).seconds > duration:
            break

    # Release everything when done
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print("Recording stopped.")

def play_video_slow(filename):
    # Open the video file
    cap = cv2.VideoCapture(filename)
    if not cap.isOpened():
        print("Error: Cannot open video file.")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    delay = int(1000 / fps * 2)  # Delay between frames in ms, doubled for half speed

    print("Playback at half speed...")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        cv2.imshow('Video Playback', frame)
        if cv2.waitKey(delay) & 0xFF == ord('q'):  # Wait longer for half-speed playback
            break

    cap.release()
    cv2.destroyAllWindows()

# Set the filename and duration
filename = "webcam_recording.avi"
duration = 3  # record for 3 seconds

flag = False

while not flag:
    user_input = input("Type 'r' to start recording\n")

    if user_input == 'r':
        flag = True

record_video(filename, duration)
play_video_slow(filename)
