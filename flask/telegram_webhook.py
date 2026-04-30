import os
import requests
from flask import request, jsonify

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"


def handle_telegram():
    data = request.json or {}

    message = data.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "").strip()

    try:
        if not text:
            reply = "أرسل طلبك."
        elif text == "/start":
            reply = start_message()
        elif text == "/menu":
            reply = menu_message()
        elif text == "/templates":
            reply = templates_menu()
        else:
            reply = route_request(text)
    except Exception:
        reply = "حدث خطأ مؤقت."

    if chat_id:
        send_message(chat_id, reply)

    return jsonify({"status": "ok"})


# ========================
# COMMANDS
# ========================

def start_message():
    return "مرحباً بك في Forge AI.\nاكتب طلبك أو استخدم /templates"


def menu_message():
    return (
        "القائمة:\n"
        "/templates - توليد Templates\n"
        "اكتب طلبك مباشرة"
    )


def templates_menu():
    return (
        "أنواع التوليد:\n\n"
        "1) flask bot\n"
        "2) api service\n"
        "3) ai assistant\n\n"
        "مثال:\n"
        "generate flask bot with telegram"
    )


# ========================
# ROUTER
# ========================

def route_request(text):
    text_lower = text.lower()

    if "flask" in text_lower:
        return generate_template("flask_bot", text)

    if "api" in text_lower:
        return generate_template("api_service", text)

    if "ai" in text_lower:
        return generate_template("ai_assistant", text)

    return process_ai(text)


# ========================
# TEMPLATE GENERATOR
# ========================

def generate_template(template_type, user_input):
    prompt = f"""
أنت مولد قوالب برمجية احترافي.

المطلوب:
- توليد كود كامل فقط
- بدون شرح
- جاهز للتنفيذ

نوع القالب: {template_type}

طلب المستخدم:
{user_input}
"""

    return call_groq(prompt)


# ========================
# AI RESPONSE
# ========================

def process_ai(text):
    prompt = f"""
أنت مساعد تقني.

أجب بشكل مختصر ومنظم.

{ text }
"""
    return call_groq(prompt)


# ========================
# GROQ
# ========================

def call_groq(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.1-8b-instant",
        "temperature": 0.2,
        "messages": [
            {"role": "system", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=data, timeout=30)

    if response.status_code != 200:
        return "AI Error"

    result = response.json()
    return result["choices"][0]["message"]["content"]


# ========================
# TELEGRAM
# ========================

def send_message(chat_id, text):
    url = f"{TELEGRAM_API}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text[:4000]
    }
    requests.post(url, json=payload, timeout=30)
