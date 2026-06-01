import cv2
import os

# ====== INPUT ======
video_path = "theft.mp4"   # change for each video
output_folder = "theft"
frames_per_second = 2        # change if needed

# ====== CREATE OUTPUT FOLDER ======
os.makedirs(output_folder, exist_ok=True)

# ====== LOAD VIDEO ======
cap = cv2.VideoCapture(video_path)

# Get original FPS of video
video_fps = cap.get(cv2.CAP_PROP_FPS)

# Calculate interval
interval = int(video_fps / frames_per_second)

frame_id = 0
saved_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Save every nth frame
    if frame_id % interval == 0:
        filename = os.path.join(output_folder, f"frame_{saved_count:04d}.jpg")
        cv2.imwrite(filename, frame)
        saved_count += 1

    frame_id += 1

cap.release()

print("Frames extracted successfully!")