from tg_bot.core.logging import LOGE
from telegram.ext import ContextTypes
import traceback


async def error_handler(update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors caused by updates."""
    # Get the exception info
    error_details = "".join(
        traceback.format_exception(
            type(context.error),
            context.error,
            context.error.__traceback__,
            limit=None,
            chain=True,
        ))

    formatted_error = "GalaxyGeeksBot: Error encountered!\n"

    # Check if update and message are valid
    if update and update.effective_message:
        formatted_error += f"Command sent: {update.effective_message.text}\n\n"
        formatted_error += error_details

        # Send error message to user
        await update.effective_message.reply_text(formatted_error)
    else:
        formatted_error += "Update object is None or has no message\n\n"
        formatted_error += error_details

    # Log the error
    LOGE(formatted_error)
    LOGE("End error handling")
