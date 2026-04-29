from flask import Flask, request, jsonify
from telegram_webhook import handle_telegram

app = Flask(__name__)

@app.route("/")
def home():
    return {"status": "Forge AI running"}

@app.route("/webhook", methods=["POST"])
def webhook():
    return handle_telegram()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
