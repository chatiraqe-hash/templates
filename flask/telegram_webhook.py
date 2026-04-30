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
            reply = "أرسل رسالة نصية لأتمكن من مساعدتك."
        elif text == "/start":
            reply = start_message()
        elif text == "/help":
            reply = help_message()
        elif text == "/menu":
            reply = menu_message()
        elif text == "/about":
            reply = about_message()
        else:
            reply = process_message(text)
    except Exception:
        reply = "حدث خطأ مؤقت، حاول مرة أخرى."

    if chat_id:
        send_message(chat_id, reply)

    return jsonify({"status": "ok"})


def start_message():
    return (
        "مرحباً بك في شركة العراق الرقمية.\n\n"
        "أنا مساعد ذكي يعمل بالذكاء الاصطناعي.\n"
        "اكتب سؤالك مباشرة، أو استخدم /menu لعرض الخيارات."
    )


def help_message():
    return (
        "طريقة الاستخدام:\n\n"
        "- اكتب أي سؤال وسأجيبك مباشرة.\n"
        "- اكتب: اشرح لي ... للحصول على شرح.\n"
        "- اكتب: لخص ... للحصول على ملخص.\n"
        "- اكتب: اعطني خطة ... للحصول على خطة منظمة.\n\n"
        "الأوامر:\n"
        "/start - بداية البوت\n"
        "/menu - عرض القائمة\n"
        "/about - معلومات عن الشركة\n"
        "/help - المساعدة"
    )


def menu_message():
    return (
        "القائمة الرئيسية:\n\n"
        "1. اسأل سؤالاً مباشراً\n"
        "2. اطلب ملخصاً\n"
        "3. اطلب شرحاً\n"
        "4. اطلب خطة عمل\n"
        "5. اطلب فكرة مشروع\n\n"
        "مثال:\n"
        "اريد خطة لمشروع ذكاء اصطناعي"
    )


def about_message():
    return (
        "شركة العراق الرقمية\n\n"
        "منصة تقنية تهدف إلى بناء حلول ذكية باستخدام الذكاء الاصطناعي، "
        "الأتمتة، وتطبيقات الويب لخدمة الأفراد والشركات."
    )


def process_message(text):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    system_prompt = """
أنت مساعد ذكي تابع لشركة العراق الرقمية.

قواعد الإجابة:
- استخدم العربية الفصحى الواضحة.
- كن دقيقاً ومباشراً.
- لا تستخدم كلمات أجنبية إلا عند الضرورة التقنية.
- لا تخترع معلومات.
- اجعل الرد منظماً بعناوين ونقاط عند الحاجة.
- إذا كان السؤال عاماً جداً، اطلب توضيحاً مختصراً.
- إذا طُلب ملخص، قدم تعريفاً مختصراً ثم نقاطاً أساسية ثم أمثلة.
- إذا طُلبت خطة، قدم خطوات عملية مرتبة.
"""

    data = {
        "model": "llama-3.1-8b-instant",
        "temperature": 0.3,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ]
    }

    response = requests.post(url, headers=headers, json=data, timeout=30)

    if response.status_code != 200:
        return "تعذر الحصول على رد حالياً. حاول مرة أخرى بعد قليل."

    result = response.json()

    return result["choices"][0]["message"]["content"]


def send_message(chat_id, text):
    url = f"{TELEGRAM_API}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload, timeout=30)
