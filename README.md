# 🌿 SmartFarm — ESP32-CAM Human Detection Dashboard

A Flask-based security monitor for your smart farm. Receives frames from an ESP32-CAM,
runs YOLOv8 human detection, displays a live tactical dashboard, and sends Telegram alerts
when a person is detected.

---

## 📁 Project Structure

```
smart_farm/
├── app.py                  # Flask entry point
├── config.py               # All settings in one place
├── requirements.txt
│
├── routes/
│   ├── upload.py           # POST /upload  — receives ESP32 frames
│   └── stream.py           # GET  /status  — JSON state for frontend
│
├── utils/
│   ├── state.py            # Shared detection state (singleton)
│   ├── detector.py         # YOLOv8 inference wrapper
│   └── telegram.py         # Telegram alert sender
│
├── templates/
│   └── index.html          # Dashboard HTML
│
├── static/
│   ├── css/dashboard.css   # Tactical dark-mode styles
│   └── js/dashboard.js     # Live polling & UI updates
│
├── photos/                 # Original frames saved here
└── results/                # Annotated frames saved here
```

---

## ⚙️ Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Telegram alerts

**Get your bot token:**
1. Open Telegram → search `@BotFather`
2. Send `/newbot`, follow the steps
3. Copy the token you receive

**Get your chat ID:**
1. Send a message to your new bot
2. Visit: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
3. Find `"chat":{"id": 123456789}` — that's your chat ID

**Set via environment variables (recommended):**
```bash
export TELEGRAM_BOT_TOKEN="123456:ABCdef..."
export TELEGRAM_CHAT_ID="123456789"
python app.py
```

Or edit `config.py` directly:
```python
TELEGRAM_BOT_TOKEN = "123456:ABCdef..."
TELEGRAM_CHAT_ID   = "123456789"
```

### 3. Run the server
```bash
python app.py
```
Open `http://<your-server-ip>:8080` in a browser.

---

## 📡 ESP32-CAM Setup

In your Arduino sketch, send frames via HTTP POST:

```cpp
#include <HTTPClient.h>

void sendFrame(uint8_t* buf, size_t len) {
    HTTPClient http;
    http.begin("http://YOUR_SERVER_IP:8080/upload");
    http.addHeader("Content-Type", "application/octet-stream");
    int code = http.POST(buf, len);
    http.end();
}
```

## 🛰️ ESP32 Motion Detector Setup

If you have a separate ESP32 motion sensor or want to send a motion event without an image, post JSON to the new `/motion` endpoint:

```cpp
#include <WiFi.h>
#include <HTTPClient.h>

void sendMotionEvent() {
    HTTPClient http;
    http.begin("http://YOUR_SERVER_IP:8080/motion");
    http.addHeader("Content-Type", "application/json");

    String body = "{"
        "\"source\": \"ESP32-Motion\"," 
        "\"motion\": true," 
        "\"note\": \"PIR sensor triggered\""
        "}";

    int code = http.POST(body);
    http.end();
}
```

This will:
- update the dashboard state
- send a Telegram alert with the motion event
- return `200 OK` when the motion event is accepted

## ✅ Health Check Endpoint

To verify the server is alive and responding, call:

```
GET http://YOUR_SERVER_IP:8080/check
```

Response:
```json
{
  "status": "YES",
  "message": "Server is alive and responding",
  "timestamp": "2026-05-20 14:30:45"
}
```

Your IoT device can use this to verify connectivity before sending motion or frame data.

---

## 🔔 Telegram Alert Cooldown

By default, alerts are throttled to **one every 30 seconds** to avoid spam.
Change this in `config.py`:
```python
ALERT_COOLDOWN = 30   # seconds
```

---

## 🚀 Features

- ✅ Real-time YOLOv8n human detection
- ✅ Side-by-side original + annotated feed
- ✅ Live statistics (frames, detections, rate)
- ✅ Telegram photo + message alert on detection
- ✅ Cooldown to prevent notification spam
- ✅ Tactical dark-mode dashboard (no page refresh — pure JS polling)
- ✅ Clean modular file structure
