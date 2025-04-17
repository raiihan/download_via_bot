import logging
from telegram import Update, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "7760025681:AAELVpPgZn9kDbbtiXvgEz11XW_VdVUYC64"

logging.basicConfig(level=logging.INFO)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is alive and got your command!")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))

    await app.bot.set_my_commands([BotCommand("start", "Start the bot")])
    print("✅ Bot is running and listening for /start")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
