from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from telegram.constants import ParseMode
import requests


async def paste(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    message = update.effective_message

    if message.reply_to_message:
        data = message.reply_to_message.text
    elif len(args) >= 1:
        data = message.text.split(None, 1)[1]
    else:
        await message.reply_text("What am I supposed to do with this?")
        return

    try:
        response = requests.post("https://nekobin.com/api/documents",
                                 json={"content": data})
        json_data = response.json()
        print("Nekobin raw response:",
              json_data)
        key = json_data.get("result", {}).get("key")
        if not key:
            raise ValueError("Nekobin response missing key")
    except Exception as e:
        await message.reply_text(f"Failed to paste: {e}")
        return

    url = f"https://nekobin.com/{key}"
    reply_text = f"Nekofied to *Nekobin* : {url}"

    await message.reply_text(reply_text,
                             parse_mode=ParseMode.MARKDOWN,
                             disable_web_page_preview=True)


# Define commands as CommandHandler instances
commands = [
    CommandHandler("paste", paste),
]
