# Flask AI Telegram Bot Template

## Overview
Starter template for building an AI-powered Telegram bot using Flask and Groq.

## Features
- Telegram webhook integration
- AI responses (Groq)
- Commands system (/start, /help, /menu, /about)
- Production-ready error handling

## Setup

1. Clone repo
2. Install dependencies:
   pip install -r requirements.txt

3. Set environment variables:
   TELEGRAM_TOKEN=your_token
   GROQ_API_KEY=your_key
   RENDER_URL=your_url

4. Run:
   gunicorn base_app:app

## Usage

- Send messages directly → AI response
- Use /menu → see options
