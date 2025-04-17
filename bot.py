import logging
from telegram import Update, BotCommand
from telegram.ext import Application, ApplicationBuilder, CommandHandler, ContextTypes
import asyncio

BOT_TOKEN = "7760025681:AAELVpPgZn9kDbbtiXvgEz11XW_VdVUYC64"

logging.basicConfig(level=logging.INFO)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is alive and received your command!")

async def set_commands(app):
    await app.bot.set_my_commands([BotCommand("start", "Start the bot")])

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    await set_commands(app)
    print("✅ Bot is running and listening for /start")
    await app.run_polling()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if "running" in str(e):
            loop = asyncio.get_event_loop()
            loop.create_task(main())
            loop.run_forever()
