import os
import requests
from flask import request, jsonify

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

def handle_telegram():
    data = request.json or {}

    message = data.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "")

    reply = process_message(text)

    if chat_id:
        send_message(chat_id, reply)

    return jsonify({"status": "ok"})


def process_message(text):
    return f"Echo: {text}"


def send_message(chat_id, text):
    url = f"{TELEGRAM_API}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)
