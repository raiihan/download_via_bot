import asyncio
import nest_asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "7760025681:AAELVpPgZn9kDbbtiXvgEz11XW_VdVUYC64"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello Sunny! Bot is running perfectly!")

async def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    print("✅ Bot is running and listening for /start")
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    await application.updater.idle()

if __name__ == "__main__":
    # Fix for Railway async environment
    nest_asyncio.apply()
    asyncio.run(main())
