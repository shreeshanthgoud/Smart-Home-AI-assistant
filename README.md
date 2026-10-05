# AI-Powered Smart Home Monitoring and Security System

## Overview

The AI-Powered Smart Home Monitoring and Security System is an intelligent surveillance solution that combines Computer Vision, Machine Learning, IoT, and real-time communication technologies to monitor household activities and enhance home security.

Unlike traditional CCTV systems that only record footage, this system understands household activities, detects abnormal behavior, captures evidence, and sends instant alerts to homeowners through Telegram.

---

## Features

### Activity Recognition
- Cooking Detection
- Cleaning Detection
- Washing Vessels Detection
- Vegetable Cutting Detection
- Idle Activity Detection

### Security Monitoring
- Suspicious Activity Detection
- Theft Detection
- Real-Time Alerts
- Automated Snapshot Capture

### Smart Notifications
- Telegram Bot Integration
- AI-Generated Activity Responses
- Event-Based Notifications
- User Query Handling

### Cloud Integration
- Cloudinary Storage Support
- Snapshot Backup
- Event History Storage

### Smart Home Features
- Owner-Controlled Door Access
- CCTV/IP Camera Integration
- Mobile Camera (IP Webcam) Support
- Multi-Camera Expansion Ready

---

## System Architecture

```text
Camera Feed (CCTV/IP Camera/Mobile Camera)
                │
                ▼
      Activity Recognition Model
                │
                ▼
      Activity Classification
                │
                ▼
     Abnormal Activity Detection
                │
                ▼
 Telegram Alerts + Cloud Storage
                │
                ▼
      Homeowner Decision Making
```

---

## Technology Stack

### Programming Language
- Python

### Libraries & Frameworks
- OpenCV
- NumPy
- TensorFlow / Keras
- Requests
- Telegram Bot API

### Cloud Services
- Cloudinary

### AI Technologies
- Computer Vision
- Deep Learning
- Activity Recognition
- Anomaly Detection

---

## Project Structure

```text
Household-Monitoring/
│
├── main.py
├── model_utils.py
├── telegram_utils.py
├── storage_utils.py
├── ai_utils.py
│
├── models/
│   └── activity_model.h5
│
├── snapshots/
│
├── dataset/
│   ├── cooking/
│   ├── cleaning/
│   ├── washing/
│   ├── cutting/
│   └── theft/
│
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/your-repository.git
```

Navigate to project directory:

```bash
cd your-repository
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Project

For webcam:

```bash
python main.py
```

For IP Webcam:

Update:

```python
IP_WEBCAM_URL = "http://YOUR_IP:8080/video"
```

Then run:

```bash
python main.py
```

---

## Future Enhancements

- Object Tracking
- Missing Item Detection
- Smart Door Lock Integration
- Mobile Application
- Multi-Camera Monitoring
- Face Recognition
- Voice-Based Commands
- Edge AI Deployment using Raspberry Pi

---

## Social Impact

This project improves household security, transparency, and accountability by providing intelligent monitoring instead of passive surveillance. It is particularly beneficial for working professionals, senior citizens, families, and property owners who require real-time visibility and remote access control.

---

## Contributors

- @shreeshanthgoud
- @poralapoornachandra

---

## License

This project is developed for academic, research, and innovation purposes.
