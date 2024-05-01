import cv2
import datetime

def record_video(filename, duration, update_progress_callback):
    cap = cv2.VideoCapture(0)  
    if not cap.isOpened():
        print("Error: Cannot open webcam.")
        return

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))

    start_time = datetime.datetime.now()
    print("Recording started...")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Cannot capture frame.")
            break

        out.write(frame)

        # update progress bar 
        elapsed_time = (datetime.datetime.now() - start_time).seconds
        update_progress_callback(elapsed_time)

        if elapsed_time >= duration:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print("Recording stopped.")

def play_video_slow(filename):
    # open the video file
    cap = cv2.VideoCapture(filename)
    if not cap.isOpened():
        print("Error: Cannot open video file.")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    delay = int(1000 / fps * 2)  # frame speed playback

    print("Playback at half speed...")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        cv2.imshow('Video Playback', frame)
        if cv2.waitKey(delay) & 0xFF == ord('q'): 
            break

    cap.release()
    cv2.destroyAllWindows()