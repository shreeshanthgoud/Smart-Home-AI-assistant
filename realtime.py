import cv2
import requests
import time
import numpy as np
from tensorflow.keras.models import load_model

# --- CONFIG ---
TOKEN = "7811526566:AAGfByOBOSDfIq6PNSR5B_tAzFgy9Dv7rko"
CHAT_ID = "1446473042"
IP_CAMERA_URL = "http://10.101.4.49:2253/video"

# --- MODEL ---
model = load_model("activity_model.h5")

classes = ["cooking", "cleaning", "cutting", "washing", "theft"]

# --- GLOBAL STATE ---
latest_status = "System started"
last_update_id = None
last_alert_time = 0

# --- TELEGRAM FUNCTIONS ---
def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

def get_updates():
    global last_update_id
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    response = requests.get(url).json()

    for result in response["result"]:
        update_id = result["update_id"]

        if last_update_id is None or update_id > last_update_id:
            last_update_id = update_id

            if "message" in result:
                return result["message"]["text"].lower()

    return None

# --- MODEL PREDICTION ---
def predict_activity(frame):
    img = cv2.resize(frame, (224, 224))
    img = img / 255.0
    img = np.reshape(img, (1, 224, 224, 3))

    prediction = model.predict(img)
    return classes[np.argmax(prediction)]

# --- CAMERA ---
cap = cv2.VideoCapture(IP_CAMERA_URL)

while True:
    ret, frame = cap.read()

    # 1️⃣ AI Prediction
    prediction = predict_activity(frame)

    # 2️⃣ Update Status
    if prediction == "theft":
        latest_status = "⚠️ Theft detected"
        
        # Send alert every 10 seconds max
        if time.time() - last_alert_time > 500:
            send_message("🚨 ALERT: Theft detected in kitchen")
            last_alert_time = time.time()
    else:
        latest_status = "✅ No abnormal activity"

    # 3️⃣ Check Telegram Messages
    user_msg = get_updates()

    if user_msg:
        if "abnormal" in user_msg or "theft" in user_msg:
            send_message(latest_status)

        elif "status" in user_msg:
            send_message(latest_status)

        elif "hi" in user_msg or "hello" in user_msg:
            send_message("Hello! I am monitoring your home.")

    cv2.imshow("Feed", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()