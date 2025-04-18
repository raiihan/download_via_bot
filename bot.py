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
    CallbackQueryHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot Token and Channel ID
TOKEN = os.getenv("BOT_TOKEN", "7760025681:AAELVpPgZn9kDbbtiXvgEz11XW_VdVUYC64")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "-1002676143465"))

# Create FastAPI app
app = FastAPI()

# Global app variable for Telegram bot
telegram_app: Application = None

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if args:
        message_id = args[0]
        await send_file_from_channel(update, context, message_id)
    else:
        await update.message.reply_text("👋 Hello! Use /search to browse files.")

# Send file from Channel B
async def send_file_from_channel(update: Update, context: ContextTypes.DEFAULT_TYPE, message_id: str):
    try:
        # Show preparing message
        status = await update.message.reply_text("📦 Preparing your file...")
        await context.bot.forward_message(
            chat_id=update.effective_chat.id,
            from_chat_id=CHANNEL_ID,
            message_id=int(message_id)
        )
        await status.delete()
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("⚠️ Sorry, file not found or has been deleted.")

# Search command handler
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔎 Search feature coming soon!")

# Telegram webhook endpoint
@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return {"status": "ok"}

# Set up Telegram bot
async def setup_bot():
    global telegram_app
    telegram_app = Application.builder().token(TOKEN).build()
    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(CommandHandler("search", search))
    await telegram_app.initialize()
    await telegram_app.start()
webhook_url = os.getenv("WEBHOOK_BASE", "").strip()
if webhook_url:
    await telegram_app.bot.set_webhook(f"{webhook_url}/webhook")
    logger.info(f"Webhook set to {webhook_url}/webhook")
else:
    logger.warning("⚠️ WEBHOOK_BASE not set in environment — skipping webhook setup.")


# Run setup during startup
@app.on_event("startup")
async def on_startup():
    await setup_bot()

# Shutdown Telegram bot
@app.on_event("shutdown")
async def on_shutdown():
    await telegram_app.stop()
