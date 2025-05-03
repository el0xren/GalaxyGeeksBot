from contextlib import redirect_stdout
from cowsay import cow
import io
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from telegram.constants import ParseMode


async def cowsay(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Format text using cowsay."""
    with io.StringIO() as buf, redirect_stdout(buf):
        try:
            cow(update.effective_message.text.split(" ", 1)[1])
        except IndexError:
            await update.effective_message.reply_text(
                "Error: Write something after the command!")
        else:
            await update.effective_message.reply_text(
                f"`{buf.getvalue()}`", parse_mode=ParseMode.MARKDOWN)


# Define commands as CommandHandler instances
commands = [
    CommandHandler("cowsay", cowsay),
]
