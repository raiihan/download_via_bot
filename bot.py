import os
import logging
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)
from telegram.constants import ChatAction

# Bot credentials
TOKEN = os.getenv("BOT_TOKEN", "7760025681:AAELVpPgZn9kDbbtiXvgEz11XW_VdVUYC64")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "-1002676143465"))

# Logger setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# FastAPI instance
app = FastAPI()

# Telegram application
telegram_app = Application.builder().token(TOKEN).build()

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if args:
        message_id = args[0]
        await send_file_from_channel(update, context, message_id)
    else:
        await update.message.reply_text("👋 Hello! Use /search to browse files.")

# Search command
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔎 Search feature coming soon!")

# Forward from Channel B
async def send_file_from_channel(update: Update, context: ContextTypes.DEFAULT_TYPE, message_id: str):
    try:
        status = await update.message.reply_text("📦 Preparing your file...")
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_DOCUMENT)

        await context.bot.forward_message(
            chat_id=update.effective_chat.id,
            from_chat_id=CHANNEL_ID,
            message_id=int(message_id)
        )

        await status.delete()
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("⚠️ Sorry, file not found or has been deleted.")

# Error logger
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update: {update} caused error: {context.error}")

# Webhook route for FastAPI
@app.post("/webhook")
async def handle_webhook(request: Request):
    try:
        data = await request.json()
        update = Update.de_json(data, telegram_app.bot)
        await telegram_app.process_update(update)
        return {"ok": True}
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return {"ok": False}

# Bot setup
async def setup_bot():
    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(CommandHandler("search", search))
    telegram_app.add_error_handler(error_handler)

    # Set webhook URL
    webhook_url = os.getenv("WEBHOOK_URL")  # Set this in Railway variables
    if webhook_url:
        await telegram_app.bot.set_webhook(url=f"{webhook_url}/webhook")

# Start everything
import asyncio
asyncio.run(setup_bot())
