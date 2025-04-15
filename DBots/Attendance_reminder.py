import re
import logging
import os
from dotenv import load_dotenv

from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

# === CONFIG ===
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_CHAT_ID = int(os.getenv("GROUP_CHAT_ID"))

# === LOGGING ===
logging.basicConfig(level=logging.INFO)

# === FUNCTIONS ===

def keyword_detected(text):
    return re.search(r"\b(pull[\s\-]?out|late update)\b", text, re.IGNORECASE)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    user = update.effective_user
    text = message.text or ""

    if keyword_detected(text):
        mention = f"@{user.username}" if user.username else user.full_name
        reminder_text = f"Update attendance sheet {mention}"
        await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=reminder_text)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is running!")

# === FLASK SERVER + BOT ===
app = Flask(__name__)
application = None

@app.route('/')
def index():
    return 'Bot is alive!'

import threading

def start_bot():
    def run():
        global application
        application = ApplicationBuilder().token(BOT_TOKEN).build()
        application.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, handle_message))
        application.add_handler(CommandHandler("start", start))
        application.run_polling()

    threading.Thread(target=run).start()

# Immediately start the bot
start_bot()

# === MAIN SETUP ===
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, handle_message))
    app.add_handler(CommandHandler("start", start))

    app.run_polling()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)