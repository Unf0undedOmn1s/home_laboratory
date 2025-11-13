import requests
from datetime import datetime

# Telegram Bot Token and Chat ID
TELEGRAM_BOT_TOKEN = "TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "TELEGRAM_CHAT_ID"  # Chat ID

def send_telegram_alert(message: str, level: str = "info"):
    """
    Send an alert message via Telegram.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    emoji = {
        "info": "ℹ️",
        "warning": "⚠️",
        "error": "🚨"
    }.get(level, "📡")

    text = f"{emoji} *Andromeda Alert*\n`{timestamp}`\n\n{message}"

    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"}
        requests.post(url, json=payload, timeout=5)
        print(f"Telegram alert sent: {message}")
    except Exception as e:
        print(f"Telegram alert failed: {e}")
