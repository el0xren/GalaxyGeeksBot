from datetime import datetime
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    before = datetime.now()
    message = await update.message.reply_text("Appraising..")
    now = datetime.now()
    res = (now - before).microseconds / 1000
    await message.edit_text(f"ping = {res}ms")


# Define commands as CommandHandler instances
commands = [
    CommandHandler("ping", ping),
]
