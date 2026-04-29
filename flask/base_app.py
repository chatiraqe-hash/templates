from flask import Flask, request, jsonify
from telegram_webhook import handle_telegram
import requests
import os

app = Flask(__name__)

@app.route("/")
def home():
    return {"status": "Forge AI running"}

@app.route("/webhook", methods=["POST"])
def webhook():
    return handle_telegram()

@app.route("/set_webhook")
def set_webhook():
    url = os.getenv("RENDER_URL") + "/webhook"
    token = os.getenv("TELEGRAM_TOKEN")

    telegram_url = f"https://api.telegram.org/bot{token}/setWebhook"
    response = requests.get(telegram_url, params={"url": url})

    return response.json()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
