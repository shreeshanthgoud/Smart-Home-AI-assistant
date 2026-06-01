import requests

TOKEN = "7811526566:AAGfByOBOSDfIq6PNSR5B_tAzFgy9Dv7rko"
CHAT_ID = "1446473042"

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

data = {
    "chat_id": CHAT_ID,
    "text": "⚠️ Test Alert Working"
}

requests.post(url, data=data)