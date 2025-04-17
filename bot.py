import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters
)
import aiohttp
from io import BytesIO
import os

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Replace with your bot token and channel ID
TOKEN = '7760025681:AAELVpPgZn9kDbbtiXvgEz11XW_VdVUYC64'
CHANNEL_ID = -1002676143465  # Must be integer, not string
BASE_FILE_URL = f"https://api.telegram.org/bot{TOKEN}/getFile?file_id="

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! Use /search to browse files.")

# Show fake file selector
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📁 File 1", callback_data='message_id:123')],
        [InlineKeyboardButton("📁 File 2", callback_data='message_id:456')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🔎 Please select a file:", reply_markup=reply_markup)

# Handle button clicks
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("message_id:"):
        msg_id = int(data.split(":")[1])

        # Show preparing message
        preparing = await query.message.reply_text("⏳ Preparing your file...")

        try:
            file_msg = await context.bot.forward_message(
                chat_id=update.effective_chat.id,
                from_chat_id=CHANNEL_ID,
                message_id=msg_id
            )
            await preparing.delete()

        except Exception as e:
            logger.error(f"❌ Error: {e}")
            await preparing.edit_text("⚠️ Sorry, this file is no longer available.")

# Error fallback for unknown messages
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❓ Sorry, I didn’t understand that. Use /search to get started.")

# Setup application
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("search", search))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown))

    app.run_polling()

if __name__ == "__main__":
    main()
