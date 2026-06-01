# model_utils.py
import cv2
import numpy as np
from ultralytics import YOLO
from tensorflow.keras.models import load_model

# ⚠️ PUT YOUR ORIGINAL TENSORFLOW/KERAS IMPORTS HERE
# from keras.models import load_model ... etc

# ==========================================
# 1. LOAD BOTH MODELS SEPARATELY
# ==========================================

# Load your original model for cooking/cleaning (Replace with your actual model file!)
activity_model = load_model('activity_model.h5') 

# Load the YOLO model for objects
yolo_model = YOLO('yolov8n.pt') 

TARGET_OBJECTS = ['apple', 'banana', 'orange', 'carrot', 'bottle', 'cell phone']


# ==========================================
# 2. ACTIVITY PREDICTION (Cooking, Cleaning)
# ==========================================
def predict_activity(frame):
    if frame is None or len(frame) == 0:
        return "normal"
        
    try:
        frame_small = cv2.resize(frame, (224, 224))
        
        # Make sure the frame is formatted correctly for your specific model!
        img_array = np.asarray(frame_small, dtype=np.float32).reshape(1, 224, 224, 3)
        img_array = (img_array / 127.5) - 1 # Normalize if your model requires it
        
        # Get the prediction numbers
        prediction = activity_model.predict(img_array, verbose=0)
        
        # ✅ THE MISSING LOGIC: Translating the numbers back into words
        # Make sure these match the EXACT order you trained your model in!
        CLASS_NAMES = ["cleaning", "cooking", "cutting", "washing", "theft","normal"]
        
        # Find the index of the highest probability
        highest_index = np.argmax(prediction)
        
        # Return the actual word
        return CLASS_NAMES[highest_index]
        
    except Exception as e:
        print("Activity model error:", e)
        return "normal"

# ==========================================
# 3. OBJECT DETECTION (YOLO)
# ==========================================
def detect_objects(frame):
    # Safety check
    if frame is None or len(frame) == 0:
        return "normal", None, frame
        
    try:
        # ✅ Pass the FULL SIZE frame directly to the 'yolo_model'
        results = yolo_model(frame, verbose=False)
        detected_classes = []
        
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                class_name = yolo_model.names[class_id]
                detected_classes.append(class_name)

        if "person" in detected_classes:
            for obj in TARGET_OBJECTS:
                if obj in detected_classes:
                    return "interaction_detected", obj, results[0].plot()
                    
        return "normal", None, frame
        
    except Exception as e:
        print("YOLO error:", e)
        return "normal", None, frame