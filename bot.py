import os
import logging
import asyncio
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Config
TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "-1002676143465"))
WEBHOOK_URL = os.getenv("WEBHOOK_BASE")

# FastAPI app
app = FastAPI()

# Global bot application
telegram_app = None


# --- Bot Command Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if args:
        await send_file_from_channel(update, context, args[0])
    else:
        await update.message.reply_text("👋 Hello! Use /search to browse files.")


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔎 Search feature coming soon!")


async def send_file_from_channel(update: Update, context: ContextTypes.DEFAULT_TYPE, message_id: str):
    try:
        status = await update.message.reply_text("📦 Preparing your file...")
        await context.bot.forward_message(
            chat_id=update.effective_chat.id,
            from_chat_id=CHANNEL_ID,
            message_id=int(message_id)
        )
        await status.delete()
    except Exception as e:
        logger.error(f"Error sending file: {e}")
        await update.message.reply_text("⚠️ File not found or deleted.")


# --- Webhook Endpoint ---
@app.post("/webhook")
async def telegram_webhook(request: Request):
    global telegram_app
    try:
        data = await request.json()
        update = Update.de_json(data, telegram_app.bot)
        await telegram_app.process_update(update)
    except Exception as e:
        logger.error(f"Webhook error: {e}")
    return {"status": "ok"}


# --- Startup Tasks ---
@app.on_event("startup")
async def on_startup():
    global telegram_app
    telegram_app = Application.builder().token(TOKEN).build()
    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(CommandHandler("search", search))
    await telegram_app.initialize()
    await telegram_app.start()

    if WEBHOOK_URL:
        await telegram_app.bot.set_webhook(f"{WEBHOOK_URL}/webhook")
        logger.info(f"Webhook set to {WEBHOOK_URL}/webhook")
    else:
        logger.warning("❌ WEBHOOK_BASE not set — webhook not configured!")


# --- Shutdown ---
@app.on_event("shutdown")
async def on_shutdown():
    await telegram_app.stop()
