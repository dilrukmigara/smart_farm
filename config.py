import os

class Config:
    SAVE_FOLDER = "photos"
    RESULT_FOLDER = "results"
    MODEL_PATH = "yolov8n.pt"

    # Telegram Bot Settings
    TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
    TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "YOUR_CHAT_ID_HERE")

    # Alert cooldown in seconds (avoid spam)
    ALERT_COOLDOWN = 30

    # Create folders on startup
    os.makedirs(SAVE_FOLDER, exist_ok=True)
    os.makedirs(RESULT_FOLDER, exist_ok=True)
