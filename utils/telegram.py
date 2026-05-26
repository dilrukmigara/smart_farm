"""
Telegram alert sender — notifies when a human is detected.
Includes cooldown to avoid message spam.
"""
import requests
from datetime import datetime
from config import Config

def send_telegram_alert(image_path: str = None):
    """
    Send a Telegram alert when a human is detected.
    Respects the ALERT_COOLDOWN setting to avoid spam.
    Returns True if message was sent, False if skipped or failed.
    """
    from utils.state import state

    now = datetime.now()

    # Cooldown check
    if state.last_alert_time:
        elapsed = (now - state.last_alert_time).total_seconds()
        if elapsed < Config.ALERT_COOLDOWN:
            return False  # Too soon, skip

    token = Config.TELEGRAM_BOT_TOKEN
    chat_id = Config.TELEGRAM_CHAT_ID

    if token == "YOUR_BOT_TOKEN_HERE" or chat_id == "YOUR_CHAT_ID_HERE":
        print("[Telegram] Bot token or chat ID not configured. Skipping alert.")
        return False

    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    message = (
        f"🚨 *SMART FARM ALERT* 🚨\n\n"
        f"👤 *Human Detected!*\n"
        f"🕐 Time: `{timestamp}`\n"
        f"📷 Camera: ESP32-CAM\n\n"
        f"_Check your farm dashboard immediately._"
    )

    try:
        # Send text message
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        resp = requests.post(url, json={
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }, timeout=5)

        # Optionally send the detection image
        if image_path and resp.status_code == 200:
            photo_url = f"https://api.telegram.org/bot{token}/sendPhoto"
            with open(image_path, "rb") as photo:
                requests.post(photo_url, data={"chat_id": chat_id}, files={"photo": photo}, timeout=10)

        if resp.status_code == 200:
            state.last_alert_time = now
            print(f"[Telegram] Alert sent at {timestamp}")
            return True
        else:
            print(f"[Telegram] Failed: {resp.status_code} {resp.text}")
            return False

    except Exception as e:
        print(f"[Telegram] Error: {e}")
        return False


def send_telegram_message(message: str, image_path: str = None):
    """Send a custom Telegram message with optional photo."""
    from utils.state import state

    now = datetime.now()

    if state.last_alert_time:
        elapsed = (now - state.last_alert_time).total_seconds()
        if elapsed < Config.ALERT_COOLDOWN:
            return False

    token = Config.TELEGRAM_BOT_TOKEN
    chat_id = Config.TELEGRAM_CHAT_ID

    if token == "YOUR_BOT_TOKEN_HERE" or chat_id == "YOUR_CHAT_ID_HERE":
        print("[Telegram] Bot token or chat ID not configured. Skipping alert.")
        return False

    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        resp = requests.post(url, json={
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }, timeout=5)

        if image_path and resp.status_code == 200:
            photo_url = f"https://api.telegram.org/bot{token}/sendPhoto"
            with open(image_path, "rb") as photo:
                requests.post(photo_url, data={"chat_id": chat_id}, files={"photo": photo}, timeout=10)

        if resp.status_code == 200:
            state.last_alert_time = now
            print(f"[Telegram] Message sent at {now.strftime('%Y-%m-%d %H:%M:%S')}")
            return True
        else:
            print(f"[Telegram] Failed: {resp.status_code} {resp.text}")
            return False
    except Exception as e:
        print(f"[Telegram] Error: {e}")
        return False
