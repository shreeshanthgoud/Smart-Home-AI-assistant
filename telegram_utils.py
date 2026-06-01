import requests
from config import TOKEN, CHAT_ID

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

def send_photo(path, caption=None):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    with open(path, "rb") as f:
        requests.post(
            url,
            data={"chat_id": CHAT_ID, "caption": caption or ""},
            files={"photo": f}
        )

last_update_id = None

def get_updates():
    global last_update_id
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    
    params = {"offset": last_update_id + 1} if last_update_id else {}

    try:
        # Added a timeout so it doesn't freeze your camera stream
        response = requests.get(url, params=params, timeout=5).json()
        
        if not response.get("ok"):
            return None

        results = response.get("result", [])
        if not results:
            return None

        # 1. Update offset immediately to the LAST message to clear the queue
        last_update_id = results[-1]["update_id"]

        # 2. Extract ONLY the very latest message (ignore any older spam)
        latest_msg = results[-1]
        if "message" in latest_msg and "text" in latest_msg["message"]:
            return latest_msg["message"]["text"]

    except Exception as e:
        print(f"Telegram polling error: {e}")

    return None