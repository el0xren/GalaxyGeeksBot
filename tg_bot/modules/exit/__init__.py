from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from tg_bot.core.bot import get_bot_context
from tg_bot.core.permissions import owner
from tg_bot.core.logging import LOGI


@owner
async def exit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Gracefully shut down the bot."""
    LOGI("Exit command received, shutting down bot")
    await update.effective_message.reply_text("Exiting now...")

    # Get the Bot instance and stop it gracefully
    bot = get_bot_context()
    if bot:
        await bot.stop()
    else:
        LOGI("Bot context not available, cannot stop gracefully")


# Define commands as CommandHandler instances
commands = [
    CommandHandler("exit", exit),
]
