import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot Token and Channel ID
TOKEN = '7760025681:AAELVpPgZn9kDbbtiXvgEz11XW_VdVUYC64'
CHANNEL_ID = -1002676143465  # Correct signed integer ID

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

        message = await context.bot.forward_message(
            chat_id=update.effective_chat.id,
            from_chat_id=CHANNEL_ID,
            message_id=int(message_id)
        )

        # Delete preparing message after sending
        await status.delete()

    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("⚠️ Sorry, file not found or has been deleted.")

# Search handler (future)
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔎 Search feature coming soon!")

# Error handler
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update: {update} caused error: {context.error}")

# Run the bot
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("search", search))
    app.add_error_handler(error_handler)

    app.run_polling()

if __name__ == "__main__":
    main()
