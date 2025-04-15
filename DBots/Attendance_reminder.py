import re
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

# === CONFIG ===
BOT_TOKEN = "7856528774:AAG5gRI-6SuC7m5rrixVefgJkLX6WDmSCPA"
GROUP_CHAT_ID = -1002500830311  # Replace with actual group chat ID

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

# === MAIN SETUP ===
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, handle_message))
    app.add_handler(CommandHandler("start", start))

    app.run_polling()

if __name__ == '__main__':
    main()