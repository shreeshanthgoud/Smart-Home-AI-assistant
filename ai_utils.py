# ai_utils.py

from google import genai
from config import GEMINI_API_KEY, USER_NAME

client = genai.Client(api_key=GEMINI_API_KEY)

# ✅ Updated parameter names to match main.py
def generate_response(current_status, current_activity, user_query):
    prompt = f"""
You are a professional AI home monitoring assistant.

User name: {USER_NAME}

Current status: {current_status}
Current activity: {current_activity}

User asked: "{user_query}"

Respond clearly, professionally, and politely.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",   # latest working model
            contents=prompt
        )

        return response.text

    except Exception as e:
        print("Gemini Error:", e)
        return "System is active, but unable to generate response right now."


def explain_image(image_path):
    try:
        with open(image_path, "rb") as f:
            image_bytes = f.read()

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                "Describe what is happening in this scene professionally.",
                {"mime_type": "image/jpeg", "data": image_bytes}
            ]
        )

        return response.text

    except Exception as e:
        print("Image Error:", e)
        return "Unable to analyze image."