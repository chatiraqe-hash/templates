from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return {"status": "Forge AI running"}

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    # Placeholder logic
    user_input = data.get("message", "")

    response = {
        "reply": f"Received: {user_input}"
    }

    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
