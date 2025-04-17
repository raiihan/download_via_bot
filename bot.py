import logging
from telegram import Update, BotCommand
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

# === CONFIGURATION ===
BOT_TOKEN = "7760025681:AAELVpPgZn9kDbbtiXvgEz11XW_VdVUYC64"
CHANNEL_B_ID = -1002676143465  # Store Room 🏬
OWNER_USERNAME = "connectYourUniverse"

# === STORAGE ===
file_db = {}  # Example: {"file001": {"title": ..., "720": file_id, "1080": file_id}}
latest_file_key = None

# === LOGGING ===
logging.basicConfig(level=logging.INFO)

# === HANDLERS ===
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if args:
        key = args[0]
        if key in file_db:
            await send_file(update, context, key)
        else:
            await update.message.reply_text("❌ File not found.")
    else:
        if latest_file_key:
            await send_file(update, context, latest_file_key)
        else:
            await update.message.reply_text("👋 Welcome! No files available yet.")

async def send_file(update: Update, context: ContextTypes.DEFAULT_TYPE, key):
    data = file_db[key]
    text = f"""
🎬 Here’s your file:
🔥 Title: {data['title']}
🎥 Available Formats:

📁 720p Quality
📁 1080p Quality

⬇️ Click below to download and Enjoy

via @{OWNER_USERNAME}
"""
    if '720' in data:
        await update.message.reply_video(video=data['720'], caption=text, parse_mode='Markdown')
    if '1080' in data:
        await update.message.reply_video(video=data['1080'])

async def channel_post_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("📩 Received file from channel")  # debug log
    global latest_file_key
    msg = update.channel_post
    if not msg.video:
        return

    title = msg.caption or "Untitled"
    file_id = msg.video.file_id

    if "720" in title:
        key = title.lower().split("720")[0].strip().replace(" ", "_")
        if key not in file_db:
            file_db[key] = {"title": title}
        file_db[key]['720'] = file_id
    elif "1080" in title:
        key = title.lower().split("1080")[0].strip().replace(" ", "_")
        if key not in file_db:
            file_db[key] = {"title": title}
        file_db[key]['1080'] = file_id

    latest_file_key = key
    logging.info(f"Stored: {key} => 720: {'720' in title}, 1080: {'1080' in title}")

async def set_commands(app):
    await app.bot.set_my_commands([
        BotCommand("start", "Start and get the file")
    ])

# === RUNNING APP ===
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start_command))
app.add_handler(MessageHandler(filters.Chat(CHANNEL_B_ID) & filters.VIDEO, channel_post_handler))

async def run_bot():
    await set_commands(app)
    print("✅ Bot is running on Railway...")
    await app.run_polling()

import asyncio
asyncio.get_event_loop().create_task(run_bot())
asyncio.get_event_loop().run_forever()
