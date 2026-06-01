# storage_utils.py

import os
import time
import cv2
import cloudinary
import cloudinary.uploader
from config import CLOUD_NAME, API_KEY, API_SECRET

cloudinary.config(
    cloud_name=CLOUD_NAME,
    api_key=API_KEY,
    api_secret=API_SECRET
)

SNAP_DIR = "snapshots"
os.makedirs(SNAP_DIR, exist_ok=True)

def save_snapshot(frame, tag="event"):
    ts = time.strftime("%Y%m%d_%H%M%S")
    path = os.path.join(SNAP_DIR, f"{tag}_{ts}.jpg")
    cv2.imwrite(path, frame)
    return path

def upload_cloudinary(path):
    try:
        result = cloudinary.uploader.upload(path, folder="home_monitor")
        return result.get("secure_url")
    except:
        return None