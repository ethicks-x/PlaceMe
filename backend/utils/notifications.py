import os

import requests


def send_chat_notification(message):
    webhook_url = os.getenv("GOOGLE_CHAT_WEBHOOK_URL")
    if not webhook_url:
        return

    resp = requests.post(webhook_url, json={"text": message}, timeout=5)
    resp.raise_for_status()
