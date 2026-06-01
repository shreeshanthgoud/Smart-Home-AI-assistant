import cv2
import time
import threading
from model_utils import predict_activity
from telegram_utils import send_message, send_photo, get_updates
from storage_utils import save_snapshot
from ai_utils import generate_response

IP_WEBCAM_URL = "http://192.0.0.4:8080/video"


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
    # AI PREDICTION (NO MESSAGES)
    # ==========================
    if frame_count % 6 == 0:
        frame_small = cv2.resize(frame, (224, 224))
        prediction = predict_activity(frame_small)

        current_activity = prediction
        current_status = "theft" if prediction == "theft" else "normal"

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
                send_photo(path, "Here is the current view.")
            
            # ===== GEMINI RESPONSE =====
            else:
                try:
                    reply = generate_response(
                        current_status=current_status,
                        current_activity=current_activity,
                        user_query=user_msg
                    )

                    print("Gemini reply:", reply)

                    # If Gemini fails to return text, do NOT use a manual hardcoded string
                    if not reply or str(reply).strip() == "":
                        reply = "⚠️ I couldn't get a response from Gemini. Please try asking again."

                except Exception as e:
                    print("Gemini error:", e)
                    # Send an error message so you know exactly why it failed
                    reply = "⚠️ I encountered an error connecting to my AI brain."

                send_message(reply)