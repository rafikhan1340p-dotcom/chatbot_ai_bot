import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# 1. তোমার Token আর API Key এখানে বসাও
TELEGRAM_TOKEN = "এখানে_BotFather_এর_Token_বসাও"
GEMINI_API_KEY = "এখানে_Google_AI_Studio_এর_API_Key_বসাও"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

app = Flask('')

@app.route('/')
def home():
    return "Chatbot AI is alive"

def run_flask():
  app.run(host='0.0.0.0', port=8080)

# /start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("হ্যালো! আমি Chatbot AI 😊 কিছু জিজ্ঞেস করো।")

# সব Message এর Reply
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        response = model.generate_content(user_text)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text("Sorry, একটু সমস্যা হইছে। আবার Try করো।")

def main():
    # Flask চালু রাখার জন্য
    t = threading.Thread(target=run_flask)
    t.start()

    # Telegram Bot চালু
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
    application.run_polling()

if __name__ == '__main__':
    main()