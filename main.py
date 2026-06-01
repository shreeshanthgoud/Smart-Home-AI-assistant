# main.py

# 1. Hide the annoying OpenCV [mjpeg overread] spam warnings
import os
os.environ["OPENCV_LOG_LEVEL"] = "FATAL" 

import cv2
import time
import threading

# Import from your modules
from model_utils import predict_activity, detect_objects
from telegram_utils import send_message, send_photo, get_updates
from storage_utils import save_snapshot, upload_cloudinary
from ai_utils import generate_response

# Added ?fps=15 to help prevent lag and dropped frames
IP_WEBCAM_URL = "http://10.122.20.39:8080/video?fps=15"


# ==========================
# LOW LATENCY STREAM
# ==========================
class VideoStream:
    def __init__(self, src):
        self.cap = cv2.VideoCapture(src)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        self.ret, self.frame = self.cap.read()
        self.running = True

        threading.Thread(target=self.update, daemon=True).start()

    def update(self):
        while self.running:
            if self.cap.isOpened():
                self.cap.grab()
                self.ret, self.frame = self.cap.retrieve()

    def read(self):
        return self.ret, self.frame

    def stop(self):
        self.running = False
        self.cap.release()


# ==========================
# INIT
# ==========================
stream = VideoStream(IP_WEBCAM_URL)

current_status = "normal"
current_activity = "idle"

last_bot_poll_time = 0
last_alert_time = 0
latest_frame = None
frame_count = 0

# ✅ Start message (only once)
send_message("✅ Monitoring system started.")


# ==========================
# MAIN LOOP
# ==========================
while True:
    ret, frame = stream.read()

    if not ret:
        print("Reconnecting...")
        stream.stop()
        time.sleep(2)
        stream = VideoStream(IP_WEBCAM_URL)
        continue

    latest_frame = frame.copy()
    frame = cv2.resize(frame, (640, 480))

    frame_count += 1

    # ==========================
    # COMBINED AI PREDICTION (ACTIVITY + OBJECTS)
    # ==========================
    if frame_count % 6 == 0:
        
        # 1. Base Activity (Cooking, Cleaning, Theft)
        base_activity = predict_activity(frame)
        base_clean = str(base_activity).strip().lower()
        is_idle = base_clean in ["normal", "idle", "", "none"]

        # 2. YOLO Object Detection
        yolo_status, object_found, boxed_frame = detect_objects(frame)

        # 3. Combine them intelligently into a single phrase
        if yolo_status == "interaction_detected":
            if not is_idle:
                current_activity = f" and interacting with {object_found}"
        else:
            current_activity = base_clean if not is_idle else "idle"

        # 4. Handle Alerts and Notifications
        if base_clean == "theft":
            current_status = "theft"
            
            # Theft Cooldown (only alert every 15 seconds)
            if time.time() - last_alert_time > 15:
                print("🚨 ALERT: THEFT DETECTED!")
                last_alert_time = time.time()
                
                path = save_snapshot(frame, "theft_alert")
                try:
                    upload_cloudinary(path)
                except Exception as e:
                    print("Cloudinary error:", e)
                    
                send_photo(path, f"🚨 URGENT: Theft detected!\nCurrent Activity: {current_activity}")
                
        elif yolo_status == "interaction_detected":
            current_status = "alert"
            
            # Object Cooldown (only alert every 15 seconds)
            if time.time() - last_alert_time > 15:
                print(f"Alert triggered: Person interacting with {object_found}!")
                last_alert_time = time.time()
                
                path = save_snapshot(boxed_frame, "auto_alert")
                try:
                    upload_cloudinary(path)
                except Exception as e:
                    print("Cloudinary error:", e)
                    
                send_photo(path, f"⚠️ ALERT: Someone is interacting with the {object_found}!\nCurrent Activity: {current_activity}")
        else:
            current_status = "normal"


    # ==========================
    # TELEGRAM HANDLING
    # ==========================
    if time.time() - last_bot_poll_time > 3:
        user_msg = get_updates()
        last_bot_poll_time = time.time()

        if user_msg:
            print("Received message:", user_msg)
            msg = user_msg.lower()

            # ===== IMAGE REQUEST =====
            if any(keyword in msg for keyword in ["image", "photo", "snapshot", "picture"]):
                path = save_snapshot(latest_frame, "manual")
                
                try:
                    upload_cloudinary(path)
                    print("✅ Uploaded to Cloudinary successfully.")
                except Exception as e:
                    print("⚠️ Cloudinary upload failed:", e)

                send_photo(path, f"Here is the current view.")
            
            # ===== GEMINI RESPONSE =====
            else:
                try:
                    reply = generate_response(
                        current_status=current_status,
                        current_activity=current_activity,
                        user_query=user_msg
                    )

                    print("Gemini reply:", reply)

                    if not reply or str(reply).strip() == "":
                        reply = "⚠️ I couldn't get a response from Gemini. Please try asking again."

                except Exception as e:
                    print("Gemini error:", e)
                    reply = "⚠️ I encountered an error connecting to my AI brain."

                send_message(reply)


    # ==========================
    # DISPLAY FEED ON SCREEN
    # ==========================
    # Draw the current activity text on the window

    cv2.imshow("Smart Home Monitor", frame)

    if cv2.waitKey(1) & 0xFF == 27: # Press 'Esc' to exit
        send_message("❌ Monitoring stopped.")
        break


# ==========================
# CLEANUP
# ==========================
stream.stop()
cv2.destroyAllWindows()