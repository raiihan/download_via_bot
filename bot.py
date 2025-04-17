import os
import logging
from telegram import Update, InputMediaDocument, InputMediaVideo, InputMediaPhoto
from telegram.ext import Application, CommandHandler, ContextTypes
from fastapi import FastAPI, Request
import telegram
import asyncio

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot credentials
TOKEN = '7760025681:AAELVpPgZn9kDbbtiXvgEz11XW_VdVUYC64'
CHANNEL_ID = -1002676143465
WEBHOOK_URL = "https://<your-railway-or-server-domain>/webhook"

# Initialize bot and application
bot = telegram.Bot(token=TOKEN)
app = FastAPI()
tg_app = Application.builder().token(TOKEN).build()

# --- Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if args:
        message_id = args[0]
        await send_file_copy(update, context, message_id)
    else:
        await update.message.reply_text("👋 Hello! Use /search to browse files.")

async def send_file_copy(update: Update, context: ContextTypes.DEFAULT_TYPE, message_id: str):
    try:
        status = await update.message.reply_text("📦 Preparing your file...")

        # Get the original message from Channel B
        original = await context.bot.get_chat(CHANNEL_ID)
        message = await context.bot.get_message(CHANNEL_ID, int(message_id))

        if message.document:
            await context.bot.send_document(update.effective_chat.id, message.document.file_id, caption=message.caption)
        elif message.video:
            await context.bot.send_video(update.effective_chat.id, message.video.file_id, caption=message.caption)
        elif message.photo:
            await context.bot.send_photo(update.effective_chat.id, message.photo[-1].file_id, caption=message.caption)
        else:
            await context.bot.send_message(update.effective_chat.id, "✅ File found but type is not supported.")

        await status.delete()

    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("⚠️ Sorry, file not found or has been deleted.")

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔎 Search feature coming soon!")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update: {update} caused error: {context.error}")

# --- Webhook Setup ---
@app.post("/webhook")
async def telegram_webhook(req: Request):
    data = await req.json()
    update = telegram.Update.de_json(data, bot)
    await tg_app.process_update(update)
    return {"ok": True}

@app.on_event("startup")
async def startup():
    await bot.delete_webhook()
    await bot.set_webhook(url=WEBHOOK_URL)
    print("Webhook set.")

# --- Add Handlers ---
tg_app.add_handler(CommandHandler("start", start))
tg_app.add_handler(CommandHandler("search", search))
tg_app.add_error_handler(error_handler)

# --- For Local Testing (Optional) ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
