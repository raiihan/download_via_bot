import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import aiohttp
import os

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot token and Channel B ID
TOKEN = '7760025681:AAELVpPgZn9kDbbtiXvgEz11XW_VdVUYC64'
CHANNEL_ID = -1002676143465  # Channel B (Store Room 🏪)

# START HANDLER
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    args = context.args

    if args:
        message_id = args[0]
        status = await update.message.reply_text("Preparing your file...")
        try:
            # Forward the message with the file from Channel B
            sent = await context.bot.copy_message(
                chat_id=update.effective_chat.id,
                from_chat_id=CHANNEL_ID,
                message_id=int(message_id)
            )
            # Delete the status message
            await status.delete()
        except Exception as e:
            logger.error(f"Error forwarding message: {e}")
            await status.edit_text("❌ Sorry, this file is no longer available.")
    else:
        await update.message.reply_text(f"👋 Hello {user.first_name}! Use /search to browse files.")

# SEARCH HANDLER (Dummy button selector)
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("File 14", url="https://t.me/NoSourceFileBot?start=14")],
        [InlineKeyboardButton("File 15", url="https://t.me/NoSourceFileBot?start=15")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose a file:", reply_markup=reply_markup)

# MAIN FUNCTION
async def main():
    application = Application.builder().token(TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("search", search))

    # Run the bot
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
