import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
import aiohttp
from io import BytesIO

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace with your actual bot token
TOKEN = '7760025681:AAELVpPgZn9kDbbtiXvgEz11XW_VdVUYC64'
CHANNEL_ID = '-1002676143465'  # Your Channel B's ID
FILE_URL_BASE = 'https://api.telegram.org/file/bot'  # Telegram file URL API

# To store user data
user_files = {}

# Function to start the bot
async def start(update: Update, context):
    user = update.effective_user
    await update.message.reply_text(f"Hello {user.first_name}, welcome to the file selector bot! Use the buttons to select a file.")

# Function to display the file selector
async def show_file_selector(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("File 1", callback_data='file1')],
        [InlineKeyboardButton("File 2", callback_data='file2')],
        [InlineKeyboardButton("File 3", callback_data='file3')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Please select a file to download:', reply_markup=reply_markup)

# Function to handle file selection
async def file_selection(update: Update, context):
    query = update.callback_query
    file_id = query.data
    # Fetch file details from Channel B using the file_id or relevant data
    file_url = await get_file_url(file_id)  # Implement function to fetch URL
    if file_url:
        file = await download_file(file_url)
        # Send the file to the user with relevant details
        await send_file(update, file)
    else:
        await query.answer("File not found.")
        await query.message.reply_text("Sorry, the file could not be found.")

# Function to fetch file URL
async def get_file_url(file_id):
    # Logic to fetch the file URL from Telegram's API based on file_id
    url = f"{FILE_URL_BASE}{TOKEN}/getFile?file_id={file_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            result = await response.json()
            if response.status == 200 and 'result' in result:
                file_path = result['result']['file_path']
                return f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
    return None

# Function to download the file from URL
async def download_file(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return BytesIO(await response.read())

# Function to send the file to the user with details
async def send_file(update, file):
    # Get file size and type if necessary
    file_size = len(file.getvalue())  # Example, real implementation might vary
    await update.message.reply_text(f"Preparing the file... Size: {file_size} bytes")
    await update.message.reply_document(file, caption="File is ready for download!")

# Function to handle errors and fallback
async def handle_error(update: Update, context):
    logger.error(f"Error occurred: {context.error}")
    await update.message.reply_text("An error occurred while processing your request. Please try again later.")

# Setup handlers
def setup_handlers(application):
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("search", show_file_selector))
    application.add_handler(CallbackQueryHandler(file_selection))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_error))

# Main function to run the bot
async def main():
    # Create the Application and set up handlers
    application = Application.builder().token(TOKEN).build()
    setup_handlers(application)

    # Start the bot
    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
