import os
import logging
import spacy
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Logging for debugging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Simple rule-based troubleshooting
def diagnose_problem(text: str) -> str:
    text = text.lower()

    if "battery" in text or "won't start" in text or "clicking" in text:
        return " This sounds like a **battery issue**. Check if it needs a jump-start or replacement."
    elif "brake" in text or "screech" in text or "grinding" in text:
        return " This may be a **brake problem**. Please check brake pads and discs."
    elif "overheat" in text or "smoke" in text or "temperature" in text:
        return " Engine is overheating. Check coolant and radiator."
    elif "oil" in text:
        return " Low oil pressure. Please check your oil levels."
    else:
        return " I’m not sure. Please describe the problem in more detail."

# Commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hi! I’m your car diagnosis bot. Tell me what’s wrong with your car.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Just type your car problem, e.g. 'My car won’t start' or 'Brakes are screeching'.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    response = diagnose_problem(user_message)
    await update.message.reply_text(response)

def main():
    if not BOT_TOKEN:
        raise ValueError(" TELEGRAM_BOT_TOKEN not set in .env file")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
