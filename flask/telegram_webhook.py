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
    text = message.get("text", "")

    reply = process_message(text)

    if chat_id:
        send_message(chat_id, reply)

    return jsonify({"status": "ok"})


def process_message(text):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    system_prompt = """
أنت خبير ذكاء اصطناعي تابع لشركة العراق الرقمية.

التعليمات الصارمة:
- استخدم العربية الفصحى فقط
- لا تستخدم أي كلمات أجنبية (لا English ولا Russian)
- لا تخترع مصطلحات
- كن دقيق علمياً 100%
- اكتب بأسلوب واضح ومنظم
- استخدم عناوين + نقاط فقط
- لا تكرر الجمل
- لا تكتب مقدمات عامة

عند طلب "ملخص":
1) تعريف من سطر واحد فقط
2) 3 إلى 5 نقاط أساسية صحيحة علمياً
3) 2 إلى 3 أمثلة تطبيقية حقيقية وواضحة
"""

    data = {
        "model": "llama-3.1-8b-instant",
        "temperature": 0.3,
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": text
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        return "حدث خطأ في الاتصال بالذكاء الاصطناعي"

    result = response.json()

    return result["choices"][0]["message"]["content"]


def send_message(chat_id, text):
    url = f"{TELEGRAM_API}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)
